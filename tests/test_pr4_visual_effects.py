"""Tests for Magic Shell PR 4: Visual effects + config + safety."""

import os
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
from rich.console import Console

from magic_shell.core.config import (
    MagicShellConfig, 
    EffectsConfig, 
    ShellConfig, 
    SafetyConfig,
    load_config,
    save_config,
    is_password_prompt,
    is_safe_environment,
    get_config_dir,
    get_config_file
)
from magic_shell.core.theme import (
    MagicTheme,
    VeilTheme,
    EmberTheme,
    PlainTheme,
    create_theme,
    AVAILABLE_THEMES
)


class TestMagicShellConfig:
    """Test configuration system."""
    
    def test_default_config_creation(self):
        """Test creating default configuration."""
        config = MagicShellConfig()
        
        assert config.effects.enabled is True
        assert config.effects.theme == "veil"
        assert config.effects.intensity == 0.7
        assert config.shell.show_welcome is True
        assert config.safety.password_detection is True
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test invalid theme
        config = MagicShellConfig(
            effects=EffectsConfig(theme="invalid")
        )
        assert config.effects.theme == "veil"  # Should fallback
        
        # Test intensity clamping
        config = MagicShellConfig(
            effects=EffectsConfig(intensity=1.5)
        )
        assert config.effects.intensity == 1.0
        
        config = MagicShellConfig(
            effects=EffectsConfig(intensity=-0.5)
        )
        assert config.effects.intensity == 0.0
        
        # Test duration clamping
        config = MagicShellConfig(
            effects=EffectsConfig(duration_ms=50)
        )
        assert config.effects.duration_ms == 100  # Minimum
        
        config = MagicShellConfig(
            effects=EffectsConfig(duration_ms=10000)
        )
        assert config.effects.duration_ms == 5000  # Maximum
    
    def test_config_file_operations(self):
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.toml"
            
            # Create test config
            config = MagicShellConfig(
                effects=EffectsConfig(
                    theme="ember",
                    intensity=0.5,
                    git_badge=True
                ),
                shell=ShellConfig(
                    show_welcome=False,
                    hook_injection=False
                )
            )
            
            # Mock get_config_file to use our temp file
            with patch("magic_shell.core.config.get_config_file", return_value=config_file):
                save_config(config)
                assert config_file.exists()
                
                # Load back and verify
                loaded_config = load_config()
                assert loaded_config.effects.theme == "ember"
                assert loaded_config.effects.intensity == 0.5
                assert loaded_config.effects.git_badge is True
                assert loaded_config.shell.show_welcome is False


class TestSafetyFeatures:
    """Test safety and password detection features."""
    
    def test_password_detection(self):
        """Test password prompt detection."""
        # Positive cases
        assert is_password_prompt("Password:")
        assert is_password_prompt("Enter password for user:")
        assert is_password_prompt("[sudo] password for robin:")
        assert is_password_prompt("Please enter password:")
        assert is_password_prompt("SSH password:")
        assert is_password_prompt("Enter passphrase:")
        
        # Negative cases
        assert not is_password_prompt("Welcome to the shell")
        assert not is_password_prompt("robin@machine:~$ ")
        assert not is_password_prompt("ls -la")
        assert not is_password_prompt("error: command not found")
    
    @patch.dict(os.environ, {}, clear=True)
    def test_safe_environment_detection(self):
        """Test safe environment detection."""
        # Clean environment should be safe
        assert is_safe_environment() is True
        
        # SSH connection should be unsafe
        with patch.dict(os.environ, {"SSH_CONNECTION": "192.168.1.1 52345 192.168.1.100 22"}):
            assert is_safe_environment() is False
            
        with patch.dict(os.environ, {"SSH_CLIENT": "192.168.1.1 52345 22"}):
            assert is_safe_environment() is False
        
        # TMUX should be unsafe
        with patch.dict(os.environ, {"TMUX": "/tmp/tmux-1000/default,12345,0"}):
            assert is_safe_environment() is False
            
        # Screen should be unsafe
        with patch.dict(os.environ, {"STY": "12345.pts-1.hostname"}):
            assert is_safe_environment() is False


