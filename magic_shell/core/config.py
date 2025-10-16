"""Configuration management for Magic Shell."""

import os
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

# Handle TOML parsing for different Python versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError(
            "tomli package is required for Python < 3.11. "
            "Install with: pip install tomli"
        )

from ..utils.colors import COLORS as colors


@dataclass
class ExecutorConfig:
    """Configuration for safe command execution."""
    
    allowed_commands: List[str]
    default_timeout: int = 30
    max_output_size: int = 1024 * 1024  # 1MB
    additional_env_vars: Dict[str, str] = None
    working_directory: str = None
    
    def __post_init__(self):
        if self.additional_env_vars is None:
            self.additional_env_vars = {}
        if self.working_directory is None:
            self.working_directory = os.getcwd()


@dataclass  
class ShellConfig:
    """Configuration for shell behavior."""
    
    wizard_mode_startup: bool = False
    show_welcome: bool = True
    enable_history: bool = True
    history_file: str = "~/.magic_shell_history"
    max_history_size: int = 1000
    auto_complete: bool = True
    color_output: bool = True


@dataclass
class MagicShellConfig:
    """Main configuration for Magic Shell."""
    
    executor: ExecutorConfig
    shell: ShellConfig
    version: str = "0.1.0"
    
    @classmethod
    def get_default(cls) -> 'MagicShellConfig':
        """Get default configuration."""
        default_commands = [
            'ls', 'cat', 'grep', 'find', 'head', 'tail', 'wc', 'sort', 'uniq',
            'pwd', 'whoami', 'date', 'echo', 'which', 'man', 'help',
            'git', 'python3', 'python', 'pip', 'pip3', 'node', 'npm',
            'tree', 'du', 'df', 'ps', 'top', 'htop', 'free', 'uptime',
            'curl', 'wget', 'ssh', 'scp', 'rsync', 'tar', 'zip', 'unzip'
        ]
        
        return cls(
            executor=ExecutorConfig(
                allowed_commands=default_commands,
                default_timeout=30,
                max_output_size=1024 * 1024,
                additional_env_vars={},
                working_directory=os.getcwd()
            ),
            shell=ShellConfig(
                wizard_mode_startup=False,
                show_welcome=True,
                enable_history=True,
                history_file="~/.magic_shell_history",
                max_history_size=1000,
                auto_complete=True,
                color_output=True
            )
        )


