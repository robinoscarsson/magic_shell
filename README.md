````markdown
# 🧙‍♂️ Magic Shell

[![CI](https://github.com/robinoscarsson/magic_shell/workflows/CI/badge.svg)](https://github.com/robinoscarsson/magic_shell/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A whimsical yet powerful command-line shell that combines magical aesthetics with enterprise-grade features. Magic Shell enhances your terminal experience with colorful visuals, safe command execution, and an extensible spell system.

## ✨ Features

### 🎨 **Enhanced User Experience**
- **Magical Interface**: Colorful welcome screens with ASCII art and inspirational quotes
- **Advanced REPL**: Built with `prompt_toolkit` for superior input handling
- **Persistent History**: Commands automatically saved with full history recall
- **Smart Tab Completion**: Context-aware completion for commands, spells, and directories
- **Graceful Interruption**: Proper Ctrl+C/Ctrl+D handling without crashes

### 🧙‍♂️ **Wizard Mode & Spells**
- **Wizard Mode**: Cast special spell commands with magical flair
- **Extensible Spell System**: Easy-to-add spells using `@command` decorators
- **Spell Aliases**: Multiple names for spells (`light` for `illuminatus_perpetuum`)
- **Auto-Discovery**: New spells automatically detected and integrated

### 🛡️ **Security & Safety**
- **Safe Command Execution**: Whitelist-based command filtering (39+ safe commands)
- **Subprocess Security**: Proper argument escaping with `shlex`
- **Configurable Timeouts**: Prevent runaway processes (default: 30s)
- **Output Limiting**: Prevent memory issues (max 1MB output)
- **Environment Control**: Minimal, secure environment variables

### ⚙️ **Configuration & Customization**
- **TOML Configuration**: User settings in `~/.config/magic-shell/config.toml`
- **Runtime Reload**: Update config without restarting with `:reload`
- **Customizable Behavior**: Shell appearance, timeouts, allowed commands
- **User-Friendly Defaults**: Works out-of-the-box with sensible settings

## 🪄 Installation

### From PyPI (Recommended)
```bash
pip install magic-shell
```

### From Source
```bash
git clone https://github.com/robinoscarsson/magic_shell.git
cd magic_shell
pip install -e .
```

### Requirements
- Python 3.8+ 
- Linux, macOS, or Windows
- Terminal with color support (most modern terminals)

## � Quick Start

Launch Magic Shell after installation:

```bash
magic-shell
```

You'll be greeted with a magical welcome screen! Try these commands:

```bash
# Get help (context-aware based on current mode)
help

# Execute safe commands  
ls -la
echo "Hello, Magic Shell!"

# Enter wizard mode for spell casting
wizard

# Cast some spells (in wizard mode)
light                    # Create magical light
fetch README            # Find files magically  
time                    # Show current time with flair
fortune                 # Get mystical wisdom

# Return to normal mode
normal

# Configure Magic Shell
config                  # Show current configuration
config edit            # Edit config file
allowed                 # Show allowed commands
allowed add mycommand   # Add command to whitelist

# Exit gracefully  
:quit
```

## 📚 Command Reference

### 🔧 **System Commands**
| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show context-aware help | `help` |
| `exit`, `quit`, `:quit` | Exit Magic Shell | `:quit` |
| `cd <path>` | Change directory with feedback | `cd /home/user` |
| `config` | Show/edit configuration | `config`, `config edit` |
| `allowed` | Manage command whitelist | `allowed`, `allowed add git` |
| `safe <command>` | Execute with explicit safety | `safe ls -la` |
| `:reload` | Reload configuration | `:reload` |

### 🧙‍♂️ **Magic Commands** 
| Command | Description |
|---------|-------------|
| `wizard` | Enter wizard mode for spell casting |
| `normal` | Exit wizard mode |

### ✨ **Available Spells** (Wizard Mode Only)
| Spell | Aliases | Description |
|-------|---------|-------------|
| `illuminatus_perpetuum` | `light` | Create magical light effect |
| `opendoorus_immedius` | `open` | Open files/directories with flair |
| `fetchum_fileium` | `fetch` | Find files with magical search |
| `antigravitonia_selectivus` | `float` | Levitate text against gravity |
| `time` | `clock` | Display time with magical effects |
| `fortune` | `wisdom`, `oracle` | Dispense mystical wisdom |

### 📝 **History & Navigation**
| Command | Description |
|---------|-------------|
| `history` | Show command history |
| `!<number>` | Execute command from history |
| ↑/↓ arrows | Navigate command history |
| Tab | Auto-complete commands/paths |

## ⚙️ Configuration

Magic Shell uses a TOML configuration file located at `~/.config/magic-shell/config.toml`. The file is created automatically with sensible defaults on first run.

### Configuration Sections

```toml
[shell]
wizard_mode_startup = false    # Start in wizard mode
show_welcome = true           # Display welcome screen
enable_history = true         # Enable command history
history_file = "~/.magic_shell_history"
max_history_size = 1000      # Maximum history entries
auto_complete = true         # Enable tab completion
color_output = true          # Enable colorized output

[executor]
default_timeout = 30         # Command timeout in seconds
max_output_size = 1048576   # Max output size (1MB)
working_directory = "."     # Default working directory

# Whitelist of allowed commands
allowed_commands = [
    "ls", "cat", "grep", "find", "echo", "git", "python3",
    # ... see config file for full list
]
```

### Runtime Configuration
```bash
config              # Show current settings
config edit         # Edit configuration file  
config path         # Show config file location
:reload             # Reload config without restart
```

## 🛡️ Security Features

Magic Shell prioritizes security while maintaining usability:

- **Command Whitelisting**: Only pre-approved commands can execute
- **Argument Sanitization**: All command arguments properly escaped
- **Timeout Protection**: Commands auto-terminate after timeout
- **Output Limiting**: Prevents memory exhaustion attacks
- **Safe Environment**: Minimal environment variables passed to subprocesses

### Managing Allowed Commands
```bash
allowed                    # Show current whitelist
allowed add mycommand      # Add command to whitelist  
allowed remove dangerous   # Remove command from whitelist
```

## 🧩 Architecture

Magic Shell uses a modern, modular architecture:

```
magic_shell/
├── main.py                    # CLI entry point
├── core/                      # Core framework
│   ├── shell.py              # Main shell with prompt_toolkit
│   ├── commands.py           # Command handlers  
│   ├── registry.py           # Command registration system
│   ├── executor.py           # Safe subprocess execution
│   ├── config.py             # TOML configuration management
│   └── history.py            # Command history
├── spells/                    # Extensible spell system  
│   ├── wizard.py             # Core spells
│   └── demo.py               # Example spells
├── utils/                     # Utilities
│   ├── welcome.py            # Welcome screen
│   ├── colors.py             # Color constants
│   └── prompt.py             # Prompt formatting
└── tests/                     # Comprehensive test suite
```

## 🌟 Extending Magic Shell

Adding new commands and spells is incredibly simple with the `@command` decorator:

### Adding a New Spell
```python
# In magic_shell/spells/my_spells.py
from ..core.registry import command
from ..utils.colors import COLORS as colors

@command("my_spell", "Description of my spell", 
         aliases=["ms"], category="Custom", wizard_only=True)
def my_custom_spell(*args):
    """My custom spell implementation."""
    print(f"{colors['purple']}✨ Casting my custom spell!{colors['end']}")
    # Your spell logic here
```

### Adding a System Command  
```python
# In magic_shell/core/commands.py or separate module
@command("my_command", "Description of command", category="System")
def my_system_command(*args):
    """My system command implementation.""" 
    # Your command logic here
```

The command registry automatically discovers and integrates new commands when their modules are imported!

## 🧪 Development

### Setting Up Development Environment
```bash
# Clone and setup
git clone https://github.com/robinoscarsson/magic_shell.git
cd magic_shell

# Install in development mode with test dependencies
pip install -e ".[dev]"

# Or install dependencies manually
pip install -e .
pip install pytest ruff black mypy
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=magic_shell --cov-report=html

# Run specific tests
pytest tests/test_shell.py -v

# Run linting
ruff check magic_shell/
black --check magic_shell/
mypy magic_shell/
```

### Code Quality
Magic Shell maintains high code quality standards:
- **Linting**: `ruff` for fast Python linting  
- **Formatting**: `black` for consistent code style
- **Type Checking**: `mypy` for static type analysis
- **Testing**: Comprehensive `pytest` test suite (20+ tests)
- **CI/CD**: GitHub Actions with multi-Python version testing

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Workflow
1. **Fork** the repository on GitHub
2. **Clone** your fork: `git clone https://github.com/yourusername/magic_shell.git`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Install** development dependencies: `pip install -e ".[dev]"`
5. **Make** your changes with tests
6. **Test** your changes: `pytest` and code quality checks
7. **Commit** your changes: `git commit -m 'Add amazing feature'`
8. **Push** to your branch: `git push origin feature/amazing-feature`
9. **Create** a Pull Request

### Contribution Guidelines
- **Write Tests**: All new features need test coverage
- **Follow Code Style**: Use `black` formatting and `ruff` linting
- **Update Documentation**: Update README.md and docstrings
- **Small Commits**: Make focused, atomic commits with clear messages
- **Spell Documentation**: New spells need help text and examples

### Areas for Contribution  
- 🧙‍♂️ **New Spells**: Creative magical commands
- 🛡️ **Security Enhancements**: Improved safety features
- 🎨 **UI/UX Improvements**: Better prompts, colors, animations
- 📖 **Documentation**: Tutorials, examples, API docs
- 🧪 **Testing**: Additional test cases and scenarios
- ⚡ **Performance**: Optimization and profiling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **prompt_toolkit** for the excellent REPL framework
- **tomli/tomllib** for TOML configuration parsing  
- The Python community for creating amazing tools
- All the wizards who believe in the magic of good software

## 📊 Changelog

### v1.0.0 (Current)
- ✨ Initial release with full feature set
- 🧙‍♂️ Wizard mode and spell system
- 🛡️ Safe command execution with whitelisting
- ⚙️ TOML configuration management
- 📚 Comprehensive test suite
- 🎨 Enhanced REPL with prompt_toolkit
- 📦 Installable CLI package

---

*"Any sufficiently advanced technology is indistinguishable from magic."* - Arthur C. Clarke

**Made with 🧙‍♂️ magic and ☕ coffee**

## 🔮 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🧙‍♀️ Acknowledgments

- The ASCII art wizards, books, and crystal balls that make our shell magical
- Terry Pratchett, whose Discworld series inspired our magical style
- Everyone who believes in the power of command-line magic

---

*"Those who don't believe in magic will never find it." — Roald Dahl*
