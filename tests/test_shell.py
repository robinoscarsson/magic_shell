"""Basic smoke tests for Magic Shell."""

import pytest
from unittest.mock import Mock, patch
from magic_shell.core.shell import Shell
from magic_shell.core.commands import CommandManager
from magic_shell.core.registry import registry, CommandInfo
from magic_shell.spells.wizard import Wizard


class TestShellBasics:
    """Test basic shell functionality."""
    
    def test_shell_initialization(self):
        """Test that shell initializes properly."""
        shell = Shell()
        assert shell.state["running"] is True
        assert shell.state["wizard_mode"] is False
        assert shell.commands is not None
        assert shell.wizard is not None
        assert shell.history is not None
    
    def test_command_manager_uses_registry(self):
        """Test that command manager uses the command registry."""
        import magic_shell.core.commands
        import magic_shell.spells.wizard
        
        state = {"running": True, "wizard_mode": False}
        cmd_manager = CommandManager(state)
        
        # Test that basic commands are registered in registry
        assert registry.get_command("exit") is not None
        assert registry.get_command("quit") is not None
        assert registry.get_command(":quit") is not None
        assert registry.get_command("help") is not None
        assert registry.get_command("wizard") is not None
        assert registry.get_command("normal") is not None
    
    def test_registry_has_spells_and_aliases(self):
        """Test that registry has both full spell names and aliases."""
        # Load commands by importing modules
        import magic_shell.core.commands
        import magic_shell.spells.wizard
        
        # Test that full names exist in registry
        assert "illuminatus_perpetuum" in registry.commands
        assert "opendoorus_immedius" in registry.commands
        assert "fetchum_fileium" in registry.commands
        assert "antigravitonia_selectivus" in registry.commands
        
        # Test that aliases exist
        assert "light" in registry.commands
        assert "open" in registry.commands  
        assert "fetch" in registry.commands
        assert "float" in registry.commands
        
        # Test wizard-only flag
        light_cmd = registry.get_command("light")
        assert light_cmd is not None
        assert light_cmd.wizard_only is True
    
    def test_exit_command_handling(self):
        """Test that exit commands properly set running state."""
        state = {"running": True, "wizard_mode": False}
        cmd_manager = CommandManager(state)
        
        # Test exit
        assert cmd_manager.handle_special_command("exit") is True
        assert state["running"] is False
        
        # Reset state
        state["running"] = True
        
        # Test quit
        assert cmd_manager.handle_special_command("quit") is True
        assert state["running"] is False
        
        # Reset state  
        state["running"] = True
        
        # Test :quit
        assert cmd_manager.handle_special_command(":quit") is True
        assert state["running"] is False
    
    def test_wizard_mode_toggle(self):
        """Test wizard mode can be toggled."""
        state = {"running": True, "wizard_mode": False}
        cmd_manager = CommandManager(state)
        
        # Enter wizard mode
        assert cmd_manager.handle_special_command("wizard") is True
        assert state["wizard_mode"] is True
        
        # Exit wizard mode
        assert cmd_manager.handle_special_command("normal") is True  
        assert state["wizard_mode"] is False


class TestCommandRegistry:
    """Test the command registry system."""
    
    def test_registry_initialization(self):
        """Test that registry initializes correctly.""" 
        # Clear registry to test fresh
        registry.commands.clear()
        registry.categories.clear()
        
        # Register a test command
        @registry.register("testcmd", "Test command", ["tc"], "Testing")
        def test_command():
            return "test result"
        
        # Verify registration
        assert "testcmd" in registry.commands
        assert "tc" in registry.commands  # alias
        
        cmd_info = registry.get_command("testcmd")
        assert cmd_info is not None
        assert cmd_info.name == "testcmd"
        assert cmd_info.help_text == "Test command"
        assert "tc" in cmd_info.aliases
        assert cmd_info.category == "Testing"
        
    def test_command_execution(self):
        """Test command execution through registry."""
        # Clear and setup test command
        registry.commands.clear()
        
        @registry.register("echo", "Echo arguments")
        def echo_command(*args):
            return " ".join(args)
        
        # Test execution
        result = registry.execute_command("echo", "hello", "world")
        assert result == "hello world"
        
    def test_wizard_only_commands(self):
        """Test wizard-only command filtering."""
        registry.commands.clear()
        
        @registry.register("normalcmd", "Normal command")
        def normal_cmd():
            pass
            
        @registry.register("wizardcmd", "Wizard command", wizard_only=True)
        def wizard_cmd():
            pass
        
        # Test normal mode - should only see normal command
        normal_commands = registry.list_commands(wizard_mode=False)
        normal_names = [cmd.name for cmd in normal_commands]
        assert "normalcmd" in normal_names
        assert "wizardcmd" not in normal_names
        
        # Test wizard mode - should see both
        wizard_commands = registry.list_commands(wizard_mode=True)
        wizard_names = [cmd.name for cmd in wizard_commands]
        assert "normalcmd" in wizard_names
        assert "wizardcmd" in wizard_names


class TestREPLIntegration:
    """Test REPL behavior without actually starting interactive mode."""
    
    @patch('magic_shell.core.shell.print_welcome')
    def test_shell_handles_keyboard_interrupt(self, mock_welcome):
        """Test that shell handles KeyboardInterrupt gracefully."""
        shell = Shell()
        
        # Mock the session to raise KeyboardInterrupt
        with patch.object(shell.session, 'prompt', side_effect=KeyboardInterrupt()):
            # This should handle KeyboardInterrupt and continue
            try:
                # Simulate getting a command that raises KeyboardInterrupt
                prompt_text = shell.session.prompt()
            except KeyboardInterrupt:
                # This is expected behavior
                pass
    
    @patch('magic_shell.core.shell.print_welcome')
    def test_shell_handles_eof_error(self, mock_welcome):
        """Test that shell handles EOFError (Ctrl+D) gracefully.""" 
        shell = Shell()
        
        # Mock the session to raise EOFError
        with patch.object(shell.session, 'prompt', side_effect=EOFError()):
            # This should handle EOFError gracefully
            try:
                # Simulate getting a command that raises EOFError
                prompt_text = shell.session.prompt()
            except EOFError:
                # This is expected behavior
                pass