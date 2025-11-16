  ✅ RESOLVED: How We'll Use Agno

  1. Agent Instantiation ✅

  Answer: Create agents on-demand, per-request is fine.

  From candidate_analyser/main.py:
  # Created inside the button click handler (lines 111-134, 180-203)
  if submit:
      agent = Agent(
          model=Nebius(id=st.session_state.model_id, ...),
          tools=[...],
          ...
      )
      response = agent.run(query, stream=True)

  For us:
  - Agents don't maintain state on the object itself
  - State is managed through session_state and persisted to database
  - Safe to create agents per-request or at module level - both work
  - Recommendation: Module-level for performance, but either is fine

  2. Audit Trail & Logging ✅

  Answer: Use stream_events=True to capture everything.

  From workflows docs:
  # Get all execution details
  response = agent.arun(prompt, stream=True, stream_events=True)

  async for event in response:
      if event.event == RunEvent.tool_call_started:
          print(f"TOOL: {event.tool.tool_name}")
          print(f"ARGS: {event.tool.tool_args}")
      if event.event == RunEvent.tool_call_completed:
          print(f"RESULT: {event.tool.result}")

  Events captured:
  - run_started, run_completed
  - tool_call_started, tool_call_completed
  - run_content (streaming content)
  - Tool names, args, results - everything!

  For audit trail: Store these events in Airtable Workflows table.

  3. Streaming + Structured Outputs ✅

  Answer: YES, they work together perfectly!

  From the docs:
  agent = Agent(
      model=OpenAIChat(id="gpt-5-mini"),
      output_schema=ExecutiveResearchResult,  # Pydantic model
  )

  # Stream AND get structured output
  stream = agent.arun(prompt, stream=True, stream_events=True)

  # Consume stream - last item is the structured output
  final_response = None
  async for event in stream:
      final_response = event  # Last one has the structured output

  assert isinstance(final_response.content, ExecutiveResearchResult)

  Key insight: Structured output arrives as final RunContent event in stream.

  4. Error Handling ✅

  Answer: Built-in retry with exponential backoff.

  agent = Agent(
      model=OpenAIResponses(id="gpt-5-mini"),
      exponential_backoff=True,  # Auto-retry on provider errors
      retries=2,
      retry_delay=1,
  )

  Custom error handling:
  from agno.exceptions import RetryAgentRun, StopAgentRun

  def my_tool(run_context: RunContext):
      if error_condition:
          raise RetryAgentRun("Try again with different instructions")
