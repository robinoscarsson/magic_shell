# Changelog

All notable changes to Magic Shell will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-12-19

### Added
- 🧙‍♂️ **Wizard Mode**: Interactive spell-casting mode with magical commands
- 🎨 **Enhanced REPL**: Built with `prompt_toolkit` for superior user experience
- 📚 **Command Registry**: Decorator-based command system with auto-discovery
- 🛡️ **Safe Execution**: Whitelist-based command filtering with subprocess safety
- ⚙️ **TOML Configuration**: User configuration in `~/.config/magic-shell/config.toml`
- 📊 **Comprehensive Testing**: 20+ tests with pytest covering all major functionality
- 🏗️ **Modern Architecture**: Modular design with clear separation of concerns
- 📦 **CLI Package**: Installable via pip with `magic-shell` console entry point

### Features
- **Persistent History**: Commands automatically saved with full recall
- **Tab Completion**: Context-aware completion for commands and files
- **Colorized Output**: Beautiful terminal colors throughout the interface  
- **Graceful Exit**: Proper Ctrl+C/Ctrl+D handling without crashes
- **Runtime Reload**: Update configuration without restarting (`:reload`)
- **Command Whitelisting**: 39+ pre-approved safe commands
- **Timeout Protection**: Configurable command timeouts (default: 30s)
- **Output Limiting**: Prevent memory issues (max 1MB output per command)

### Spells Available
- `light` / `illuminatus_perpetuum`: Create magical light
- `fetch <pattern>`: Find files with magical search
- `time` / `tempus`: Display current time with flair
- `fortune` / `wisdom`: Get mystical wisdom and quotes
- `teleport <path>`: Navigate directories with style
- `scry <command>`: Preview command without execution
- `transmute <file>`: Display file contents with syntax highlighting
- `divination <query>`: Search through command history

### Security Features
- Command argument sanitization with `shlex`
- Minimal environment variable exposure
- Working directory controls
- Safe subprocess execution patterns
- User-configurable command whitelist

### Development Tools
- **Code Quality**: `ruff`, `black`, `mypy` integration
- **CI/CD**: GitHub Actions with multi-Python version testing (3.8-3.12)
- **Documentation**: Comprehensive README with examples
- **Testing**: Full test coverage including edge cases

## [0.1.0] - 2024-12-19

### Added
- Initial Magic Shell implementation
- Basic REPL functionality
- Simple command execution
- Wizard spells system
- Colorized terminal output
- Basic history management

---

**Magic Shell** - Where technology meets magic ✨

[Unreleased]: https://github.com/robinoscarsson/magic_shell/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/robinoscarsson/magic_shell/releases/tag/v1.0.0
[0.1.0]: https://github.com/robinoscarsson/magic_shell/releases/tag/v0.1.0