#!/usr/bin/env python3
"""
Tests for consolidated scripts functionality.

Verifies that init.py and validate_skill.py maintain
backward compatibility with deprecated scripts.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SKILLKIT_DIR = Path(__file__).parent.parent.parent
SCRIPTS_DIR = SKILLKIT_DIR / 'scripts'


class TestInitConsolidation:
    """Tests for unified init.py script."""

    def test_init_skill_creates_structure(self):
        """Verify init.py skill creates proper directory structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / 'init.py'),
                 'skill', 'test-skill', '--path', tmpdir, '--mode', 'fast'],
                capture_output=True, text=True
            )
            assert result.returncode == 0, f"init.py failed: {result.stderr}"

            skill_dir = Path(tmpdir) / 'test-skill'
            assert skill_dir.exists()
            assert (skill_dir / 'SKILL.md').exists()
            assert (skill_dir / 'scripts').exists()
            assert (skill_dir / 'references').exists()
            assert (skill_dir / 'assets').exists()
            assert (skill_dir / '.skillkit-mode').read_text().strip() == 'fast'

    def test_init_skill_full_mode(self):
        """Verify init.py skill --mode full creates behavioral sections."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / 'init.py'),
                 'skill', 'test-skill', '--path', tmpdir, '--mode', 'full'],
                capture_output=True, text=True
            )
            assert result.returncode == 0

            skill_md = Path(tmpdir) / 'test-skill' / 'SKILL.md'
            content = skill_md.read_text()
            assert 'Behavioral Validation' in content
            assert 'RED Phase' in content
            assert 'Pressure Test Results' in content

    def test_init_subagent_creates_file(self):
        """Verify init.py subagent creates .md file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / 'init.py'),
                 'subagent', 'test-agent', '--path', tmpdir],
                capture_output=True, text=True
            )
            assert result.returncode == 0, f"init.py subagent failed: {result.stderr}"

            agent_file = Path(tmpdir) / 'test-agent.md'
            assert agent_file.exists()
            content = agent_file.read_text()
            assert 'name: test-agent' in content
            assert 'subagent_type' in content

    def test_init_skill_invalid_name(self):
        """Verify init.py rejects invalid skill names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / 'init.py'),
                 'skill', 'INVALID_NAME', '--path', tmpdir],
                capture_output=True, text=True
            )
            assert result.returncode != 0
            assert 'Invalid skill name' in result.stdout or 'Invalid skill name' in result.stderr

    def test_init_subagent_invalid_name(self):
        """Verify init.py rejects invalid subagent names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / 'init.py'),
                 'subagent', 'INVALID_NAME', '--path', tmpdir],
                capture_output=True, text=True
            )
            assert result.returncode != 0


class TestDeprecatedInitScripts:
    """Tests that old init scripts print deprecation warnings."""

    def test_init_skill_deprecated(self):
        """Verify init_skill.py prints deprecation and exits 1."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'init_skill.py'), 'test'],
            capture_output=True, text=True
        )
        assert result.returncode == 1
        assert 'DEPRECATED' in result.stderr
        assert 'init.py skill' in result.stderr

    def test_init_subagent_deprecated(self):
        """Verify init_subagent.py prints deprecation and exits 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / 'init_subagent.py'), 'test', '--path', tmpdir],
                capture_output=True, text=True
            )
            assert result.returncode == 1
            assert 'DEPRECATED' in result.stderr
            assert 'init.py subagent' in result.stderr