class TestThemeSystem:
    """Test theme system and visual effects."""
    
    def test_theme_creation(self):
        """Test creating different themes."""
        # Test all available themes
        for theme_name in AVAILABLE_THEMES:
            theme = create_theme(theme_name)
            assert theme.name == theme_name
            
        # Test invalid theme fallback
        theme = create_theme("invalid")
        assert theme.name == "veil"
    
    def test_theme_types(self):
        """Test specific theme implementations."""
        config = MagicShellConfig()
        
        veil = create_theme("veil", config)
        assert isinstance(veil, VeilTheme)
        assert veil._effects_enabled is True
        
        ember = create_theme("ember", config)
        assert isinstance(ember, EmberTheme)
        assert ember._effects_enabled is True
        
        plain = create_theme("plain", config)
        assert isinstance(plain, PlainTheme)
        assert plain._effects_enabled is False
    
    @patch("rich.console.Console.print")
    def test_theme_startup_banner(self, mock_print):
        """Test theme startup banner display."""
        config = MagicShellConfig()
        theme = VeilTheme(config)
        
        shell_info = {
            "version": "0.4.0",
            "shell": "bash",
            "hooks_supported": True
        }
        
        theme.on_startup(shell_info)
        mock_print.assert_called_once()
        
        # Test disabled banner
        config.shell.startup_banner = False
        theme = VeilTheme(config)
        mock_print.reset_mock()
        
        theme.on_startup(shell_info)
        mock_print.assert_not_called()
    
    def test_effect_safety_checks(self):
        """Test effect safety and password mode."""
        config = MagicShellConfig()
        theme = VeilTheme(config)
        
        # Normal text should allow effects
        assert theme._should_show_effects("normal command") is True
        
        # Password prompt should disable effects
        assert theme._should_show_effects("Password:") is False
        assert theme._password_mode is True
        
        # After password mode, prompt_start should reset it
        theme.on_prompt_start()
        assert theme._password_mode is False
        assert theme._should_show_effects("normal command") is True
    
    @patch("rich.console.Console.print")
    @patch("time.sleep")
    def test_veil_theme_effects(self, mock_sleep, mock_print):
        """Test VeilTheme visual effects."""
        config = MagicShellConfig()
        theme = VeilTheme(config)
        
        # Test command shimmer
        theme.on_command_start("ls -la")
        assert mock_print.call_count >= 1  # Shimmer and clear
        
        mock_print.reset_mock()
        
        # Test success glow (quick command)
        theme.on_command_end("ls -la", 0)
        mock_print.assert_called_once()
        
        mock_print.reset_mock()
        
        # Test error pulse
        theme.on_command_end("false", 1)
        mock_print.assert_called_once()
    
    @patch("subprocess.run")
    def test_git_badge_integration(self, mock_run):
        """Test git badge functionality."""
        config = MagicShellConfig(
            effects=EffectsConfig(git_badge=True)
        )
        theme = VeilTheme(config)
        
        # Mock successful git command
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "main\n"
        mock_run.return_value = mock_result
        
        git_info = theme._get_git_info()
        assert git_info == {"branch": "main"}
        
        # Test disabled git badge
        config.effects.git_badge = False
        git_info = theme._get_git_info()
        assert git_info is None
        
        # Test git command failure
        config.effects.git_badge = True
        mock_result.returncode = 1
        git_info = theme._get_git_info()
        assert git_info is None


class TestMainIntegrationPR4:
    """Test main.py integration with PR 4 features."""
    
    @patch("magic_shell.main.asyncio.run")
    @patch("magic_shell.main.PTYBridge")
    @patch("magic_shell.main.get_config")
    def test_main_with_config_integration(self, mock_get_config, mock_bridge_class, mock_asyncio_run):
        """Test main() integration with configuration."""
        from magic_shell.main import main
        
        # Mock configuration
        mock_config = MagicShellConfig(
            effects=EffectsConfig(theme="ember", enabled=True),
            shell=ShellConfig(show_welcome=True)
        )
        mock_get_config.return_value = mock_config
        
        # Mock bridge
        mock_bridge = Mock()
        mock_bridge_class.return_value = mock_bridge
        mock_asyncio_run.return_value = 0
        
        # Test with default arguments
        with patch("sys.argv", ["magic-shell"]):
            exit_code = main()
            
        assert exit_code == 0
        mock_bridge_class.assert_called_once()
        mock_bridge.add_event_callback.assert_called_once()
    
    @patch("magic_shell.main.get_config_dir")
    def test_config_dir_flag(self, mock_get_config_dir):
        """Test --config-dir flag."""
        from magic_shell.main import main
        
        mock_get_config_dir.return_value = Path("/home/user/.config/magic-shell")
        
        with patch("sys.argv", ["magic-shell", "--config-dir"]):
            with patch("builtins.print") as mock_print:
                exit_code = main()
                
        assert exit_code == 0
        mock_print.assert_called_with(Path("/home/user/.config/magic-shell"))
    
    def test_theme_cli_override(self):
        """Test theme selection via CLI arguments."""
        from magic_shell.main import main
        
        test_cases = [
            (["--plain"], "plain"),
            (["--no-effects"], "plain"),
            (["--theme", "ember"], "ember"),
            (["--theme", "veil"], "veil"),
        ]
        
        for args, expected_theme in test_cases:
            with patch("sys.argv", ["magic-shell"] + args):
                with patch("magic_shell.main.create_theme") as mock_create_theme:
                    with patch("magic_shell.main.asyncio.run", return_value=0):
                        with patch("magic_shell.main.PTYBridge"):
                            main()
                            
                mock_create_theme.assert_called()
                actual_theme = mock_create_theme.call_args[0][0]
                assert actual_theme == expected_theme


class TestVersionAndMetadata:
    """Test version handling and metadata."""
    
    def test_version_consistency(self):
        """Test version consistency across files."""
        from magic_shell import __version__
        
        # Version should be 0.4.0 for PR 4
        assert __version__ == "0.4.0"
        
        # Test main.py version flag
        from magic_shell.main import main
        
        with patch("sys.argv", ["magic-shell", "--version"]):
            with pytest.raises(SystemExit):  # argparse calls sys.exit on --version
                main()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])