#!/usr/bin/env python3
"""
Comprehensive skill validation tool.
Validates skills against best practices from Files 02, 07, 10, 12.

v1.2 Update: Enhanced cross-reference validation
- Comprehensive file reference detection (markdown links, code refs, paths)
- File existence verification
- Orphaned file detection
- Uses CrossReferenceValidator utility

Usage:
    python validate_skill.py <skill_path> [--strict] [--format text|json]

References:
    - File 02: Description engineering patterns
    - File 07: Security best practices
    - File 10: Progressive disclosure architecture
    - File 12: Testing and validation checklist
"""

import os
import re
import sys
import json
import argparse
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from utils.reference_validator import CrossReferenceValidator
except ImportError:
    CrossReferenceValidator = None  # Graceful fallback


# Security scanning classes (from security_scanner.py)
class SecuritySeverity(Enum):
    """Security finding severity levels."""
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    INFO = 4


@dataclass
class SecurityFinding:
    """Single security finding."""
    severity: SecuritySeverity
    finding_type: str
    file: str
    line: int
    description: str
    evidence: str
    remediation: str


class SecurityScanner:
    """Integrated security vulnerability detection."""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.findings: list[SecurityFinding] = []

    def _get_scannable_files(self) -> list[Path]:
        """Get all files that should be scanned."""
        extensions = ['.py', '.md', '.sh', '.yaml', '.yml']
        files = []
        for ext in extensions:
            files.extend(self.skill_path.rglob(f'*{ext}'))
        return files

    def _get_python_files(self) -> list[Path]:
        """Get all Python files."""
        return list(self.skill_path.rglob('*.py'))

    def scan_hardcoded_secrets(self) -> list[SecurityFinding]:
        """Scan for hardcoded secrets."""
        findings = []
        secret_patterns = [
            (r'api[_-]?key\s*=\s*["\'][\w\-]+["\']', 'API key'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Password'),
            (r'token\s*=\s*["\'][\w\-]+["\']', 'Token'),
            (r'secret\s*=\s*["\'][\w\-]+["\']', 'Secret'),
            (r'Authorization:\s*Bearer\s+[\w\-\.]+', 'Bearer token'),
            (r'sk-[a-zA-Z0-9]{32,}', 'API key pattern'),
        ]

        for file_path in self._get_scannable_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            for pattern, secret_type in secret_patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(SecurityFinding(
                        severity=SecuritySeverity.CRITICAL,
                        finding_type='Hardcoded Secret',
                        file=str(file_path.relative_to(self.skill_path)),
                        line=line_num,
                        description=f'{secret_type} detected in code',
                        evidence=match.group(0)[:50] + '...',
                        remediation='Use environment variables or secret management'
                    ))
        return findings

    def scan_command_injection(self) -> list[SecurityFinding]:
        """Scan for command injection vulnerabilities."""
        findings = []
        dangerous_patterns = [
            (r'subprocess\.\w+\([^)]*shell\s*=\s*True', 'shell=True', SecuritySeverity.CRITICAL),
            (r'os\.system\s*\(', 'os.system()', SecuritySeverity.CRITICAL),
            (r'\beval\s*\(', 'eval()', SecuritySeverity.CRITICAL),
            (r'\bexec\s*\(', 'exec()', SecuritySeverity.CRITICAL),
        ]

        for file_path in self._get_python_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            for pattern, name, severity in dangerous_patterns:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(SecurityFinding(
                        severity=severity,
                        finding_type='Command Injection Risk',
                        file=str(file_path.relative_to(self.skill_path)),
                        line=line_num,
                        description=f'Dangerous function: {name}',
                        evidence=match.group(0),
                        remediation='Use parameterized commands, avoid shell=True/eval/exec'
                    ))
        return findings

    def scan_sql_injection(self) -> list[SecurityFinding]:
        """Scan for SQL injection patterns."""
        findings = []
        sql_patterns = [
            (r'(SELECT|INSERT|UPDATE|DELETE).*\+.*', 'string concatenation'),
            (r'(SELECT|INSERT|UPDATE|DELETE).*f["\'].*\{', 'f-string formatting'),
            (r'(SELECT|INSERT|UPDATE|DELETE).*\.format\(', '.format() usage'),
        ]

        for file_path in self._get_python_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            for pattern, name in sql_patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(SecurityFinding(
                        severity=SecuritySeverity.HIGH,
                        finding_type='SQL Injection Risk',
                        file=str(file_path.relative_to(self.skill_path)),
                        line=line_num,
                        description=f'SQL query with {name}',
                        evidence=match.group(0)[:80],
                        remediation='Use parameterized queries with placeholders (?)'
                    ))
        return findings

    def scan_dangerous_imports(self) -> list[SecurityFinding]:
        """Scan for dangerous library imports."""
        findings = []
        dangerous_imports = [
            ('import pickle', 'pickle', SecuritySeverity.HIGH,
             'Arbitrary code execution via deserialization. Use json instead.'),
            ('from pickle', 'pickle', SecuritySeverity.HIGH,
             'Arbitrary code execution via deserialization. Use json instead.'),
            ('yaml.load(', 'yaml.load()', SecuritySeverity.HIGH,
             'Unsafe YAML loading. Use yaml.safe_load() instead.'),
        ]

        for file_path in self._get_python_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            for pattern, name, severity, remediation in dangerous_imports:
                if pattern in content:
                    line_num = content.split(pattern)[0].count('\n') + 1
                    findings.append(SecurityFinding(
                        severity=severity,
                        finding_type='Dangerous Import',
                        file=str(file_path.relative_to(self.skill_path)),
                        line=line_num,
                        description=f'Risky library: {name}',
                        evidence=pattern,
                        remediation=remediation
                    ))
        return findings

    def run_all_scans(self) -> list[SecurityFinding]:
        """Run all security scans."""
        self.findings = []
        self.findings.extend(self.scan_hardcoded_secrets())
        self.findings.extend(self.scan_command_injection())
        self.findings.extend(self.scan_sql_injection())
        self.findings.extend(self.scan_dangerous_imports())
        return self.findings


@dataclass
class CostBreakdown:
    """Token and cost breakdown for a usage scenario."""
    scenario: str
    tokens: int
    cost_per_use: float
    monthly_cost: float


class TokenAnalyzer:
    """Token cost estimation and progressive disclosure analysis."""

    PRICING = {
        'claude-sonnet-4-6': {'input': 3.00, 'output': 15.00},
        'claude-opus-4-6': {'input': 15.00, 'output': 75.00}
    }

    def __init__(self, skill_path: str, model: str = 'claude-sonnet-4-6'):
        self.skill_path = Path(skill_path)
        self.model = model
        self.pricing = self.PRICING.get(model, self.PRICING['claude-sonnet-4-6'])

    def count_tokens(self, text: str) -> int:
        """Estimate token count using averaged method."""
        words = len(text.split())
        chars = len(text)
        token_by_words = int(words * 1.3)
        token_by_chars = int(chars / 4)
        return int((token_by_words + token_by_chars) / 2)

    def analyze_progressive_disclosure(self) -> dict:
        """Analyze skill using 3-level progressive disclosure model."""
        breakdown = {
            'level_1_metadata': 0,
            'level_2_skill_body': 0,
            'level_3_references': {},
        }

        skill_md = self.skill_path / 'SKILL.md'
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8')
            # Level 1: Metadata (frontmatter)
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    breakdown['level_1_metadata'] = self.count_tokens(parts[1])
                    breakdown['level_2_skill_body'] = self.count_tokens(parts[2])
            else:
                breakdown['level_2_skill_body'] = self.count_tokens(content)

        # Level 3: References
        refs_dir = self.skill_path / 'references'
        if refs_dir.exists():
            for ref_file in refs_dir.glob('*.md'):
                content = ref_file.read_text(encoding='utf-8')
                breakdown['level_3_references'][ref_file.name] = self.count_tokens(content)

        return breakdown

    def estimate_usage_scenarios(self, breakdown: dict) -> dict[str, int]:
        """Calculate token usage for different scenarios."""
        scenarios = {
            'idle': breakdown['level_1_metadata'],
            'typical': breakdown['level_1_metadata'] + breakdown['level_2_skill_body'],
        }

        if breakdown['level_3_references']:
            smallest_ref = min(breakdown['level_3_references'].values())
            scenarios['with_reference'] = scenarios['typical'] + smallest_ref
            total_refs = sum(breakdown['level_3_references'].values())
            scenarios['worst_case'] = scenarios['typical'] + total_refs
        else:
            scenarios['with_reference'] = scenarios['typical']
            scenarios['worst_case'] = scenarios['typical']

        return scenarios


class Severity(Enum):
    """Validation result severity levels."""
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"


@dataclass
class ValidationResult:
    """Single validation check result."""
    check_name: str
    severity: Severity
    message: str
    suggestion: str = ""
    line_number: int = None


class SkillValidator:
    """Main validator implementing 10 comprehensive checks."""
    
    def __init__(self, skill_path: str, strict: bool = False):
        """
        Initialize validator.
        
        Args:
            skill_path: Path to skill directory
            strict: If True, warnings become failures
        """
        self.skill_path = Path(skill_path)
        self.strict = strict
        self.results: List[ValidationResult] = []
        
        # Load SKILL.md content once
        self.skill_md_path = self.skill_path / "SKILL.md"
        self.skill_content = ""
        self.frontmatter = {}
        
        if self.skill_md_path.exists():
            self.skill_content = self.skill_md_path.read_text(encoding='utf-8')
            self._parse_frontmatter()
    
    def _parse_frontmatter(self):
        """Extract and parse YAML frontmatter."""
        if self.skill_content.startswith('---'):
            parts = self.skill_content.split('---', 2)
            if len(parts) >= 3:
                try:
                    self.frontmatter = yaml.safe_load(parts[1])
                except yaml.YAMLError:
                    self.frontmatter = {}
    
    # ========== STRUCTURAL VALIDATION ==========
    
    def validate_yaml_frontmatter(self) -> ValidationResult:
        """Validate YAML frontmatter structure and required fields."""
        if not self.skill_md_path.exists():
            return ValidationResult(
                "YAML Frontmatter",
                Severity.FAIL,
                "SKILL.md not found",
                "Create SKILL.md in skill directory"
            )
        
        if not self.frontmatter:
            return ValidationResult(
                "YAML Frontmatter",
                Severity.FAIL,
                "Invalid or missing YAML frontmatter",
                "Add valid YAML frontmatter between --- markers"
            )
        
        # Check required fields
        required_fields = ['name', 'description']
        missing = [f for f in required_fields if f not in self.frontmatter]
        
        if missing:
            return ValidationResult(
                "YAML Frontmatter",
                Severity.FAIL,
                f"Missing required fields: {', '.join(missing)}",
                "Add required fields to frontmatter"
            )
        
        return ValidationResult(
            "YAML Frontmatter",
            Severity.PASS,
            "Valid YAML frontmatter with required fields"
        )
    
    def validate_file_structure(self) -> ValidationResult:
        """Validate skill directory structure."""
        if not self.skill_md_path.exists():
            return ValidationResult(
                "File Structure",
                Severity.FAIL,
                "SKILL.md missing",
                "Create SKILL.md file"
            )
        
        issues = []
        
        # Check for scripts directory if any .py files exist
        scripts_dir = self.skill_path / "scripts"
        py_files = list(self.skill_path.glob("*.py"))
        
        if py_files and not scripts_dir.exists():
            issues.append("Python files found but no scripts/ directory")
        
        # Check for references directory if SKILL.md is large
        line_count = len(self.skill_content.splitlines())
        references_dir = self.skill_path / "references"
        
        if line_count > 500 and not references_dir.exists():
            issues.append(f"SKILL.md has {line_count} lines (>500), consider using references/")
        
        if issues:
            severity = Severity.WARNING if not self.strict else Severity.FAIL
            return ValidationResult(
                "File Structure",
                severity,
                "; ".join(issues),
                "Organize files according to progressive disclosure pattern (File 10)"
            )
        
        return ValidationResult(
            "File Structure",
            Severity.PASS,
            "Proper file organization"
        )
    
    # ========== DESCRIPTION QUALITY ==========
    
    def validate_description_quality(self) -> ValidationResult:
        """Validate description includes WHAT + WHEN."""
        description = self.frontmatter.get('description', '')
        
        if not description:
            return ValidationResult(
                "Description Quality",
                Severity.FAIL,
                "Description is empty",
                "Add description with WHAT (capability) and WHEN (triggers)"
            )
        
        # Check length
        if len(description) < 20:
            return ValidationResult(
                "Description Quality",
                Severity.WARNING,
                f"Description too short ({len(description)} chars)",
                "Expand to 20-100 words with clear capabilities"
            )
        
        if len(description) > 1024:
            return ValidationResult(
                "Description Quality",
                Severity.FAIL,
                f"Description too long ({len(description)} chars, max 1024)",
                "Condense to essential WHAT and WHEN information"
            )
        
        # Check for trigger phrases (WHEN)
        trigger_phrases = [
            'use when', 'trigger on', 'for tasks involving',
            'when claude needs to', 'activate when', 'applies to'
        ]
        
        has_trigger = any(phrase in description.lower() for phrase in trigger_phrases)
        
        if not has_trigger:
            severity = Severity.WARNING if not self.strict else Severity.FAIL
            return ValidationResult(
                "Description Quality",
                severity,
                "Description missing WHEN trigger phrases",
                "Add phrases like 'Use when...' or 'Trigger on...' (File 02)"
            )
        
        return ValidationResult(
            "Description Quality",
            Severity.PASS,
            "Description includes WHAT and WHEN triggers"
        )
    
    # ========== TOKEN EFFICIENCY ==========
    
    def validate_token_count(self) -> ValidationResult:
        """Validate token efficiency."""
        line_count = len(self.skill_content.splitlines())
        
        # Estimate tokens (average method: 1 line â‰ˆ 8 tokens)
        estimated_tokens = int(line_count * 8)
        
        issues = []
        
        # SKILL.md size checks
        if line_count > 800:
            issues.append(f"SKILL.md too large ({line_count} lines, max 800)")
        elif line_count > 500:
            issues.append(f"SKILL.md large ({line_count} lines), consider splitting at 500+")
        
        # Token estimate checks
        if estimated_tokens > 6000:
            issues.append(f"Estimated {estimated_tokens} tokens (critical >6000)")
        elif estimated_tokens > 4500:
            issues.append(f"Estimated {estimated_tokens} tokens (warning >4500)")
        
        if not issues:
            return ValidationResult(
                "Token Efficiency",
                Severity.PASS,
                f"Efficient: {line_count} lines (~{estimated_tokens} tokens)"
            )
        
        severity = Severity.FAIL if line_count > 800 else Severity.WARNING
        
        return ValidationResult(
            "Token Efficiency",
            severity,
            "; ".join(issues),
            "Apply progressive disclosure: move details to references/ (File 10)"
        )
    
    # ========== SECURITY VALIDATION ==========
    
    def validate_security_basics(self) -> ValidationResult:
        """Basic security checks (see security_scanner.py for comprehensive audit)."""
        issues = []
        
        # Check SKILL.md for obvious secrets
        secret_patterns = [
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret'),
            (r'token\s*=\s*["\'][^"\']+["\']', 'Hardcoded token'),
        ]
        
        for pattern, desc in secret_patterns:
            if re.search(pattern, self.skill_content, re.IGNORECASE):
                issues.append(f"{desc} detected in SKILL.md")
        
        # Check scripts for dangerous patterns
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists():
            for script_file in scripts_dir.glob("*.py"):
                script_content = script_file.read_text(encoding='utf-8')
                
                if 'shell=True' in script_content:
                    issues.append(f"shell=True found in {script_file.name}")
                
                if re.search(r'\beval\s*\(', script_content):
                    issues.append(f"eval() usage in {script_file.name}")
                
                if re.search(r'\bexec\s*\(', script_content):
                    issues.append(f"exec() usage in {script_file.name}")
        
        if issues:
            return ValidationResult(
                "Security Basics",
                Severity.FAIL,
                "; ".join(issues),
                "Remove hardcoded secrets, avoid shell=True/eval/exec (File 07). Run security_scanner.py for full audit."
            )
        
        return ValidationResult(
            "Security Basics",
            Severity.PASS,
            "No obvious security issues (run security_scanner.py for comprehensive audit)"
        )
    
    # ========== BEST PRACTICES ==========
    
    def validate_writing_style(self) -> ValidationResult:
        """Validate agent-layer writing style."""
        body = self.skill_content.split('---', 2)[-1] if '---' in self.skill_content else self.skill_content
        
        issues = []
        
        # Check for non-imperative patterns
        weak_patterns = [
            'you can', 'you may', 'you should', 'you might',
            'it is possible', 'one could', 'consider'
        ]
        
        weak_count = sum(body.lower().count(pattern) for pattern in weak_patterns)
        
        if weak_count > 5:
            issues.append(f"Too many weak phrases ({weak_count} instances)")
        
        # Check for section headers (good sign of organization)
        header_count = len(re.findall(r'^#+\s+', body, re.MULTILINE))
        
        if header_count < 3 and len(body.splitlines()) > 100:
            issues.append("Few section headers (improves scannability)")
        
        if issues:
            severity = Severity.WARNING
            return ValidationResult(
                "Writing Style",
                severity,
                "; ".join(issues),
                "Use imperative form ('Use X' not 'You can use X'), add clear headers"
            )
        
        return ValidationResult(
            "Writing Style",
            Severity.PASS,
            "Agent-layer writing style maintained"
        )
    
    def validate_progressive_disclosure(self) -> ValidationResult:
        """Validate progressive disclosure implementation."""
        line_count = len(self.skill_content.splitlines())
        references_dir = self.skill_path / "references"
        
        # If SKILL.md is large but no references, suggest splitting
        if line_count > 350 and not references_dir.exists():
            return ValidationResult(
                "Progressive Disclosure",
                Severity.WARNING,
                f"SKILL.md has {line_count} lines, no references/ directory",
                "Move optional details to references/ for better progressive disclosure (File 10)"
            )
        
        # Check reference files have TOC if >100 lines
        if references_dir.exists():
            for ref_file in references_dir.glob("*.md"):
                ref_content = ref_file.read_text(encoding='utf-8')
                ref_lines = len(ref_content.splitlines())
                
                if ref_lines > 100:
                    # Simple TOC check: look for list of links to headers
                    has_toc = bool(re.search(r'\[.*\]\(#.*\)', ref_content[:500]))
                    
                    if not has_toc:
                        return ValidationResult(
                            "Progressive Disclosure",
                            Severity.WARNING,
                            f"{ref_file.name} has {ref_lines} lines but no TOC",
                            "Add table of contents at top of reference files >100 lines"
                        )
        
        return ValidationResult(
            "Progressive Disclosure",
            Severity.PASS,
            "Progressive disclosure properly implemented"
        )
    
    def validate_cross_references(self) -> ValidationResult:
        """
        Validate cross-reference integrity with comprehensive file checking.

        v1.2 Enhanced: Uses CrossReferenceValidator for:
        - Markdown links: [text](path)
        - Code references: `file.md`
        - Path patterns: "file: path.md"
        - File existence verification
        - Orphaned file detection
        """
        # Try to use comprehensive CrossReferenceValidator
        if CrossReferenceValidator:
            try:
                validator = CrossReferenceValidator(str(self.skill_path))
                ref_result = validator.validate_skill_md()

                if ref_result.status == 'fail':
                    # Comprehensive failure message with all issues
                    issues = []
                    if ref_result.missing_files:
                        issues.append(f"Missing: {', '.join(ref_result.missing_files[:3])}")
                    if ref_result.orphaned_files:
                        issues.append(f"Orphaned: {', '.join(ref_result.orphaned_files[:3])}")

                    return ValidationResult(
                        "Cross-References",
                        Severity.FAIL,
                        f"{'; '.join(issues)}{'...' if len(issues) > 2 else ''}",
                        ref_result.suggestion or "Fix or remove broken cross-references"
                    )
                else:
                    return ValidationResult(
                        "Cross-References",
                        Severity.PASS,
                        f"All {len(ref_result.valid_references)} cross-references valid"
                    )
            except Exception as e:
                # Fallback to original simple validation
                pass

        # Fallback: Original simple validation (backward compatibility)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, self.skill_content)

        broken = []

        for link_text, link_target in links:
            # Skip external URLs
            if link_target.startswith(('http://', 'https://', '#')):
                continue

            # Check if file exists
            target_path = self.skill_path / link_target
            if not target_path.exists():
                broken.append(f"'{link_text}' -> {link_target}")

        if broken:
            return ValidationResult(
                "Cross-References",
                Severity.FAIL,
                f"Broken links found: {'; '.join(broken[:3])}{'...' if len(broken) > 3 else ''}",
                "Fix or remove broken cross-references"
            )

        return ValidationResult(
            "Cross-References",
            Severity.PASS,
            "All cross-references valid"
        )
    
    # ========== UTILITY METHODS ==========
    
    def run_all_validations(self) -> List[ValidationResult]:
        """Run all validation checks."""
        self.results = [
            self.validate_yaml_frontmatter(),
            self.validate_file_structure(),
            self.validate_description_quality(),
            self.validate_token_count(),
            self.validate_security_basics(),
            self.validate_writing_style(),
            self.validate_progressive_disclosure(),
            self.validate_cross_references(),
        ]
        return self.results
    
    def generate_report(self, format: str = 'text') -> str:
        """Generate validation report."""
        if format == 'json':
            return self._generate_json_report()
        return self._generate_text_report()
    
    def _generate_text_report(self) -> str:
        """Generate human-readable text report."""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"Skill Validation Report: {self.skill_path.name}")
        lines.append('='*60 + '\n')
        
        # Categorize results
        passed = [r for r in self.results if r.severity == Severity.PASS]
        warnings = [r for r in self.results if r.severity == Severity.WARNING]
        failed = [r for r in self.results if r.severity == Severity.FAIL]
        
        # Display results
        for result in self.results:
            icon = {
                Severity.PASS: 'âœ“',
                Severity.WARNING: 'âš ',
                Severity.FAIL: 'âœ—'
            }[result.severity]
            
            lines.append(f"{icon} {result.check_name}")
            
            if result.severity != Severity.PASS:
                lines.append(f"  {result.message}")
                if result.suggestion:
                    lines.append(f"  â†’ {result.suggestion}")
            
            lines.append('')
        
        # Summary
        lines.append('-'*60)
        lines.append(f"Validation Score: {len(passed)}/{len(self.results)} checks passed")
        lines.append(f"Severity: {len(failed)} critical, {len(warnings)} warnings, {len(passed)} passed")
        lines.append('')
        
        if failed:
            lines.append("âŒ Fix critical issues before packaging.")
        elif warnings:
            lines.append("âš ï¸  Address warnings to improve quality.")
        else:
            lines.append("âœ… All validations passed! Skill ready for deployment.")
        
        return '\n'.join(lines)
    
    def _generate_json_report(self) -> str:
        """Generate machine-readable JSON report."""
        report = {
            'skill_name': self.skill_path.name,
            'timestamp': str(Path.cwd()),
            'results': [
                {
                    'check': r.check_name,
                    'severity': r.severity.value,
                    'message': r.message,
                    'suggestion': r.suggestion
                }
                for r in self.results
            ],
            'summary': {
                'total': len(self.results),
                'passed': len([r for r in self.results if r.severity == Severity.PASS]),
                'warnings': len([r for r in self.results if r.severity == Severity.WARNING]),
                'failed': len([r for r in self.results if r.severity == Severity.FAIL])
            }
        }
        return json.dumps(report, indent=2)
    
    def get_exit_code(self) -> int:
        """Get appropriate exit code based on results."""
        if any(r.severity == Severity.FAIL for r in self.results):
            return 2  # Critical failures
        if any(r.severity == Severity.WARNING for r in self.results):
            return 1  # Warnings only
        return 0  # All passed


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Comprehensive skill validation tool',
        epilog='References: Files 02, 07, 10, 12 for validation rules'
    )
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--strict', action='store_true',
                        help='Treat warnings as failures')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='Output format (default: text)')
    
    args = parser.parse_args()
    
    # Validate skill path
    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"Error: Skill path '{skill_path}' does not exist", file=sys.stderr)
        sys.exit(2)
    
    if not skill_path.is_dir():
        print(f"Error: '{skill_path}' is not a directory", file=sys.stderr)
        sys.exit(2)
    
    # Run validation
    validator = SkillValidator(skill_path, strict=args.strict)
    validator.run_all_validations()
    
    # Generate report
    report = validator.generate_report(format=args.format)
    print(report)
    
    # Exit with appropriate code
    sys.exit(validator.get_exit_code())


if __name__ == '__main__':
    main()
