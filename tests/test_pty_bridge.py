"""Tests for PTY bridge and shell detection - PR 2."""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from magic_shell.core.shell_detect import (
    get_login_shell,
    get_shell_name, 
    validate_shell,
    get_shell_with_fallback
)


class TestShellDetection:
    """Tests for shell detection functionality."""
    
    def test_get_shell_name(self):
        """Test shell name extraction from path."""
        assert get_shell_name("/bin/bash") == "bash"
        assert get_shell_name("/usr/bin/zsh") == "zsh"
        assert get_shell_name("/bin/sh") == "sh"
        assert get_shell_name("fish") == "fish"
    
    def test_validate_shell_existing(self):
        """Test validation of existing shells."""
        # Test with /bin/sh which should exist on most Unix systems
        if Path("/bin/sh").exists():
            assert validate_shell("/bin/sh") is True
            
        # Test with a non-existent path
        assert validate_shell("/nonexistent/shell") is False
        assert validate_shell("") is False
    
    def test_validate_shell_edge_cases(self):
        """Test shell validation edge cases."""
        assert validate_shell(None) is False
        assert validate_shell(123) is False  # type: ignore
        
    def test_get_login_shell(self):
        """Test login shell detection."""
        shell = get_login_shell()
        
        # Should return a valid path
        assert shell is not None
        assert isinstance(shell, str)
        assert len(shell) > 0
        
        # Should be a valid executable
        assert validate_shell(shell) is True
    
    def test_get_shell_with_fallback_auto(self):
        """Test shell detection with auto-detection."""
        shell = get_shell_with_fallback(None)
        
        assert shell is not None
        assert validate_shell(shell) is True
    
    def test_get_shell_with_fallback_valid_request(self):
        """Test shell detection with valid requested shell."""
        if Path("/bin/sh").exists():
            shell = get_shell_with_fallback("/bin/sh")
            assert shell == "/bin/sh"
    
    def test_get_shell_with_fallback_invalid_request(self):
        """Test shell detection with invalid requested shell."""
        with pytest.raises(RuntimeError, match="not available"):
            get_shell_with_fallback("/nonexistent/shell")


class TestPTYBridge:
    """Tests for PTY bridge functionality."""
    
    def test_pty_bridge_import(self):
        """Test that PTYBridge can be imported."""
        from magic_shell.core.bridge import PTYBridge
        assert PTYBridge is not None
    
    def test_pty_bridge_initialization(self):
        """Test PTY bridge initialization."""
        from magic_shell.core.bridge import PTYBridge
        
        # Test with default shell
        bridge = PTYBridge()
        assert bridge.shell_path is not None
        assert bridge.stage_mode is False
        assert bridge.master_fd is None
        assert bridge.child_pid is None
        
        # Test with explicit shell
        if Path("/bin/sh").exists():
            bridge = PTYBridge(shell_path="/bin/sh", stage_mode=True)
            assert bridge.shell_path == "/bin/sh"
            assert bridge.stage_mode is True
    
    def test_pty_bridge_shell_info(self):
        """Test shell information retrieval."""
        from magic_shell.core.bridge import PTYBridge
        
        bridge = PTYBridge()
        info = bridge.get_shell_info()
        
        assert "path" in info
        assert "name" in info  
        assert "stage_mode" in info
        assert isinstance(info["path"], str)
        assert isinstance(info["name"], str)
        assert isinstance(info["stage_mode"], bool)
    
    @pytest.mark.pty
    def test_pty_bridge_invalid_shell(self):
        """Test PTY bridge with invalid shell."""
        from magic_shell.core.bridge import PTYBridge
        
        with pytest.raises(RuntimeError):
            PTYBridge(shell_path="/nonexistent/shell")


class TestMainIntegration:
    """Integration tests for main entry point with PTY bridge."""
    
    def test_main_with_pty_help(self):
        """Test main function help still works with PTY changes."""
        result = subprocess.run([
            sys.executable, "-m", "magic_shell.main", "--help"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "magical wrapper" in result.stdout.lower()
    
    def test_main_version_updated(self):
        """Test that version is updated to v0.4.0 for PR 4."""
        import subprocess
        import sys
        
        result = subprocess.run([
            sys.executable, "-m", "magic_shell.main", "--version"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "0.4.0" in result.stdout
    
    def test_main_shell_detection_error(self):
        """Test main handles shell detection errors gracefully."""
        with patch("magic_shell.main.get_shell_with_fallback") as mock_shell:
            mock_shell.side_effect = RuntimeError("No shell found")
            
            result = subprocess.run([
                sys.executable, "-c", 
                "from magic_shell.main import main; exit(main())"
            ], capture_output=True, text=True)
            
            assert result.returncode == 1
            assert "Magic Shell error" in result.stderr
    
    @pytest.mark.pty 
    def test_main_invalid_shell_flag(self):
        """Test main with invalid --shell flag."""
        result = subprocess.run([
            sys.executable, "-m", "magic_shell.main", 
            "--shell", "/nonexistent/shell"
        ], capture_output=True, text=True, timeout=5)
        
        assert result.returncode == 1
        assert "error" in result.stderr.lower()


# Placeholder for future integration tests (coming in PR 5)
@pytest.mark.integration
class TestIntegrationPlaceholder:
    """Placeholder for integration tests with external tools."""
    
    def test_vim_integration_placeholder(self):
        """Placeholder for vim integration test."""
        # Will test: magic-shell -c "vim -Nu NONE -c q" 
        # Verify vim works identically through PTY bridge
        pytest.skip("Integration tests coming in PR 5")
    
    def test_less_integration_placeholder(self):
        """Placeholder for less integration test."""  
        # Will test: echo "test" | magic-shell -c "less"
        # Verify pager works correctly
        pytest.skip("Integration tests coming in PR 5")
    
    def test_ssh_integration_placeholder(self):
        """Placeholder for SSH integration test."""
        # Will test: magic-shell -c "ssh -G localhost"
        # Verify SSH config parsing works
        pytest.skip("Integration tests coming in PR 5")