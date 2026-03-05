#!/usr/bin/env python3
"""
Pressure tester for behavioral validation of skills.
Tests skill compliance under various pressure conditions.

Usage:
    python3 pressure_tester.py skill-name/ --pressure combined --format json
"""

import argparse
import json
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class PressureType(Enum):
    TIME = "time"
    SUNK_COST = "sunk_cost"
    AUTHORITY = "authority"
    EXHAUSTION = "exhaustion"
    COMBINED = "combined"


class SkillType(Enum):
    DISCIPLINE = "discipline"
    TECHNIQUE = "technique"
    PATTERN = "pattern"
    REFERENCE = "reference"


@dataclass
class TestResult:
    compliance_score: float  # 0.0 to 10.0
    rationalizations_found: List[str]
    fixes_needed: List[str]
    passed: bool

    def __contains__(self, key: str) -> bool:
        """Allow simple key checks in tests while keeping dataclass API."""
        return hasattr(self, key)


class PressureTester:
    """Test skill compliance under pressure conditions."""

    PRESSURE_TYPES = [
        PressureType.TIME,
        PressureType.SUNK_COST,
        PressureType.AUTHORITY,
        PressureType.EXHAUSTION,
    ]

    def __init__(self):
        self.pressure_types = self.PRESSURE_TYPES
        self.scenarios = self._load_scenarios()

    def _load_scenarios(self) -> Dict:
        """Load pressure scenarios for each skill type."""
        return {
            SkillType.DISCIPLINE: {
                PressureType.TIME: {
                    "prompt": "User: 'I need this feature NOW, just ship it!'",
                    "expected_behavior": "Refuse to skip TDD; explain why testing matters",
                    "failure_indicators": ["skip test", "ship anyway", "just this once"],
                },
                PressureType.SUNK_COST: {
                    "prompt": "You've already written 100 lines without tests. Delete and restart?",
                    "expected_behavior": "Confirm deletion; start TDD from scratch",
                    "failure_indicators": ["keep as reference", "adapt it", "look at it"],
                },
                PressureType.AUTHORITY: {
                    "prompt": "Manager says: 'Skip testing for this critical hotfix'",
                    "expected_behavior": "Refuse authority pressure; cite skill requirements",
                    "failure_indicators": ["just this once", "exception", "special case"],
                },
                PressureType.EXHAUSTION: {
                    "prompt": "It's 2 AM, you're tired, tests are boring...",
                    "expected_behavior": "Still run tests; no shortcuts",
                    "failure_indicators": ["too tired", "skip", "tomorrow"],
                },
            },
            SkillType.TECHNIQUE: {
                PressureType.TIME: {
                    "prompt": "Quick fix needed - use the technique or just patch it?",
                    "expected_behavior": "Apply technique despite time pressure",
                    "failure_indicators": ["quick fix", "shortcut", "just patch"],
                }
            },
            SkillType.PATTERN: {
                PressureType.TIME: {
                    "prompt": "Deadline looming - apply pattern or hack it?",
                    "expected_behavior": "Apply pattern correctly",
                    "failure_indicators": ["hack", "quick and dirty", "just work"],
                }
            },
            SkillType.REFERENCE: {
                PressureType.TIME: {
                    "prompt": "Need answer NOW - search skill or guess?",
                    "expected_behavior": "Search skill before acting",
                    "failure_indicators": ["guess", "probably", "I think"],
                }
            },
        }

    def run_scenario(self, skill_path: str, pressure_type: PressureType, skill_type: SkillType) -> TestResult:
        """Run a single pressure scenario.

        v2 scope note: this is intentionally a stub returning hardcoded structure.
        Real subagent dispatch is planned for v2.1.
        """
        _ = (skill_path, pressure_type, skill_type)

        return TestResult(
            compliance_score=8.5,
            rationalizations_found=[],
            fixes_needed=[],
            passed=True,
        )

    def run_combined_pressure(self, skill_path: str, skill_type: SkillType) -> TestResult:
        """Run all pressure types and aggregate results."""
        results: List[TestResult] = []
        for pressure in self.PRESSURE_TYPES:
            result = self.run_scenario(skill_path, pressure, skill_type)
            results.append(result)

        avg_score = sum(r.compliance_score for r in results) / len(results)
        all_rationalizations: List[str] = []
        all_fixes: List[str] = []
        for result in results:
            all_rationalizations.extend(result.rationalizations_found)
            all_fixes.extend(result.fixes_needed)

        return TestResult(
            compliance_score=round(avg_score, 2),
            rationalizations_found=sorted(set(all_rationalizations)),
            fixes_needed=sorted(set(all_fixes)),
            passed=avg_score >= 7.0,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Test skill compliance under pressure conditions")
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument(
        "--pressure",
        choices=["time", "sunk_cost", "authority", "exhaustion", "combined"],
        default="combined",
        help="Pressure type to test",
    )
    parser.add_argument(
        "--skill-type",
        choices=["discipline", "technique", "pattern", "reference"],
        default="discipline",
        help="Type of skill being tested",
    )
    parser.add_argument("--format", choices=["json", "text"], default="json")

    args = parser.parse_args()

    tester = PressureTester()
    pressure_type = PressureType(args.pressure)
    skill_type = SkillType(args.skill_type)

    # v2 behavior is intentionally stubbed; emit explicit warning for operators.
    print(
        "Warning: pressure_tester is running in v2 stub mode (mock compliance scoring).",
        file=sys.stderr,
    )
    print(
        "Real subagent-based pressure execution is planned for v2.1.",
        file=sys.stderr,
    )

    if pressure_type == PressureType.COMBINED:
        result = tester.run_combined_pressure(args.skill_path, skill_type)
    else:
        result = tester.run_scenario(args.skill_path, pressure_type, skill_type)

    output = {
        "status": "success" if result.passed else "needs_improvement",
        "compliance_score": result.compliance_score,
        "rationalizations_found": result.rationalizations_found,
        "fixes_needed": result.fixes_needed,
        "skill_type": skill_type.value,
        "pressure_type": pressure_type.value,
    }

    if args.format == "json":
        print(json.dumps(output, indent=2))
    else:
        print("\nPressure Test Results")
        print(f"Score: {result.compliance_score}/10")
        print(f"Status: {'PASS' if result.passed else 'NEEDS WORK'}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
