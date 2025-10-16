"""Tests for shell hooks and OSC marker parsing - PR 3."""

import pytest
from unittest.mock import patch, MagicMock

from magic_shell.core.hooks import ShellHooks, shell_hooks


class TestShellHooks:
    """Tests for shell hook injection and marker parsing."""
    
    def test_shell_hooks_initialization(self):
        """Test ShellHooks initialization."""
        hooks = ShellHooks()
        
        assert "bash" in hooks.hooks
        assert "zsh" in hooks.hooks
        assert "fish" in hooks.hooks
    
    def test_osc_markers_defined(self):
        """Test that OSC escape sequences are properly defined."""
        hooks = ShellHooks()
        
        # Check that OSC markers are proper escape sequences
        assert hooks.OSC_COMMAND_START.startswith("\033]133;")
        assert hooks.OSC_COMMAND_END.startswith("\033]133;") 
        assert hooks.OSC_PROMPT_START.startswith("\033]133;")
        assert hooks.OSC_PROMPT_END.startswith("\033]133;")
        
        # Check they end with bell character
        assert hooks.OSC_COMMAND_START.endswith("\007")
        assert hooks.OSC_COMMAND_END.endswith("\007")
    
    def test_supported_shells(self):
        """Test shell support detection.""" 
        hooks = ShellHooks()
        
        assert hooks.is_supported_shell("bash") is True
        assert hooks.is_supported_shell("zsh") is True  
        assert hooks.is_supported_shell("fish") is True
        assert hooks.is_supported_shell("sh") is False
        assert hooks.is_supported_shell("unknown") is False
    
    def test_bash_hooks_generation(self):
        """Test bash hook command generation."""
        hooks = ShellHooks()
        bash_hooks = hooks.get_shell_hooks("bash")
        
        assert bash_hooks is not None
        assert "init_commands" in bash_hooks
        
        commands = bash_hooks["init_commands"]
        assert len(commands) > 0
        
        # Check that PROMPT_COMMAND and DEBUG trap are set up
        command_str = " ".join(commands)
        assert "PROMPT_COMMAND" in command_str
        assert "trap" in command_str
        assert "DEBUG" in command_str
    
    def test_zsh_hooks_generation(self):
        """Test zsh hook command generation."""
        hooks = ShellHooks()
        zsh_hooks = hooks.get_shell_hooks("zsh")
        
        assert zsh_hooks is not None
        assert "init_commands" in zsh_hooks
        
        commands = zsh_hooks["init_commands"]
        command_str = " ".join(commands)
        
        # Check that preexec and precmd functions are defined
        assert "preexec()" in command_str
        assert "precmd()" in command_str
    
    def test_fish_hooks_generation(self):
        """Test fish hook command generation."""
        hooks = ShellHooks()
        fish_hooks = hooks.get_shell_hooks("fish")
        
        assert fish_hooks is not None
        assert "init_commands" in fish_hooks
        
        commands = fish_hooks["init_commands"]
        command_str = " ".join(commands)
        
        # Check that fish event functions are defined
        assert "fish_preexec" in command_str
        assert "fish_prompt" in command_str
    
    def test_inject_hooks_bash(self):
        """Test hook injection for bash."""
        hooks = ShellHooks()
        injection = hooks.inject_hooks("bash")
        
        assert isinstance(injection, str)
        assert len(injection) > 0
        assert injection.endswith("\n")
        
        # Should contain hook setup commands
        assert "PROMPT_COMMAND" in injection or "trap" in injection
    
    def test_inject_hooks_unsupported(self):
        """Test hook injection for unsupported shell."""
        hooks = ShellHooks()
        injection = hooks.inject_hooks("sh")
        
        assert injection == ""
    
    def test_parse_osc_markers_empty(self):
        """Test OSC marker parsing with no markers."""
        data = b"hello world"
        cleaned, events = ShellHooks.parse_osc_markers(data)
        
        assert cleaned == data
        assert events == []
    
    def test_parse_osc_markers_single(self):
        """Test OSC marker parsing with single marker."""
        hooks = ShellHooks()
        
        # Create data with command start marker
        marker_bytes = hooks.OSC_COMMAND_START.encode('utf-8')
        data = b"before" + marker_bytes + b"after"
        
        cleaned, events = hooks.parse_osc_markers(data)
        
        assert marker_bytes not in cleaned  # Marker should be removed
        assert b"before" in cleaned
        assert b"after" in cleaned
        assert "command_start" in events
    
    def test_parse_osc_markers_multiple(self):
        """Test OSC marker parsing with multiple markers."""
        hooks = ShellHooks()
        
        # Create data with multiple markers
        start_marker = hooks.OSC_COMMAND_START.encode('utf-8')
        end_marker = hooks.OSC_COMMAND_END.encode('utf-8')
        data = start_marker + b"command output" + end_marker
        
        cleaned, events = hooks.parse_osc_markers(data)
        
        assert start_marker not in cleaned
        assert end_marker not in cleaned
        assert b"command output" in cleaned
        assert "command_start" in events
        assert "command_end" in events
        assert len(events) == 2
    
    def test_parse_osc_markers_invalid_utf8(self):
        """Test OSC marker parsing with invalid UTF-8."""
        # Create invalid UTF-8 data
        data = b"\xff\xfe invalid utf8"
        
        cleaned, events = ShellHooks.parse_osc_markers(data)
        
        # Should return original data if not valid UTF-8
        assert cleaned == data
        assert events == []
    
    def test_global_instance(self):
        """Test that global shell_hooks instance works."""
        assert shell_hooks is not None
        assert isinstance(shell_hooks, ShellHooks)
        
        # Should be able to use all methods
        assert shell_hooks.is_supported_shell("bash") is True
        bash_hooks = shell_hooks.get_shell_hooks("bash")
        assert bash_hooks is not None