class ConfigManager:
    """Manages Magic Shell configuration."""
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.config_dir = Path.home() / ".config" / "magic-shell"
        self.config_file = self.config_dir / "config.toml"
        self.logger = logging.getLogger(__name__)
        
        # Current configuration
        self.config: MagicShellConfig = MagicShellConfig.get_default()
        
    def load_config(self) -> MagicShellConfig:
        """
        Load configuration from file or create default.
        
        Returns:
            MagicShellConfig: Loaded configuration
        """
        try:
            if self.config_file.exists():
                self.config = self._load_from_file()
                self.logger.info(f"Configuration loaded from {self.config_file}")
            else:
                self.logger.info("No config file found, using defaults")
                self._create_default_config()
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            print(f"{colors['yellow']}⚠️  Warning: Could not load config, using defaults{colors['end']}")
            self.config = MagicShellConfig.get_default()
            
        return self.config
    
    def _load_from_file(self) -> MagicShellConfig:
        """Load configuration from TOML file."""
        with open(self.config_file, 'rb') as f:
            config_data = tomllib.load(f)
        
        # Parse executor config
        executor_data = config_data.get('executor', {})
        executor_config = ExecutorConfig(
            allowed_commands=executor_data.get('allowed_commands', []),
            default_timeout=executor_data.get('default_timeout', 30),
            max_output_size=executor_data.get('max_output_size', 1024 * 1024),
            additional_env_vars=executor_data.get('additional_env_vars', {}),
            working_directory=executor_data.get('working_directory', os.getcwd())
        )
        
        # Parse shell config
        shell_data = config_data.get('shell', {})
        shell_config = ShellConfig(
            wizard_mode_startup=shell_data.get('wizard_mode_startup', False),
            show_welcome=shell_data.get('show_welcome', True),
            enable_history=shell_data.get('enable_history', True),
            history_file=shell_data.get('history_file', "~/.magic_shell_history"),
            max_history_size=shell_data.get('max_history_size', 1000),
            auto_complete=shell_data.get('auto_complete', True),
            color_output=shell_data.get('color_output', True)
        )
        
        return MagicShellConfig(
            executor=executor_config,
            shell=shell_config,
            version=config_data.get('version', "0.1.0")
        )
    
    def _create_default_config(self):
        """Create default configuration file."""
        try:
            # Create config directory
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate default config TOML
            config_toml = self._generate_config_toml(self.config)
            
            # Write to file
            with open(self.config_file, 'w') as f:
                f.write(config_toml)
                
            print(f"{colors['green']}✅ Created default config at {self.config_file}{colors['end']}")
            
        except Exception as e:
            self.logger.error(f"Could not create default config: {e}")
            print(f"{colors['red']}❌ Could not create config file: {e}{colors['end']}")
    
    def _generate_config_toml(self, config: MagicShellConfig) -> str:
        """Generate TOML configuration string."""
        return f"""# Magic Shell Configuration
# This file controls the behavior of Magic Shell
# Edit carefully and restart Magic Shell for changes to take effect

version = "{config.version}"

[shell]
# Shell behavior settings
wizard_mode_startup = {str(config.shell.wizard_mode_startup).lower()}
show_welcome = {str(config.shell.show_welcome).lower()}
enable_history = {str(config.shell.enable_history).lower()}
history_file = "{config.shell.history_file}"
max_history_size = {config.shell.max_history_size}
auto_complete = {str(config.shell.auto_complete).lower()}
color_output = {str(config.shell.color_output).lower()}

[executor]
# Safe execution settings
default_timeout = {config.executor.default_timeout}
max_output_size = {config.executor.max_output_size}
working_directory = "{config.executor.working_directory}"

# List of commands allowed for execution
# Add or remove commands as needed for your security requirements
allowed_commands = [
{self._format_command_list(config.executor.allowed_commands)}
]

# Additional environment variables for executed commands
[executor.additional_env_vars]
# Example: EDITOR = "nano"
# Example: PAGER = "less"
"""
    
    def _format_command_list(self, commands: List[str]) -> str:
        """Format command list for TOML."""
        formatted = []
        for i, cmd in enumerate(sorted(commands)):
            if i % 6 == 0:  # New line every 6 commands
                formatted.append(f'\n    "{cmd}"')
            else:
                formatted.append(f'"{cmd}"')
        return ', '.join(formatted)
    
    def save_config(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            config_toml = self._generate_config_toml(self.config)
            
            with open(self.config_file, 'w') as f:
                f.write(config_toml)
                
            print(f"{colors['green']}✅ Configuration saved to {self.config_file}{colors['end']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Could not save config: {e}")
            print(f"{colors['red']}❌ Could not save config: {e}{colors['end']}")
            return False
    
    def reload_config(self) -> MagicShellConfig:
        """
        Reload configuration from file.
        
        Returns:
            MagicShellConfig: Reloaded configuration
        """
        print(f"{colors['blue']}🔄 Reloading configuration...{colors['end']}")
        self.config = self.load_config()
        print(f"{colors['green']}✅ Configuration reloaded{colors['end']}")
        return self.config
    
    def get_config(self) -> MagicShellConfig:
        """Get current configuration."""
        return self.config
    
    def update_allowed_commands(self, commands: List[str]) -> None:
        """
        Update the allowed commands list.
        
        Args:
            commands: New list of allowed commands
        """
        self.config.executor.allowed_commands = commands
        
    def add_allowed_commands(self, commands: List[str]) -> None:
        """
        Add commands to the allowed list.
        
        Args:
            commands: Commands to add
        """
        current = set(self.config.executor.allowed_commands)
        current.update(commands)
        self.config.executor.allowed_commands = list(current)


# Global configuration manager
config_manager = ConfigManager()