class TestValidateConsolidation:
    """Tests for enhanced validate_skill.py script."""

    @pytest.fixture
    def sample_skill(self, tmp_path):
        """Create a sample skill for testing."""
        skill_dir = tmp_path / 'sample-skill'
        skill_dir.mkdir()

        # Create SKILL.md with frontmatter
        skill_md = skill_dir / 'SKILL.md'
        skill_md.write_text("""---
name: sample-skill
description: Test skill for validation
---

# Sample Skill

## Overview

This is a test skill.
""")
        return skill_dir

    def test_validate_all_runs_structure(self, sample_skill):
        """Verify default validate runs structure checks."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'validate_skill.py'),
             str(sample_skill), '--format', 'json'],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Validation failed: {result.stderr}"

        output = json.loads(result.stdout)
        assert 'validations' in output
        assert 'structure' in output['validations']

    def test_validate_security_only(self, sample_skill):
        """Verify --security-only flag works."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'validate_skill.py'),
             str(sample_skill), '--security-only', '--format', 'json'],
            capture_output=True, text=True
        )
        assert result.returncode == 0

        output = json.loads(result.stdout)
        assert 'security' in output['validations']
        assert 'structure' not in output['validations']
        assert 'tokens' not in output['validations']

    def test_validate_structure_only(self, sample_skill):
        """Verify --structure-only flag works."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'validate_skill.py'),
             str(sample_skill), '--structure-only', '--format', 'json'],
            capture_output=True, text=True
        )
        assert result.returncode == 0

        output = json.loads(result.stdout)
        assert 'structure' in output['validations']
        assert 'security' not in output['validations']
        assert 'tokens' not in output['validations']

    def test_validate_tokens_only(self, sample_skill):
        """Verify --tokens-only flag works."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'validate_skill.py'),
             str(sample_skill), '--tokens-only', '--format', 'json'],
            capture_output=True, text=True
        )
        assert result.returncode == 0

        output = json.loads(result.stdout)
        assert 'tokens' in output['validations']
        assert 'structure' not in output['validations']
        assert 'security' not in output['validations']

    def test_validate_detects_secrets(self, sample_skill):
        """Verify security scan detects hardcoded secrets."""
        # Add a file with a secret
        secret_file = sample_skill / 'scripts' / 'test.py'
        secret_file.parent.mkdir(exist_ok=True)
        secret_file.write_text('api_key = "sk-test1234567890123456789012345678"\n')

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'validate_skill.py'),
             str(sample_skill), '--security-only', '--format', 'json'],
            capture_output=True, text=True
        )

        output = json.loads(result.stdout)
        findings = output['validations']['security']['findings']
        assert any('API key' in f['description'] for f in findings)

    def test_validate_token_counts(self, sample_skill):
        """Verify token analysis produces reasonable counts."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'validate_skill.py'),
             str(sample_skill), '--tokens-only', '--format', 'json'],
            capture_output=True, text=True
        )

        output = json.loads(result.stdout)
        scenarios = output['validations']['tokens']['scenarios']
        assert 'idle' in scenarios
        assert 'typical' in scenarios
        assert scenarios['typical'] >= scenarios['idle']


class TestDeprecatedValidateScripts:
    """Tests that old validate scripts print deprecation warnings."""

    def test_security_scanner_deprecated(self):
        """Verify security_scanner.py prints deprecation and exits 1."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'security_scanner.py'), '/tmp'],
            capture_output=True, text=True
        )
        assert result.returncode == 1
        assert 'DEPRECATED' in result.stderr
        assert '--security-only' in result.stderr

    def test_token_estimator_deprecated(self):
        """Verify token_estimator.py prints deprecation and exits 1."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'token_estimator.py'), '/tmp'],
            capture_output=True, text=True
        )
        assert result.returncode == 1
        assert 'DEPRECATED' in result.stderr
        assert '--tokens-only' in result.stderr


class TestFeatureParity:
    """Verify consolidated scripts have feature parity with old ones."""

    def test_skill_name_validation_matches(self):
        """Verify init.py uses same name validation as old scripts."""
        invalid_names = [
            'UPPERCASE',
            'name_with_underscore',
            '-starts-with-dash',
            'ends-with-dash-',
            'has--double-dash',
            'a' * 41,  # Too long
        ]

        for name in invalid_names:
            with tempfile.TemporaryDirectory() as tmpdir:
                result = subprocess.run(
                    [sys.executable, str(SCRIPTS_DIR / 'init.py'),
                     'skill', name, '--path', tmpdir],
                    capture_output=True, text=True
                )
                assert result.returncode != 0, f"Should reject: {name}"

    def test_security_scan_covers_all_checks(self):
        """Verify security scanner covers patterns from old script."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / 'test'
            skill_dir.mkdir()
            skill_dir.joinpath('SKILL.md').write_text('---\nname: test\n---\n# Test')

            scripts_dir = skill_dir / 'scripts'
            scripts_dir.mkdir()

            # Test various vulnerable patterns
            (scripts_dir / 'secrets.py').write_text(
                'password = "secret123"\n'
                'api_key = "sk-test1234567890123456789012345678"\n'
            )
            (scripts_dir / 'injection.py').write_text(
                'import subprocess\n'
                'subprocess.run(cmd, shell=True)\n'
            )
            (scripts_dir / 'dangerous.py').write_text(
                'import pickle\n'
                'data = pickle.loads(untrusted)\n'
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / 'validate_skill.py'),
                 str(skill_dir), '--security-only', '--format', 'json'],
                capture_output=True, text=True
            )

            output = json.loads(result.stdout)
            findings = output['validations']['security']['findings']
            finding_types = {f['type'] for f in findings}

            assert 'Hardcoded Secret' in finding_types
            assert 'Command Injection Risk' in finding_types
            assert 'Dangerous Import' in finding_types


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
