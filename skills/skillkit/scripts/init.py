#!/usr/bin/env python3
"""
Unified initializer for skills and subagents.

Usage:
    python init.py skill <name> --path <path> [--mode fast|full]
    python init.py subagent <name> --path <path>

Replaces: init_skill.py, init_subagent.py
"""

import argparse
import sys
from pathlib import Path
from enum import Enum



class WorkflowMode(Enum):
    """Workflow mode for skill creation."""
    FAST = "fast"
    FULL = "full"



SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Delete this section when done.]

## [TODO: Replace with the first main section]

[TODO: Add content here]

## Resources

This skill includes example resource directories:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly.

### references/
Documentation and reference material for Claude's context.

### assets/
Files not intended to be loaded into context (templates, images, etc.).

---

**Any unneeded directories can be deleted.**
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

Replace with actual implementation or delete if not needed.
"""

def main():
    print("This is an example script for {skill_name}")

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files or delete if not needed.

Asset files are NOT intended to be loaded into context.
"""

SUBAGENT_TEMPLATE = """---
name: {subagent_name}
description: "[TODO: Clear description of what this subagent does and when to use it. Include specific scenarios that trigger delegation.]"
subagent_type: [TODO: Choose one]
# Options: general-purpose, code-reviewer, typescript-pro, flutter-expert,
#          red-team, qa-expert, seo-manager, creative-copywriter,
#          decision-maker, research, custom

tools:
  - Read
  # - Write
  # - Edit
  # - Bash
  # - Glob
  # - Grep
  # - Skill
---

You are a specialist in [TODO: domain expertise]. Your purpose is to [TODO: main purpose].

## Your Capabilities

**Core Expertise:**
- [TODO: Capability 1]
- [TODO: Capability 2]

**When to Invoke You:**
- [TODO: Trigger condition 1]
- [TODO: Trigger condition 2]

## Output Format

Always structure your response as:

```
## Summary
[Brief overview of what was done]

## Details
[Detailed explanation]

## Recommendations
[Actionable next steps]
```

---

**IMPORTANT:** Replace all [TODO] sections before using this subagent.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def validate_skill_name(name: str) -> tuple[bool, str]:
    """Validate skill/subagent name format."""
    if not name or not name.strip():
        return False, "Name cannot be empty or whitespace"
    name = name.strip()
    if len(name) > 40:
        return False, "Name must be 40 characters or less"
    if not all(c.islower() or c.isdigit() or c == '-' for c in name):
        return False, "Name must contain only lowercase letters, digits, and hyphens"
    if name.startswith('-') or name.endswith('-'):
        return False, "Name cannot start or end with a hyphen"
    if '--' in name:
        return False, "Name cannot contain consecutive hyphens"
    return True, ""


def prompt_for_mode():
    """Ask user for workflow mode."""
    print("\n" + "=" * 60)
    print("WORKFLOW MODE SELECTION")
    print("=" * 60)
    print("\nFAST Mode (12 steps)")
    print("  - Structural validation only")
    print("  - Quick iteration")
    print("\nFULL Mode (15 steps)")
    print("  - Structural + behavioral validation")
    print("  - TDD pressure testing")
    print("\n" + "-" * 60)

    while True:
        choice = input("\nSelect mode (1=fast, 2=full) [1]: ").strip() or "1"
        if choice == "1":
            return WorkflowMode.FAST
        if choice == "2":
            return WorkflowMode.FULL
        print("Invalid choice. Enter 1 or 2.")


def init_skill(skill_name: str, path: str, mode: WorkflowMode) -> Path | None:
    """Initialize a new skill directory."""
    is_valid, error_msg = validate_skill_name(skill_name)
    if not is_valid:
        print(f"Error: Invalid skill name '{skill_name}': {error_msg}")
        return None

    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    # Create mode marker
    mode_file = skill_dir / '.skillkit-mode'
    mode_file.write_text(mode.value)

    # Create SKILL.md
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    if mode == WorkflowMode.FULL:
        skill_content += """

