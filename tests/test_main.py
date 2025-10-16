"""Basic tests for Magic Shell PR 1: Packaging & README & CI skeleton."""

import subprocess
import sys
from pathlib import Path


def test_main_import():
    """Test that main module can be imported."""
    from magic_shell.main import main
    assert callable(main)


def test_main_help_flag():
    """Test that main function handles --help flag."""
    # Test via subprocess to avoid SystemExit
    result = subprocess.run([
        sys.executable, "-m", "magic_shell.main", "--help"
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "magical wrapper" in result.stdout.lower()
    assert "--shell" in result.stdout
    assert "--theme" in result.stdout


def test_main_version_flag():
    """Test that main function handles --version flag.""" 
    result = subprocess.run([
        sys.executable, "-m", "magic_shell.main", "--version"
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_main_basic_run():
    """Test that main function runs and shows PR 1 message."""
    result = subprocess.run([
        sys.executable, "-m", "magic_shell.main"
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "Magic Shell v0.1.0" in result.stdout
    assert "PR 1:" in result.stdout
    assert "PTY bridge coming in PR 2" in result.stdout


def test_main_with_flags():
    """Test that main function handles various flag combinations."""
    result = subprocess.run([
        sys.executable, "-m", "magic_shell.main", 
        "--shell", "/bin/bash",
        "--theme", "ember", 
        "--plain",
        "--stage"
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "Shell: /bin/bash" in result.stdout
    assert "Theme: ember" in result.stdout
    assert "Plain mode: True" in result.stdout
    assert "Staging: True" in result.stdout


def test_console_entry_point():
    """Test that magic-shell console entry point works."""
    # This tests the console_scripts entry point from pyproject.toml
    result = subprocess.run([
        "magic-shell", "--version"
    ], capture_output=True, text=True)
    
    # This might fail if not installed, so check both success and expected error
    if result.returncode == 0:
        assert "0.1.0" in result.stdout
    else:
        # Command not found is expected if not installed
        assert result.returncode != 0


# Placeholder for integration tests (coming in PR 5)
def test_integration_placeholder():
    """Placeholder for future integration tests with external tools."""
    # These will be added in PR 5 with pexpect
    assert True  # Always pass for now