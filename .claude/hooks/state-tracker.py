#!/usr/bin/env python3
"""
State Tracker for aidev V4.2 (Python Edition)
Parses Markdown documents with YAML frontmatter
Generates comprehensive state snapshot in .claude/logs/state.json
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Optional PyYAML for robust frontmatter parsing (graceful degradation)
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Paths
ROOT = Path.cwd()
SPEC_DIR = ROOT / "spec"
UNITS_DIR = SPEC_DIR / "units"
LOGS_DIR = ROOT / ".claude" / "logs"
STATE_FILE = LOGS_DIR / "state.json"

def safe_load_markdown(path: Path) -> Optional[Dict[str, Any]]:
    """Load Markdown file with YAML frontmatter"""
    if not path.exists():
        return None

    try:
        with open(path, 'r') as f:
            content = f.read()
    except Exception:
        return None

    # Extract frontmatter (between --- delimiters)
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not frontmatter_match:
        return {}

    frontmatter_text = frontmatter_match.group(1)

    if YAML_AVAILABLE:
        # Use PyYAML for robust parsing
        try:
            return yaml.safe_load(frontmatter_text) or {}
        except Exception:
            return {}
    else:
        # Fallback: simple key-value regex parsing
        data = {}
        for line in frontmatter_text.split('\n'):
            match = re.match(r'(\w+):\s*"?([^"]+)"?', line.strip())
            if match:
                key, value = match.groups()
                data[key] = value
        return data

def get_l1_status() -> Dict[str, Any]:
    """Check status of L1 documents (constitution, prd, spec)"""
    docs = {
        "constitution": SPEC_DIR / "constitution.md",
        "prd": SPEC_DIR / "prd.md",
        "spec": SPEC_DIR / "spec.md"
    }

    status = {}
    for name, path in docs.items():
        if path.exists():
            meta = safe_load_markdown(path)
            status[name] = {
                "exists": True,
                "version": meta.get('version') if meta else None,
                "updated": meta.get('updated') if meta else None
            }
        else:
            status[name] = {"exists": False}

    return status

def parse_status_from_markdown(content: str) -> Dict[str, Any]:
    """Parse status section from Markdown body"""
    info = {}

    # Find Status section
    status_match = re.search(r'##\s+Status\s*\n(.*?)(?=\n##[^#]|\Z)', content, re.DOTALL)
    if not status_match:
        return info

    status_section = status_match.group(1)

    # Parse progress
    progress_match = re.search(r'\*\*Progress:\*\*\s*(\d+)%', status_section)
    if progress_match:
        info['progress'] = int(progress_match.group(1))

    # Parse coverage
    coverage_match = re.search(r'\*\*Coverage:\*\*\s*([\d.]+)%?', status_section)
    if coverage_match:
        info['coverage'] = float(coverage_match.group(1)) / 100 if '.' in coverage_match.group(1) else float(coverage_match.group(1))

    # Parse blockers
    blockers_match = re.search(r'\*\*Blockers:\*\*\s*(.+?)(?=\n\*\*|\Z)', status_section, re.DOTALL)
    if blockers_match:
        blockers_text = blockers_match.group(1).strip()
        if blockers_text.lower() not in ['none', 'n/a', '']:
            info['blockers'] = [b.strip() for b in blockers_text.split(',')]

    return info

def parse_tasks_from_markdown(content: str) -> Dict[str, Any]:
    """Parse tasks from Markdown body"""
    tasks = {}

    # Find Tasks section
    tasks_match = re.search(r'##\s+Tasks\s*\n(.*?)(?=\n##[^#]|\Z)', content, re.DOTALL)
    if not tasks_match:
        return tasks

    tasks_section = tasks_match.group(1)

    # Find all task headers (### TK-##)
    task_blocks = re.split(r'###\s+(TK-\d+)', tasks_section)[1:]  # Skip first empty element

    for i in range(0, len(task_blocks), 2):
        if i + 1 >= len(task_blocks):
            break

        task_id = task_blocks[i].strip()
        task_content = task_blocks[i + 1]

        # Parse task fields
        title_match = re.search(r'\*\*Title:\*\*\s*(.+)', task_content)
        status_match = re.search(r'\*\*Status:\*\*\s*(\w+)', task_content)
        completed_match = re.search(r'\*\*Completed:\*\*\s*(\d{4}-\d{2}-\d{2})', task_content)

        tasks[task_id] = {
            "title": title_match.group(1).strip() if title_match else "Unknown",
            "status": status_match.group(1).strip() if status_match else "unknown",
            "completed": completed_match.group(1) if completed_match else None
        }

    return tasks

def get_units_status() -> Dict[str, Any]:
    """Get status of all units"""
    units = {}

    if not UNITS_DIR.exists():
        return units

    for unit_dir in sorted(UNITS_DIR.iterdir()):
        if not unit_dir.is_dir():
            continue

        unit_name = unit_dir.name
        unit_status = {
            "design_exists": False,
            "plan_exists": False,
            "tasks": {},
            "blockers": [],
            "actual_coverage": None
        }

        # Check design
        design_path = unit_dir / "design.md"
        if design_path.exists():
            unit_status["design_exists"] = True

        # Check plan and parse tasks
        plan_path = unit_dir / "plan.md"
        if plan_path.exists():
            unit_status["plan_exists"] = True

            try:
                with open(plan_path, 'r') as f:
                    plan_content = f.read()

                # Parse tasks from Markdown body
                unit_status['tasks'] = parse_tasks_from_markdown(plan_content)

                # Parse status section from Markdown body
                status_info = parse_status_from_markdown(plan_content)
                unit_status['blockers'] = status_info.get('blockers', [])
                unit_status['actual_coverage'] = status_info.get('coverage', None)

            except Exception:
                pass

        units[unit_name] = unit_status

    return units

def parse_interfaces_from_markdown(content: str) -> Set[str]:
    """Parse interface names from Markdown body (### [interface_name] sections)"""
    interfaces = set()

    # Find Interfaces section
    interfaces_match = re.search(r'##\s+Interfaces\s*\n(.*?)(?=\n##[^#]|\Z)', content, re.DOTALL)
    if not interfaces_match:
        return interfaces

    interfaces_section = interfaces_match.group(1)

    # Find all ### headers with optional brackets
    interface_matches = re.finditer(r'###\s+(?:\[(\w+)\]|(\w+))', interfaces_section)
    for match in interface_matches:
        interface_name = match.group(1) or match.group(2)
        if interface_name:
            interfaces.add(interface_name)

    return interfaces

def parse_entities_from_markdown(content: str) -> Set[str]:
    """Parse entity names from Markdown body (### Entity: [EntityName] sections)"""
    entities = set()

    # Find Data Model section
    data_model_match = re.search(r'##\s+Data Model\s*\n(.*?)(?=\n##[^#]|\Z)', content, re.DOTALL)
    if not data_model_match:
        return entities

    data_model_section = data_model_match.group(1)

    # Find all ### Entity: headers
    entity_matches = re.finditer(r'###\s+Entity:\s+(?:\[(\w+)\]|(\w+))', data_model_section)
    for match in entity_matches:
        entity_name = match.group(1) or match.group(2)
        if entity_name:
            entities.add(entity_name)

    return entities

def validate_alignment() -> Dict[str, Any]:
    """Validate document alignment and references"""
    issues = []

    # Load spec content
    spec_path = SPEC_DIR / "spec.md"
    if not spec_path.exists():
        return {"valid": True, "issues": []}

    try:
        with open(spec_path, 'r') as f:
            spec_content = f.read()
    except Exception:
        return {"valid": True, "issues": []}

    # Parse interfaces and entities from Markdown body
    spec_interfaces = parse_interfaces_from_markdown(spec_content)
    spec_entities = parse_entities_from_markdown(spec_content)

    # Check each unit's design references
    if UNITS_DIR.exists():
        for unit_dir in UNITS_DIR.iterdir():
            if not unit_dir.is_dir():
                continue

            design = safe_load_markdown(unit_dir / "design.md")
            if not design:
                continue

            # Check interface references
            interfaces_touched = design.get('interfaces_touched', [])
            if isinstance(interfaces_touched, list):
                for iface_ref in interfaces_touched:
                    if iface_ref and iface_ref not in spec_interfaces:
                        issues.append({
                            "type": "invalid_reference",
                            "unit": unit_dir.name,
                            "file": "design.md",
                            "message": f"References interface '{iface_ref}' which doesn't exist in spec.md"
                        })

            # Check entity references
            data_shapes = design.get('data_shapes', [])
            if isinstance(data_shapes, list):
                for entity_ref in data_shapes:
                    if entity_ref and entity_ref not in spec_entities:
                        issues.append({
                            "type": "invalid_reference",
                            "unit": unit_dir.name,
                            "file": "design.md",
                            "message": f"References entity '{entity_ref}' which doesn't exist in spec.md"
                        })

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }

def check_constitution_compliance() -> Dict[str, Any]:
    """Check compliance with constitution quality bars"""
    violations = []

    constitution = safe_load_markdown(SPEC_DIR / "constitution.md")
    if not constitution:
        return {"violations": []}

    quality_bars = constitution.get('quality_bars', {})
    coverage_target = quality_bars.get('coverage_target', 0.85) if isinstance(quality_bars, dict) else 0.85

    # Get actual coverage from unit status
    units_status = get_units_status()
    for unit_name, unit_data in units_status.items():
        actual_coverage = unit_data.get('actual_coverage')
        # Only report violation if coverage is explicitly set and below target
        if actual_coverage is not None and actual_coverage < coverage_target:
            violations.append({
                "type": "coverage",
                "unit": unit_name,
                "actual": actual_coverage,
                "required": coverage_target
            })

    return {"violations": violations}

def generate_state() -> Dict[str, Any]:
    """Generate complete state snapshot"""
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "l1_status": get_l1_status(),
        "units": get_units_status(),
        "alignment": validate_alignment(),
        "constitution_compliance": check_constitution_compliance()
    }

def main():
    """Main entry point"""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        state = generate_state()
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        print("✅ State updated")
    except Exception as e:
        print(f"❌ State tracker failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
