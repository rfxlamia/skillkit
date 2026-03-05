#!/usr/bin/env python3
"""
Auto-generate comprehensive test scenarios for skills.
Based on skill description and validation requirements.

v1.2 Update: Parameter standardization
- Renamed --format to --test-format (test framework choice)
- Renamed --output to --format (output style)
- Backward compatibility maintained for --output (deprecated)

References: File 12 (testing best practices)
"""

import re
import json
import argparse
import warnings
import sys
from pathlib import Path
from typing import List, Dict, Optional

class TestGenerator:
    """Generate test scenarios from skill description."""
    
    def __init__(
        self,
        skill_path: str,
        coverage: str = 'standard',
        test_format: str = 'pytest',
        output_format: str = 'text',
        behavioral: bool = False
    ):
        """
        Initialize test generator.
        
        Args:
            skill_path: Path to skill directory
            coverage: 'basic', 'standard', or 'comprehensive'
            test_format: 'pytest', 'unittest', or 'plain'
            output_format: 'text' or 'json' (agent-layer)
        
        References: File 12 (testing best practices)
        """
        self.skill_path = Path(skill_path)
        self.coverage = coverage
        self.test_format = test_format
        self.output_format = output_format
        self.skill_md_content = None
        self.behavioral = behavioral
        self.skill_name = None
        self.capabilities = []
        self.test_scenarios = []
    
    # ========== PARSING ==========
    
    def parse_skill_description(self) -> Dict:
        """
        Parse SKILL.md to extract testable capabilities.
        
        Extracts:
        - Skill name (from frontmatter)
        - Main capabilities (from description)
        - Trigger conditions (WHEN clauses)
        - Example usages (if present)
        
        Returns:
            Dict with parsed information
        
        Raises:
            FileNotFoundError: If SKILL.md doesn't exist
        
        References: File 02 (description structure)
        """
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            raise FileNotFoundError(f"SKILL.md not found in {self.skill_path}")
        
        with open(skill_md, encoding='utf-8') as f:
            self.skill_md_content = f.read()
        
        # Parse YAML frontmatter
        frontmatter = self._extract_frontmatter()
        self.skill_name = frontmatter.get('name', 'unknown')
        
        # Parse capabilities
        description = frontmatter.get('description', '')
        self.capabilities = self._extract_capabilities(description, self.skill_md_content)
        
        return {
            'name': self.skill_name,
            'capabilities': self.capabilities,
            'description': description
        }
    
    def _extract_frontmatter(self) -> Dict:
        """
        Extract YAML frontmatter from SKILL.md.
        
        Returns:
            Dict with frontmatter key-value pairs
        """
        pattern = r'^---\n(.*?)\n---'
        match = re.search(pattern, self.skill_md_content, re.DOTALL)
        if not match:
            return {}
        
        # Simple YAML parsing (key: value)
        frontmatter = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"\'')
        
        return frontmatter
    
    def _extract_capabilities(self, description: str, content: str) -> List[str]:
        """
        Extract individual capabilities from description and content.
        
        Looks for:
        - Bulleted capabilities in description
        - WHEN/IF trigger clauses
        - Section headers indicating features
        
        Args:
            description: Skill description from frontmatter
            content: Full SKILL.md content
        
        Returns:
            List of capability descriptions
        """
        capabilities = []
        
        # Extract from description bullets
        for line in description.split('\n'):
            if line.strip().startswith(('-', '*', 'â€¢')):
                cap = line.strip().lstrip('-*â€¢ ')
                if cap and len(cap) > 10:  # Meaningful capability
                    capabilities.append(cap)
        
        # Extract WHEN clauses
        when_pattern = r'(?:when|if|for)\s+(.{20,100})'
        for match in re.finditer(when_pattern, content, re.IGNORECASE):
            cap = match.group(1).strip()
            if cap not in capabilities:
                capabilities.append(cap)
        
        # If no capabilities found, use generic
        if not capabilities:
            capabilities = ["Basic functionality"]
        
        return capabilities[:10]  # Limit to 10 capabilities
    
    # ========== TEST SCENARIO GENERATION ==========
    
    def generate_test_scenarios(self) -> List[Dict]:
        """
        Generate test scenarios based on coverage level.
        
        Returns:
            List of test scenario dicts with:
            - description: What to test
            - priority: P0 (critical), P1 (high), P2 (medium)
            - category: functional, edge_case, error_handling
            - expected_result: Expected outcome
        
        References: File 12 (test prioritization)
        """
        scenarios = []
        
        # P0: Critical functional tests (always included)
        scenarios.extend(self._generate_functional_tests())
        
        if self.coverage in ['standard', 'comprehensive']:
            # P1: Edge cases
            scenarios.extend(self._generate_edge_case_tests())
        
        if self.coverage == 'comprehensive':
            # P2: Error handling and performance
            scenarios.extend(self._generate_error_tests())
            scenarios.extend(self._generate_performance_tests())
        
        self.test_scenarios = scenarios
        return scenarios
    
    def _generate_functional_tests(self) -> List[Dict]:
        """Generate P0 critical functional tests."""
        tests = []
        
        # One functional test per capability
        for cap in self.capabilities:
            tests.append({
                'description': f"Test {cap}",
                'priority': 'P0',
                'category': 'functional',
                'expected_result': f"Skill successfully handles: {cap}",
                'test_data': 'valid_input'
            })
        
        # Always test basic invocation
        if not any('invocation' in t['description'].lower() for t in tests):
            tests.insert(0, {
                'description': "Test basic skill invocation",
                'priority': 'P0',
                'category': 'functional',
                'expected_result': "Skill loads and responds to trigger",
                'test_data': 'minimal_valid'
            })
        
        return tests
    
    def _generate_edge_case_tests(self) -> List[Dict]:
        """Generate P1 edge case tests."""
        return [
            {
                'description': "Test with minimal input",
                'priority': 'P1',
                'category': 'edge_case',
                'expected_result': "Graceful handling of minimal valid input",
                'test_data': 'minimal'
            },
            {
                'description': "Test with maximum/complex input",
                'priority': 'P1',
                'category': 'edge_case',
                'expected_result': "Proper handling of complex scenarios",
                'test_data': 'complex'
            }
        ]
    
    def _generate_error_tests(self) -> List[Dict]:
        """Generate P2 error handling tests."""
        return [
            {
                'description': "Test invalid input handling",
                'priority': 'P2',
                'category': 'error_handling',
                'expected_result': "Clear error message, no crash",
                'test_data': 'invalid'
            },
            {
                'description': "Test missing data handling",
                'priority': 'P2',
                'category': 'error_handling',
                'expected_result': "Appropriate fallback behavior",
                'test_data': 'missing'
            }
        ]
    
    def _generate_performance_tests(self) -> List[Dict]:
        """Generate P2 performance tests."""
        return [
            {
                'description': "Test response time",
                'priority': 'P2',
                'category': 'performance',
                'expected_result': "Response within acceptable time (<2s typical)",
                'test_data': 'typical'
            }
        ]
    
    # ========== OUTPUT GENERATION ==========
    
    def generate_test_documentation(self, output_path: Path):
        """
        Generate human-readable test documentation.
        
        Creates a markdown file with:
        - Test overview
        - Scenarios by priority
        - Setup instructions
        
        Args:
            output_path: Path to write documentation
        """
        lines = []
        lines.append(f"# Test Scenarios: {self.skill_name}\n")
        lines.append(f"**Generated:** Auto-generated from SKILL.md")
        lines.append(f"**Coverage:** {self.coverage}\n")
        
        # Group by priority
        for priority in ['P0', 'P1', 'P2']:
            priority_scenarios = [s for s in self.test_scenarios if s['priority'] == priority]
            if not priority_scenarios:
                continue
            
            lines.append(f"\n## {priority} Tests ({len(priority_scenarios)})\n")
            for scenario in priority_scenarios:
                lines.append(f"### {scenario['description']}")
                lines.append(f"- **Category:** {scenario['category']}")
                lines.append(f"- **Expected:** {scenario['expected_result']}")
                lines.append(f"- **Test Data:** {scenario['test_data']}\n")
        
        # Setup instructions
        lines.append("\n## Setup\n")
        lines.append("1. Install dependencies: `pip install pytest` (or unittest)")
        lines.append("2. Review test scenarios above")
        lines.append("3. Implement test logic in test files")
        lines.append("4. Run tests: `pytest tests/`\n")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def generate_pytest_implementation(self, output_path: Path):
        """Generate pytest test implementation."""
        lines = []
        lines.append("\"\"\"")
        lines.append(f"Pytest tests for {self.skill_name}")
        lines.append("Auto-generated - customize as needed")
        lines.append("\"\"\"")
        lines.append("\nimport pytest\n")
        
        # Generate test functions
        for scenario in self.test_scenarios:
            test_name = self._sanitize_test_name(scenario['description'])
            lines.append(f"def test_{test_name}():")
            lines.append(f"    \"\"\"")
            lines.append(f"    {scenario['description']}")
            lines.append(f"    Priority: {scenario['priority']}")
            lines.append(f"    Expected: {scenario['expected_result']}")
            lines.append(f"    \"\"\"")
            lines.append(f"    # TODO: Implement test logic")
            lines.append(f"    # Test data: {scenario['test_data']}")
            lines.append(f"    assert True, 'Test not implemented yet'\n")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def generate_unittest_implementation(self, output_path: Path):
        """Generate unittest test implementation."""
        lines = []
        lines.append("\"\"\"")
        lines.append(f"Unittest tests for {self.skill_name}")
        lines.append("Auto-generated - customize as needed")
        lines.append("\"\"\"")
        lines.append("\nimport unittest\n")
        
        lines.append(f"class Test{self.skill_name.replace('-', '_').title()}(unittest.TestCase):")
        lines.append(f"    \"\"\"Test suite for {self.skill_name}.\"\"\"")
        lines.append("")
        
        # Generate test methods
        for scenario in self.test_scenarios:
            test_name = self._sanitize_test_name(scenario['description'])
            lines.append(f"    def test_{test_name}(self):")
            lines.append(f"        \"\"\"")
            lines.append(f"        {scenario['description']}")
            lines.append(f"        Priority: {scenario['priority']}")
            lines.append(f"        Expected: {scenario['expected_result']}")
            lines.append(f"        \"\"\"")
            lines.append(f"        # TODO: Implement test logic")
            lines.append(f"        # Test data: {scenario['test_data']}")
            lines.append(f"        self.assertTrue(True, 'Test not implemented yet')\n")
        
        lines.append("\nif __name__ == '__main__':")
        lines.append("    unittest.main()")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def generate_plain_documentation(self, output_path: Path):
        """Generate plain text test plan."""
        lines = []
        lines.append(f"TEST PLAN: {self.skill_name}")
        lines.append("=" * 60)
        lines.append(f"Coverage: {self.coverage}")
        lines.append(f"Total scenarios: {len(self.test_scenarios)}\n")
        
        for i, scenario in enumerate(self.test_scenarios, 1):
            lines.append(f"\n{i}. {scenario['description']}")
            lines.append(f"   Priority: {scenario['priority']}")
            lines.append(f"   Category: {scenario['category']}")
            lines.append(f"   Expected: {scenario['expected_result']}")
            lines.append(f"   Test Data: {scenario['test_data']}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def generate_behavioral_tests(self, skill_path: str, skill_type: str) -> str:
        """
        Generate pressure-test scenarios for a skill.

        Returns pytest-compatible test template content.
        Behavioral templates are only emitted for pytest mode.
        """
        _ = skill_type
        if self.test_format != 'pytest':
            return ""

        template = '''"""
Behavioral tests for {skill_name}
Generated by test_generator.py --behavioral
"""

import pytest

# RED Phase: Baseline tests (run WITHOUT skill)
class TestBaselineBehavior:
    """Document how agents behave without skill."""

    def test_time_pressure_rationalization(self):
        """Under time pressure, agents typically..."""
        # Document expected failure
        pass

    def test_sunk_cost_rationalization(self):
        """With sunk cost, agents typically..."""
        pass

# GREEN Phase: Verification tests (run WITH skill)
class TestSkillCompliance:
    """Verify agents comply WITH skill."""

    def test_resists_time_pressure(self):
        """Skill helps agent resist time pressure."""
        pass

    def test_resists_sunk_cost(self):
        """Skill helps agent resist sunk cost fallacy."""
        pass

# REFACTOR Phase: Combined pressure
class TestCombinedPressure:
    """All pressures at once."""

    def test_combined_pressure_compliance(self):
        """Agent complies under maximum pressure."""
        pass
'''
        skill_name = Path(skill_path).name
        return template.format(skill_name=skill_name, skill_type=skill_type)
    
    def _sanitize_test_name(self, description: str) -> str:
        """
        Convert description to valid Python function name.
        
        Args:
            description: Test description
        
        Returns:
            Sanitized function name
        """
        # Remove non-alphanumeric, convert spaces to underscores
        name = re.sub(r'[^a-zA-Z0-9\s]', '', description)
        name = name.lower().replace(' ', '_')
        # Limit length and remove extra underscores
        name = re.sub(r'_+', '_', name)
        return name[:50].strip('_')
    
    # ========== MAIN EXECUTION ==========
    
    def generate(self):
        """
        Main generation workflow.
        
        1. Parse skill description
        2. Generate test scenarios
        3. Write test documentation
        4. Write test implementation
        
        References: File 12 (testing workflow)
        """
        # Parse
        skill_info = self.parse_skill_description()
        
        # Generate scenarios
        scenarios = self.generate_test_scenarios()
        
        # Calculate stats
        behavioral_generated = self.behavioral and self.test_format == 'pytest'

        stats = {
            'skill_name': skill_info['name'],
            'capabilities_found': len(skill_info['capabilities']),
            'total_scenarios': len(scenarios),
            'by_priority': {
                'P0': sum(1 for s in scenarios if s['priority'] == 'P0'),
                'P1': sum(1 for s in scenarios if s['priority'] == 'P1'),
                'P2': sum(1 for s in scenarios if s['priority'] == 'P2')
            },
            'coverage': self.coverage,
            'test_format': self.test_format,
            'behavioral': self.behavioral,
            'behavioral_generated': behavioral_generated
        }
        
        # Create tests/ directory
        tests_dir = self.skill_path / "tests"
        tests_dir.mkdir(exist_ok=True)
        
        # Write outputs
        self.generate_test_documentation(tests_dir / "test_scenarios.md")
        
        if self.test_format == 'pytest':
            self.generate_pytest_implementation(tests_dir / "test_skill.py")
            stats['output_files'] = [
                str(tests_dir / 'test_scenarios.md'),
                str(tests_dir / 'test_skill.py')
            ]
        elif self.test_format == 'unittest':
            self.generate_unittest_implementation(tests_dir / "test_skill.py")
            stats['output_files'] = [
                str(tests_dir / 'test_scenarios.md'),
                str(tests_dir / 'test_skill.py')
            ]
        else:  # plain
            self.generate_plain_documentation(tests_dir / "test_plan.txt")
            stats['output_files'] = [
                str(tests_dir / 'test_scenarios.md'),
                str(tests_dir / 'test_plan.txt')
            ]

        if behavioral_generated:
            behavioral_file = tests_dir / "test_behavioral.py"
            behavioral_content = self.generate_behavioral_tests(
                str(self.skill_path),
                "discipline"
            )
            with open(behavioral_file, 'w', encoding='utf-8') as f:
                f.write(behavioral_content)
            stats['output_files'].append(str(behavioral_file))
        
        # Output based on format
        if self.output_format == 'json':
            self._output_json(stats, scenarios)
        else:
            self._output_text(stats, tests_dir)
        
        return stats
    
    def _output_json(self, stats: Dict, scenarios: List[Dict]):
        """Output in JSON format for agent-layer."""
        output = {
            'status': 'success',
            'skill_name': stats['skill_name'],
            'capabilities_found': stats['capabilities_found'],
            'test_scenarios': {
                'total': stats['total_scenarios'],
                'by_priority': stats['by_priority'],
                'scenarios': scenarios
            },
            'configuration': {
                'coverage': stats['coverage'],
                'test_format': stats['test_format'],
                'behavioral': stats['behavioral'],
                'behavioral_generated': stats['behavioral_generated']
            },
            'output_files': stats['output_files'],
            'next_steps': [
                'Review test scenarios in test_scenarios.md',
                'Implement test logic in test files',
                f"Run: pytest {self.skill_path / 'tests'}" if self.test_format == 'pytest' else f"Run: python -m unittest discover {self.skill_path / 'tests'}"
            ]
        }
        print(json.dumps(output, indent=2))
    
    def _output_text(self, stats: Dict, tests_dir: Path):
        """Output in human-readable text format."""
        print(f"Generating tests for {self.skill_path}...")
        print(f"Skill: {stats['skill_name']}")
        print(f"Capabilities found: {stats['capabilities_found']}")
        print(f"Test scenarios generated: {stats['total_scenarios']}")
        print(f"  - P0 (Critical): {stats['by_priority']['P0']}")
        print(f"  - P1 (High): {stats['by_priority']['P1']}")
        print(f"  - P2 (Medium): {stats['by_priority']['P2']}")
        
        print(f"\nâœ” Test documentation: {tests_dir / 'test_scenarios.md'}")
        
        if self.test_format == 'pytest':
            print(f"âœ” Pytest implementation: {tests_dir / 'test_skill.py'}")
        elif self.test_format == 'unittest':
            print(f"âœ” Unittest implementation: {tests_dir / 'test_skill.py'}")
        else:
            print(f"âœ” Plain test plan: {tests_dir / 'test_plan.txt'}")
        if stats['behavioral_generated']:
            print(f"âœ” Behavioral template: {tests_dir / 'test_behavioral.py'}")
        elif stats['behavioral']:
            print("! Behavioral template skipped (only supported with --test-format pytest)")
        
        print(f"\nNext steps:")
        print(f"   1. Review test scenarios in test_scenarios.md")
        print(f"   2. Implement test logic in test files")
        if self.test_format == 'pytest':
            print(f"   3. Run: pytest {tests_dir}")
        elif self.test_format == 'unittest':
            print(f"   3. Run: python -m unittest discover {tests_dir}")
        print(f"\nâœ” Tests generated successfully!")

def main():
    """CLI entry point with v1.2 parameter standardization."""
    parser = argparse.ArgumentParser(
        description="Auto-generate test scenarios for skills",
        epilog="References: File 12 for testing best practices | v1.2: Standardized parameters"
    )
    parser.add_argument(
        'skill_path',
        type=str,
        help='Path to skill directory'
    )
    parser.add_argument(
        '--coverage',
        choices=['basic', 'standard', 'comprehensive'],
        default='standard',
        help='Test coverage level (default: standard)'
    )
    # v1.2: Renamed from --format (test framework choice)
    parser.add_argument(
        '--test-format',
        choices=['pytest', 'unittest', 'plain'],
        default='pytest',
        help='Test framework format (default: pytest)'
    )
    # v1.2: Renamed from --output (standardized to --format for all tools)
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format: text (human-readable) or json (agent-layer)'
    )
    # v1.2: Backward compatibility for deprecated --output parameter
    parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default=None,
        help='[DEPRECATED v1.2] Use --format instead. This parameter will be removed in v2.0.'
    )
    parser.add_argument(
        '--behavioral',
        action='store_true',
        help='Generate behavioral pressure tests'
    )

    args = parser.parse_args()

    # v1.2: Handle backward compatibility for --output parameter
    if args.output is not None:
        warnings.warn(
            "Parameter '--output' is deprecated (v1.2). Use '--format' instead. "
            "The '--output' parameter will be removed in v2.0.0.",
            DeprecationWarning,
            stacklevel=2
        )
        output_format = args.output
    else:
        output_format = args.format

    try:
        generator = TestGenerator(
            args.skill_path,
            coverage=args.coverage,
            test_format=args.test_format,
            output_format=output_format,
            behavioral=args.behavioral
        )
        generator.generate()
        return 0
    except FileNotFoundError as e:
        if output_format == 'json':
            print(json.dumps({
                'status': 'error',
                'error_type': 'FileNotFoundError',
                'message': str(e)
            }))
        else:
            print(f"✗ Error: {e}")
        return 1
    except Exception as e:
        if output_format == 'json':
            print(json.dumps({
                'status': 'error',
                'error_type': type(e).__name__,
                'message': str(e)
            }))
        else:
            print(f"✗ Unexpected error: {e}")
        return 2

if __name__ == "__main__":
    exit(main())
