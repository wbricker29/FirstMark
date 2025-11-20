"""AgentOS-aware workflow orchestration for candidate screening.

This module contains the AgentOSCandidateWorkflow class that coordinates
the four-step screening process (research → quality check → incremental search → assessment).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, cast

from agno.db.base import SessionType
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from agno.run import RunContext
from agno.workflow import Step, Workflow
from agno.workflow.types import StepInput, StepOutput

from demo.agents import (
    assess_candidate,
    run_incremental_search,
    run_research,
)
from demo.models import AssessmentResult, CandidateDict
from demo.screening_helpers import (
    check_research_quality,
    extract_candidate_context,
    reconstruct_research,
)
from demo.screening_service import LogSymbols
from demo.settings import settings

# Use centralized log symbols from screening_service
_LOG_SYMBOLS = LogSymbols()
LOG_SEARCH = _LOG_SYMBOLS.search
LOG_SUCCESS = _LOG_SYMBOLS.success
LOG_ERROR = _LOG_SYMBOLS.error


class AgentOSCandidateWorkflow:
    """AgentOS-aware workflow that runs the four candidate screening steps."""

    def __init__(self, log: logging.Logger, agent_os: AgentOS | None = None) -> None:
        self.logger = log
        self.agent_os = agent_os
        db_path = Path("tmp") / "agno_sessions.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.workflow = Workflow(
            id="talent-signal-candidate-workflow",
            name="Talent Signal Candidate Workflow",
            description="Deep research → quality check → optional incremental search → assessment",
            db=SqliteDb(
                db_file=str(db_path),
            ),
            stream_events=True,
            # AgentOS supplies ``RunContext`` to step executors, but the public type
            # signature exposes ``Callable[[StepInput], StepOutput]``. ``cast`` keeps
            # type-checking happy without altering runtime behavior.
            steps=[
                Step(
                    name="deep_research",
                    description="Run Deep Research agent",
                    executor=cast(Any, self._deep_research_step),
                ),
                Step(
                    name="quality_check",
                    description="Evaluate research sufficiency",
                    executor=cast(Any, self._quality_check_step),
                ),
                Step(
                    name="incremental_search",
                    description="Run incremental search when the quality gate fails",
                    executor=cast(Any, self._incremental_search_step),
                ),
                Step(
                    name="assessment",
                    description="Score the candidate against the role spec",
                    executor=cast(Any, self._assessment_step),
                ),
            ],
        )

    def run_candidate_workflow(
        self,
        candidate_data: CandidateDict,
        role_spec_markdown: str,
        screen_id: str,
        custom_instructions: str | None = None,
    ) -> tuple[AssessmentResult, Any]:
        """Run the candidate screening workflow.

        Returns:
            Tuple of (assessment, research) where research is ExecutiveResearchResult or None.
        """
        candidate_id = (
            candidate_data.get("id")
            or candidate_data.get("record_id")
            or candidate_data.get("airtable_id")
            or "candidate"
        )
        session_id = f"screen_{screen_id}_{candidate_id}"
        run_input = {
            "candidate": candidate_data,
            "role_spec_markdown": role_spec_markdown,
            "screen_id": screen_id,
            "session_id": session_id,
            "custom_instructions": custom_instructions,
        }

        # Use direct workflow reference.
        # AgentOS tracks workflows registered during initialization (see agentos_app.py),
        # but we use the direct reference for execution to ensure consistent behavior.
        workflow_to_run = self.workflow

        self.logger.info(
            "%s Executing workflow %s with session_id=%s",
            LOG_SEARCH,
            workflow_to_run.id or workflow_to_run.name,
            session_id,
        )
        run_output = workflow_to_run.run(input=run_input, session_id=session_id)

        # Verify session was persisted to database (fail-fast check)
        if workflow_to_run.db:
            session = workflow_to_run.db.get_session(
                session_id, session_type=SessionType.WORKFLOW
            )
            if not session:
                raise RuntimeError(
                    f"Session {session_id} was not persisted to database."
                )

        # Extract assessment and research from workflow output.
        assessment = self._extract_assessment_from_output(run_output, session_id)
        research = self._extract_research_from_output(run_output, session_id)

        return assessment, research

    @staticmethod
    def _extract_workflow_state(session_data: Any) -> dict[str, Any]:
        """Normalize workflow_data retrieval from AgentOS session payloads."""

        if not isinstance(session_data, dict):
            return {}

        workflow_data = session_data.get("workflow_data")
        if isinstance(workflow_data, dict) and workflow_data:
            return workflow_data

        session_state = session_data.get("session_state")
        if isinstance(session_state, dict):
            nested = session_state.get("workflow_data")
            if isinstance(nested, dict):
                return nested

        return {}

    def _extract_assessment_from_output(
        self, run_output: Any, session_id: str
    ) -> AssessmentResult:
        """Extract AssessmentResult from workflow run output.

        Args:
            run_output: Output from workflow.run() call.
            session_id: Session ID for logging/debugging.

        Returns:
            AssessmentResult from the workflow execution.

        Raises:
            RuntimeError: If assessment cannot be extracted from output or session state.
        """
        # Primary path: Extract from workflow output content
        # The assessment step returns StepOutput with content={"assessment": assessment.model_dump()}
        if hasattr(run_output, "content"):
            content = run_output.content
            if isinstance(content, dict):
                assessment_data = content.get("assessment")
                if assessment_data:
                    if isinstance(assessment_data, AssessmentResult):
                        return assessment_data
                    if isinstance(assessment_data, dict):
                        try:
                            return AssessmentResult.model_validate(assessment_data)
                        except Exception as e:
                            self.logger.warning(
                                "Failed to parse assessment from workflow output: %s", e
                            )

        # Fallback: Extract from session state
        if self.workflow.db:
            try:
                from agno.session.workflow import WorkflowSession

                session = self.workflow.db.get_session(
                    session_id, session_type=SessionType.WORKFLOW
                )
                if session and isinstance(session, WorkflowSession):
                    session_data = session.session_data or {}
                    workflow_data = self._extract_workflow_state(session_data)
                    assessment_obj = workflow_data.get("assessment")
                    if assessment_obj:
                        if isinstance(assessment_obj, AssessmentResult):
                            return assessment_obj
                        if isinstance(assessment_obj, dict):
                            try:
                                return AssessmentResult.model_validate(assessment_obj)
                            except Exception as e:
                                self.logger.warning(
                                    "Failed to parse assessment from session state: %s",
                                    e,
                                )
            except Exception as e:
                self.logger.warning(
                    "Failed to retrieve assessment from session state: %s", e
                )

        raise RuntimeError(
            f"Workflow did not produce an assessment result for session {session_id}. "
            "Check workflow run output and session state."
        )

    def _extract_research_from_output(self, run_output: Any, session_id: str) -> Any:
        """Extract ExecutiveResearchResult from workflow run output.

        Args:
            run_output: Output from workflow.run() call.
            session_id: Session ID for logging/debugging.

        Returns:
            ExecutiveResearchResult from the workflow execution, or None if not found.
        """
        # Extract from session state
        if self.workflow.db:
            try:
                from agno.session.workflow import WorkflowSession

                from demo.models import ExecutiveResearchResult

                session = self.workflow.db.get_session(
                    session_id, session_type=SessionType.WORKFLOW
                )
                self.logger.debug("Session retrieved: %s", session is not None)
                if session and isinstance(session, WorkflowSession):
                    session_data = session.session_data or {}
                    self.logger.debug(
                        "Session data keys: %s", list(session_data.keys())
                    )
                    workflow_data = self._extract_workflow_state(session_data)
                    self.logger.debug(
                        "Workflow data keys: %s",
                        list(workflow_data.keys()) if workflow_data else "None",
                    )
                    research_data = workflow_data.get("research")
                    self.logger.debug(
                        "Research data present: %s", research_data is not None
                    )
                    if research_data:
                        if isinstance(research_data, ExecutiveResearchResult):
                            self.logger.info(
                                "✅ Extracted research from session (ExecutiveResearchResult object)"
                            )
                            return research_data
                        if isinstance(research_data, dict):
                            try:
                                result = ExecutiveResearchResult.model_validate(
                                    research_data
                                )
                                self.logger.info(
                                    "✅ Extracted research from session (dict → ExecutiveResearchResult)"
                                )
                                return result
                            except Exception as e:
                                self.logger.warning(
                                    "Failed to parse research from session state: %s",
                                    e,
                                )
                    else:
                        self.logger.warning(
                            "⚠️  Research data not found in session workflow_data"
                        )
                else:
                    self.logger.warning(
                        "⚠️  Session not found or wrong type for %s", session_id
                    )
            except Exception as e:
                self.logger.warning(
                    "Failed to retrieve research from session state: %s", e
                )

        self.logger.warning("❌ Returning None for research (not found in session)")
        return None

    # ------------------------------------------------------------------
    # Step helpers
    # ------------------------------------------------------------------

    def _deep_research_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        # Initialize session state if needed
        if run_context.session_state is None:
            run_context.session_state = {}

        # Initialize workflow state structure
        if "workflow_data" not in run_context.session_state:
            run_context.session_state["workflow_data"] = {}

        state = run_context.session_state["workflow_data"]

        # Extract input data
        input_data: dict[str, Any] = (
            step_input.input if isinstance(step_input.input, dict) else {}
        )
        raw_candidate = input_data.get("candidate")
        if isinstance(raw_candidate, dict):
            candidate: CandidateDict = cast(CandidateDict, raw_candidate)
        else:
            candidate = cast(CandidateDict, {})
        # Note: candidate may be legacy format dict, but extract_candidate_context handles both
        context = extract_candidate_context(candidate)

        # Store initial state
        state.setdefault("screen_id", input_data.get("screen_id"))
        state.setdefault("candidate", candidate)
        state.setdefault("role_spec_markdown", input_data.get("role_spec_markdown", ""))
        if "custom_instructions" not in state:
            state["custom_instructions"] = input_data.get("custom_instructions")
        state.update(context)

        self.logger.info(
            "%s Starting deep research for %s (%s at %s)",
            LOG_SEARCH,
            context["candidate_name"],
            context["current_title"],
            context["current_company"],
        )
        research = run_research(
            candidate_name=context["candidate_name"],
            current_title=context["current_title"],
            current_company=context["current_company"],
            linkedin_url=context["linkedin_url"],
            use_deep_research=settings.openai.use_deep_research,
        )
        # Store as dict using JSON mode to keep datetimes serializable
        state["research"] = research.model_dump(mode="json")
        return StepOutput(
            step_name="deep_research",
            executor_name="run_research",
            success=True,
            content={"citations": len(research.citations)},
        )

    def _quality_check_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        if run_context.session_state is None:
            run_context.session_state = {}

        state = run_context.session_state.get("workflow_data", {})
        research_data = state.get("research")
        if research_data is None:
            raise RuntimeError("Deep research step must run before quality check")

        # Reconstruct research object from dict if needed
        research = reconstruct_research(research_data)

        quality_ok = check_research_quality(research)
        state["quality_ok"] = quality_ok
        self.logger.info(
            "%s Research quality check for %s → %s",
            LOG_SEARCH,
            state.get("candidate_name", "candidate"),
            "pass" if quality_ok else "fail",
        )
        return StepOutput(
            step_name="quality_check",
            executor_name="check_research_quality",
            success=True,
            content={"quality_ok": quality_ok},
        )

    def _incremental_search_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        if run_context.session_state is None:
            run_context.session_state = {}

        state = run_context.session_state.get("workflow_data", {})
        research_data = state.get("research")
        if research_data is None:
            raise RuntimeError("Missing research payload before incremental search")
        if state.get("quality_ok"):
            self.logger.info(
                "%s Skipping incremental search for %s (quality threshold met)",
                LOG_SUCCESS,
                state.get("candidate_name", "candidate"),
            )
            return StepOutput(
                step_name="incremental_search",
                executor_name="run_incremental_search",
                success=True,
                content={"skipped": True},
            )

        self.logger.info(
            "%s Running incremental search for %s",
            LOG_SEARCH,
            state.get("candidate_name", "candidate"),
        )
        # Reconstruct research object from dict if needed
        research = reconstruct_research(research_data)

        merged_research = run_incremental_search(
            candidate_name=state.get("candidate_name", "candidate"),
            initial_research=research,
            quality_gaps=research.gaps,
            role_spec_markdown=state.get("role_spec_markdown", ""),
        )
        # Store as dict for JSON serialization (SqliteDb persistence)
        state["research"] = merged_research.model_dump(mode="json")
        return StepOutput(
            step_name="incremental_search",
            executor_name="run_incremental_search",
            success=True,
            content={"citations": len(merged_research.citations)},
        )

    def _assessment_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        if run_context.session_state is None:
            run_context.session_state = {}

        state = run_context.session_state.get("workflow_data", {})
        research_data = state.get("research")
        if research_data is None:
            raise RuntimeError("Missing research payload before assessment")

        # Reconstruct research object from dict if needed
        research = reconstruct_research(research_data)

        self.logger.info(
            "%s Starting assessment for %s",
            LOG_SEARCH,
            state.get("candidate_name", "candidate"),
        )
        assessment = assess_candidate(
            research=research,
            role_spec_markdown=state.get("role_spec_markdown", ""),
            custom_instructions=state.get("custom_instructions"),
        )
        # Store as dict for JSON serialization (SqliteDb persistence)
        state["assessment"] = assessment.model_dump(mode="json")
        self.logger.info(
            "%s Assessment complete for %s (overall_score=%s)",
            LOG_SUCCESS,
            state.get("candidate_name", "candidate"),
            assessment.overall_score,
        )
        return StepOutput(
            step_name="assessment",
            executor_name="assess_candidate",
            success=True,
            content={"assessment": assessment.model_dump(mode="json")},
        )
