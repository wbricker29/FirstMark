#!/usr/bin/env python3
"""Enhanced validation script for Claude skills."""

import json
import re
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_LINES = 500
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED_WORDS = {"anthropic", "claude"}
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def _simple_frontmatter_parse(frontmatter: str) -> dict:
    """Fallback parser when PyYAML is unavailable."""

    result = {}
    current_key = None
    current_lines = []

    def flush():
        nonlocal current_key, current_lines
        if current_key is not None:
            result[current_key] = "\n".join(current_lines).strip()
            current_key = None
            current_lines = []

    for raw_line in frontmatter.splitlines():
        if not raw_line.strip():
            if current_key is not None:
                current_lines.append("")
            continue
        if raw_line.lstrip().startswith("#"):
            continue
        if not raw_line.startswith(" ") and ":" in raw_line:
            flush()
            key, value = raw_line.split(":", 1)
            current_key = key.strip()
            current_lines = [value.strip()]
        elif current_key is not None:
            current_lines.append(raw_line.strip())
    flush()
    return result


def _parse_frontmatter(frontmatter: str) -> dict:
    if yaml is not None:
        data = yaml.safe_load(frontmatter)
        if not isinstance(data, dict):
            raise ValueError("Frontmatter must be a YAML mapping")
        return data
    return _simple_frontmatter_parse(frontmatter)


def _extract_frontmatter(content: str):
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None, None
    try:
        data = _parse_frontmatter(match.group(1))
    except Exception as exc:  # pragma: no cover - defensive
        raise ValueError(f"Unable to parse frontmatter: {exc}") from exc
    return data, match.group(1)


def _validate_name(skill_name: str, directory_name: str):
    errors = []
    if not skill_name:
        errors.append("Frontmatter 'name' cannot be empty")
        return errors
    if len(skill_name) > MAX_NAME_LENGTH:
        errors.append(f"Skill name '{skill_name}' exceeds {MAX_NAME_LENGTH} characters")
    if not NAME_PATTERN.match(skill_name):
        errors.append(
            "Name must be lowercase hyphen-case (letters, numbers, hyphen separators)"
        )
    if any(reserved in skill_name for reserved in RESERVED_WORDS):
        errors.append("Name cannot contain reserved words 'anthropic' or 'claude'")
    if skill_name != directory_name:
        errors.append(
            f"Directory name '{directory_name}' must match frontmatter name '{skill_name}'"
        )
    return errors


def _validate_description(description: str):
    errors = []
    if not description or not description.strip():
        errors.append("Frontmatter 'description' cannot be empty")
        return errors
    if len(description.strip()) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            "Description exceeds 1024 characters. Keep it concise and actionable."
        )
    if "<" in description or ">" in description:
        errors.append("Description cannot contain angle brackets (< or >)")
    return errors