class TestPTYBridgeHookIntegration:
    """Tests for PTY bridge integration with hooks."""
    
    def test_pty_bridge_hook_support_info(self):
        """Test that PTY bridge reports hook support in shell info."""
        from magic_shell.core.bridge import PTYBridge
        
        # Test with supported shell
        bridge = PTYBridge(shell_path="/bin/bash")
        info = bridge.get_shell_info()
        
        assert "hooks_supported" in info
        assert isinstance(info["hooks_supported"], bool)
    
    def test_pty_bridge_event_callbacks(self):
        """Test event callback registration in PTY bridge."""
        from magic_shell.core.bridge import PTYBridge
        
        bridge = PTYBridge()
        
        # Test callback registration
        callback_called = []
        def test_callback(event):
            callback_called.append(event)
        
        bridge.add_event_callback(test_callback)
        assert len(bridge.event_callbacks) == 1
        
        # Test event triggering
        bridge._trigger_event("test_event")
        assert callback_called == ["test_event"]
    
    def test_pty_bridge_event_callback_error_handling(self):
        """Test that callback errors don't break PTY bridge."""
        from magic_shell.core.bridge import PTYBridge
        
        bridge = PTYBridge()
        
        # Add callback that raises an error
        def bad_callback(event):
            raise ValueError("Test error")
        
        bridge.add_event_callback(bad_callback)
        
        # Should not raise an error
        bridge._trigger_event("test_event")


class TestThemeIntegration:
    """Tests for theme integration with timing events."""
    
    def test_theme_creation(self):
        """Test theme creation and configuration."""
        from magic_shell.core.theme import create_theme, AVAILABLE_THEMES
        
        # Test available themes
        assert "veil" in AVAILABLE_THEMES
        assert "ember" in AVAILABLE_THEMES
        assert "plain" in AVAILABLE_THEMES
        
        # Test theme creation
        theme = create_theme("veil")
        assert theme.theme_name == "veil"
        assert theme.effects_enabled is True
        
        plain_theme = create_theme("plain")
        assert plain_theme.effects_enabled is False
    
    def test_theme_event_methods(self):
        """Test that theme has all required event methods."""
        from magic_shell.core.theme import create_theme
        
        theme = create_theme("veil")
        
        # Should have all event handler methods
        assert hasattr(theme, "on_command_start")
        assert hasattr(theme, "on_command_end") 
        assert hasattr(theme, "on_prompt_start")
        assert hasattr(theme, "on_prompt_end")
        assert hasattr(theme, "show_startup_banner")
        
        # Methods should be callable (no errors for PR 3)
        theme.on_command_start()
        theme.on_command_end(0)
        theme.on_command_end(1)
        theme.on_prompt_start()
        theme.on_prompt_end()


class TestMainIntegrationPR3:
    """Integration tests for main entry point with hooks - PR 3."""
    
    def test_main_version_updated(self):
        """Test that version is updated to v0.4.0 for PR 4."""
        import subprocess
        import sys
        
        result = subprocess.run([
            sys.executable, "-m", "magic_shell.main", "--version"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "0.4.0" in result.stdout
    
    def test_main_with_theme_flags(self):
        """Test main with theme-related flags.""" 
        # This is a basic import test since we can't easily test full PTY in unit tests
        from magic_shell.main import main, _handle_timing_event
        from magic_shell.core.theme import create_theme
        
        # Test event handler function
        theme = create_theme("veil")
        
        # Should not raise errors
        _handle_timing_event(theme, "command_start")
        _handle_timing_event(theme, "command_end") 
        _handle_timing_event(theme, "prompt_start")
        _handle_timing_event(theme, "prompt_end")
        _handle_timing_event(theme, "unknown_event")  # Should be ignored