## Behavioral Validation

### RED Phase - Baseline Failures
<!-- Document rationalizations found WITHOUT skill -->

### GREEN Phase - Verification
<!-- Confirm compliance WITH skill -->

### Rationalization Table
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks |
| "I'll test after" | Tests-after proves nothing |

## Pressure Test Results
- [ ] Time pressure: __
- [ ] Sunk cost pressure: __
- [ ] Authority pressure: __
- [ ] Exhaustion pressure: __
- [ ] Combined pressure: __

**Final Behavioral Score:** __/10
"""

    skill_md_path = skill_dir / 'SKILL.md'
    skill_md_path.write_text(skill_content)
    print("Created SKILL.md")

    # Create resource directories
    try:
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("Created scripts/example.py")

        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("Created references/api_reference.md")

        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("Created assets/example_asset.txt")
    except Exception as e:
        print(f"Error creating resource directories: {e}")
        return None

    print(f"\nSkill '{skill_name}' initialized successfully at {skill_dir}")
    return skill_dir


def init_subagent(subagent_name: str, path: str) -> Path | None:
    """Initialize a new subagent file."""
    is_valid, error_msg = validate_skill_name(subagent_name)
    if not is_valid:
        print(f"Error: Invalid subagent name '{subagent_name}': {error_msg}")
        return None

    target_dir = Path(path).expanduser().resolve()
    subagent_file = target_dir / f"{subagent_name}.md"

    if subagent_file.exists():
        print(f"Error: Subagent file already exists: {subagent_file}")
        return None

    if target_dir.exists() and not target_dir.is_dir():
        print(f"Error: Target path exists but is not a directory: {target_dir}")
        return None

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"Error: Permission denied creating directory: {target_dir}")
        return None
    except OSError as e:
        print(f"Error creating directory: {e}")
        return None

    try:
        subagent_file.write_text(SUBAGENT_TEMPLATE.format(subagent_name=subagent_name))
        print(f"Created subagent file: {subagent_file}")
    except PermissionError:
        print(f"Error: Permission denied writing file: {subagent_file}")
        return None
    except OSError as e:
        print(f"Error creating subagent file: {e}")
        return None

    print(f"\nSubagent '{subagent_name}' initialized successfully")
    print("\nIMPORTANT: This is a template with [TODO] placeholders.")
    print("   Before using this subagent, you MUST:")
    print("   1. Replace all [TODO] sections with specific content")
    print("   2. Add concrete examples with <example> tags")
    print(f"\n   Edit the file: {subagent_file}")

    return subagent_file


def main():
    parser = argparse.ArgumentParser(
        description='Initialize skills and subagents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  init.py skill my-new-skill --path skills/
  init.py skill my-api-helper --path . --mode full
  init.py subagent code-reviewer --path ~/.claude/agents

Name requirements:
  - Hyphen-case (e.g., 'data-analyzer')
  - Lowercase letters, digits, hyphens only
  - Max 40 characters
  - No leading/trailing/consecutive hyphens
""")

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Skill subcommand
    skill_parser = subparsers.add_parser('skill', help='Initialize a new skill')
    skill_parser.add_argument('name', help='Name of the skill')
    skill_parser.add_argument('--path', default='.', help='Path for skill directory')
    skill_parser.add_argument('--mode', choices=['fast', 'full'], help='Workflow mode')

    # Subagent subcommand
    subagent_parser = subparsers.add_parser('subagent', help='Initialize a new subagent')
    subagent_parser.add_argument('name', help='Name of the subagent')
    subagent_parser.add_argument('--path', default='.', help='Path for subagent file')

    args = parser.parse_args()

    if args.command == 'skill':
        mode = WorkflowMode(args.mode) if args.mode else WorkflowMode.FAST
        result = init_skill(args.name, args.path, mode)
        sys.exit(0 if result else 1)
    elif args.command == 'subagent':
        result = init_subagent(args.name, args.path)
        sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