def _find_skill_rules_file(skill_path: Path) -> Optional[Path]:
    candidates = [
        skill_path / "skill-rules.json",
        skill_path.parent / "skill-rules.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _ensure_string_list(values, field_name: str):
    if values is None:
        return []
    if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
        return [f"'{field_name}' must be a list of strings"]
    return []


def _validate_skill_rules(skill_path: Path, skill_name: str):
    errors: list[str] = []
    warnings: list[str] = []
    skill_rules_path = _find_skill_rules_file(skill_path)
    if not skill_rules_path:
        return errors, warnings

    try:
        data = json.loads(skill_rules_path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"skill-rules.json is not valid JSON: {exc}")
        return errors, warnings

    skills_section = None
    if isinstance(data, dict) and "skills" in data and isinstance(data["skills"], dict):
        skills_section = data["skills"]
    elif isinstance(data, dict):
        skills_section = data

    if not isinstance(skills_section, dict):
        errors.append("skill-rules.json must contain a skills mapping")
        return errors, warnings

    rule = skills_section.get(skill_name)
    if rule is None:
        # Only warn if the file lives inside the skill directory itself.
        if skill_rules_path.parent == skill_path:
            warnings.append(
                f"skill-rules.json does not declare '{skill_name}'. Add a rule when creating Claude Code guardrails."
            )
        return errors, warnings

    if not isinstance(rule, dict):
        errors.append("Skill rule definition must be an object")
        return errors, warnings

    allowed_types = {"guardrail", "domain"}
    allowed_enforcement = {"block", "suggest", "warn"}
    allowed_priority = {"critical", "high", "medium", "low"}

    if rule.get("type") not in allowed_types:
        errors.append("skill-rules type must be 'guardrail' or 'domain'")
    if rule.get("enforcement") not in allowed_enforcement:
        errors.append("enforcement must be one of block/suggest/warn")
    if rule.get("priority") not in allowed_priority:
        errors.append("priority must be critical/high/medium/low")

    if rule.get("enforcement") == "block" and not rule.get("blockMessage"):
        errors.append("block enforcement requires a non-empty blockMessage")

    prompt_triggers = rule.get("promptTriggers")
    if prompt_triggers is not None:
        if not isinstance(prompt_triggers, dict):
            errors.append("promptTriggers must be an object")
        else:
            errors.extend(
                _ensure_string_list(
                    prompt_triggers.get("keywords"), "promptTriggers.keywords"
                )
            )
            errors.extend(
                _ensure_string_list(
                    prompt_triggers.get("intentPatterns"),
                    "promptTriggers.intentPatterns",
                )
            )

    file_triggers = rule.get("fileTriggers")
    if file_triggers is not None:
        if not isinstance(file_triggers, dict):
            errors.append("fileTriggers must be an object")
        else:
            errors.extend(
                _ensure_string_list(
                    file_triggers.get("pathPatterns"), "fileTriggers.pathPatterns"
                )
            )
            if file_triggers.get("pathPatterns") is None:
                errors.append(
                    "fileTriggers.pathPatterns is required when fileTriggers is present"
                )
            errors.extend(
                _ensure_string_list(
                    file_triggers.get("pathExclusions"), "fileTriggers.pathExclusions"
                )
            )
            errors.extend(
                _ensure_string_list(
                    file_triggers.get("contentPatterns"), "fileTriggers.contentPatterns"
                )
            )
            create_only = file_triggers.get("createOnly")
            if create_only is not None and not isinstance(create_only, bool):
                errors.append("fileTriggers.createOnly must be a boolean if provided")

    skip_conditions = rule.get("skipConditions")
    if skip_conditions is not None and not isinstance(skip_conditions, dict):
        errors.append("skipConditions must be an object when provided")

    return errors, warnings


def validate_skill(skill_path):
    """Validate a skill directory and return (is_valid, message)."""

    path = Path(skill_path)
    errors: list[str] = []
    warnings: list[str] = []

    if not path.exists():
        return False, f"Skill path not found: {path}"
    if not path.is_dir():
        return False, "Skill path must be a directory"

    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    try:
        frontmatter, _raw = _extract_frontmatter(content)
    except ValueError as exc:
        return False, str(exc)

    if not frontmatter:
        return False, "No YAML frontmatter found"

    if "name" not in frontmatter:
        errors.append("Frontmatter must include a 'name' field")
    if "description" not in frontmatter:
        errors.append("Frontmatter must include a 'description' field")

    if not errors:
        errors.extend(
            _validate_name(str(frontmatter.get("name", "")).strip(), path.name)
        )
        errors.extend(_validate_description(str(frontmatter.get("description", ""))))

    line_count = len(content.rstrip("\n").splitlines())
    if line_count > MAX_SKILL_LINES:
        errors.append(
            f"SKILL.md has {line_count} lines. Keep it under {MAX_SKILL_LINES} lines."
        )

    sr_errors, sr_warnings = _validate_skill_rules(
        path, str(frontmatter.get("name", ""))
    )
    errors.extend(sr_errors)
    warnings.extend(sr_warnings)

    if errors:
        return False, "Validation failed:\n- " + "\n- ".join(errors)

    message = "Skill is valid!"
    if warnings:
        message += "\nWarnings:\n- " + "\n- ".join(warnings)
    return True, message


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run python scripts/quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
