"""Tests for enhanced UX features: safe execution and configuration."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, Mock

from magic_shell.core.executor import SafeExecutor
from magic_shell.core.config import ConfigManager, MagicShellConfig


class TestSafeExecutor:
    """Test the safe command execution system."""
    
    def test_safe_executor_initialization(self):
        """Test safe executor initializes with defaults."""
        executor = SafeExecutor()
        
        # Check default commands are loaded
        assert 'ls' in executor.whitelist
        assert 'cat' in executor.whitelist
        assert 'rm' not in executor.whitelist  # Should not be in default
        
    def test_command_whitelist_checking(self):
        """Test command whitelist validation."""
        executor = SafeExecutor()
        
        # Test allowed commands
        assert executor.is_command_allowed('ls -la')
        assert executor.is_command_allowed('cat file.txt')
        assert executor.is_command_allowed('git status')
        
        # Test disallowed commands  
        assert not executor.is_command_allowed('rm -rf /')
        assert not executor.is_command_allowed('sudo make install')
        assert not executor.is_command_allowed('/usr/bin/dangerous')
    
    def test_safe_command_execution(self):
        """Test safe command execution."""
        executor = SafeExecutor()
        
        # Test successful command
        exit_code, stdout, stderr = executor.execute_safe('echo "Hello World"')
        assert exit_code == 0
        assert "Hello World" in stdout
        assert stderr == ""
        
        # Test command with arguments
        exit_code, stdout, stderr = executor.execute_safe('date +%Y')
        assert exit_code == 0
        assert len(stdout.strip()) == 4  # Year should be 4 digits
        
    def test_disallowed_command_blocking(self):
        """Test that disallowed commands are blocked."""
        executor = SafeExecutor()
        
        # Should block dangerous commands
        exit_code, stdout, stderr = executor.execute_safe('rm -rf /', check_whitelist=True)
        assert exit_code == 1
        assert "not in the allowed commands list" in stderr
        
    def test_command_timeout(self):
        """Test command timeout functionality.""" 
        executor = SafeExecutor()
        
        # Add sleep to whitelist for this test
        executor.add_to_whitelist(['sleep'])
        
        # Test short timeout (this command should timeout)
        exit_code, stdout, stderr = executor.execute_safe('sleep 5', timeout=1)
        assert exit_code == 124  # Timeout exit code
        assert "timed out" in stderr
    
    def test_whitelist_management(self):
        """Test adding/removing commands from whitelist."""
        executor = SafeExecutor()
        
        # Add new command
        executor.add_to_whitelist(['mycommand'])
        assert 'mycommand' in executor.whitelist
        
        # Remove command
        executor.remove_from_whitelist(['mycommand'])
        assert 'mycommand' not in executor.whitelist


class TestConfigManager:
    """Test the configuration management system."""
    
    def test_default_config_creation(self):
        """Test default configuration creation."""
        config = MagicShellConfig.get_default()
        
        # Test default values
        assert config.version == "0.1.0"
        assert config.shell.show_welcome is True
        assert config.shell.enable_history is True
        assert config.executor.default_timeout == 30
        assert len(config.executor.allowed_commands) > 10  # Should have many default commands
        
    def test_config_manager_initialization(self):
        """Test config manager initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary config manager
            config_manager = ConfigManager()
            config_manager.config_dir = Path(temp_dir) / "magic-shell"
            config_manager.config_file = config_manager.config_dir / "config.toml"
            
            # Load config (should create default)
            config = config_manager.load_config()
            
            # Check config file was created
            assert config_manager.config_file.exists()
            assert isinstance(config, MagicShellConfig)
    
    def test_config_toml_generation(self):
        """Test TOML configuration file generation.""" 
        config_manager = ConfigManager()
        config = MagicShellConfig.get_default()
        
        toml_content = config_manager._generate_config_toml(config)
        
        # Check essential sections are present
        assert '[shell]' in toml_content
        assert '[executor]' in toml_content
        assert 'allowed_commands' in toml_content
        assert 'version = "0.1.0"' in toml_content


class TestIntegration:
    """Test integration between components."""
    
    def test_config_updates_executor(self):
        """Test that configuration updates affect executor."""
        # Create executor with custom config
        custom_config = {
            'allowed_commands': ['echo', 'date'],
            'default_timeout': 10
        }
        
        executor = SafeExecutor(custom_config)
        
        # Check config was applied
        assert executor.whitelist == {'echo', 'date'}
        assert executor.default_timeout == 10
        
        # Test that only allowed commands work
        assert executor.is_command_allowed('echo test')
        assert executor.is_command_allowed('date')
        assert not executor.is_command_allowed('ls')  # Not in custom whitelist