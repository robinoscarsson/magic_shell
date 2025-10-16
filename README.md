# � Magic Shell

[![CI](https://github.com/robinoscarsson/magic_shell/workflows/CI/badge.svg)](https://github.com/robinoscarsson/magic_shell/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A magical wrapper around your real shell** - adds cosmetic effects and subtle enhancements while preserving 100% compatibility with your existing workflow.

## 🌟 Why Magic Shell?

Your shell is perfect. Your tools work flawlessly. Your muscle memory is intact. 

Magic Shell doesn't replace anything - it simply adds a **thin layer of visual magic** around your existing shell experience. Think of it as a beautiful, non-intrusive overlay that makes your terminal sessions more delightful without changing how anything actually works.

### ✨ What Magic Shell Does
- **Wraps your real shell** (bash, zsh, fish) in a PTY bridge with zero interference
- **Adds subtle visual effects** - gentle glows after successful commands, discrete notifications
- **Preserves everything** - all keybindings, tools (vim, git, ssh, htop), and behaviors work identically
- **Respects privacy** - never logs sensitive input, disables effects during password prompts
- **Stays invisible** - near-zero overhead, fast startup, smooth typing

### 🚫 What Magic Shell Doesn't Do
- No custom commands or "spell casting"
- No command replacement or interception  
- No breaking changes to your workflow
- No learning curve or new syntax
- No performance impact on your daily tools

## 🚀 Install

### Prerequisites
- **Python 3.12+**
- **Unix-like system** (Linux, macOS) with PTY support
- **Windows**: WSL recommended, otherwise limited "prompt-only" mode

### Installation
```bash
# Install from PyPI (coming soon)
pip install magic-shell

# Or install from source
git clone https://github.com/robinoscarsson/magic_shell.git
cd magic_shell
pip install -e .
```

## � Quick Start

```bash
# Launch Magic Shell (wraps your default shell)
magic-shell

# Everything works exactly like normal
ls -la
git status
vim myfile.txt
ssh user@server
htop

# Optional: customize the magic
magic-shell --theme ember
magic-shell --plain          # Disable all effects
magic-shell --shell /bin/zsh # Use specific shell
```

### Configuration
Magic Shell creates `~/.config/magic-shell/config.toml` with sensible defaults:

```toml
# Visual theme: "veil" | "ember" | "plain" 
theme = "veil"

[effects]
success = "burst"    # Effect after successful commands (rc=0)
fail = "rift"        # Effect after failed commands (rc≠0)

[behavior]
stage = false        # Enable experimental features
telemetry = "off"    # Never enabled by default
```

## � How It Works

Magic Shell uses a **PTY (pseudo-terminal) bridge** to wrap your existing shell:

1. **Spawns your login shell** inside a proper PTY
2. **Forwards everything** - keystrokes, output, signals (Ctrl-C), window resizes
3. **Injects timing hooks** using shell-specific mechanisms (bash `PROMPT_COMMAND`, zsh `preexec/precmd`)
4. **Detects command boundaries** via invisible OSC escape sequences
5. **Applies cosmetic effects** at precise moments without interfering

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Your Input    │ ──▶│   Magic Shell   │ ──▶│   Real Shell    │
│                 │    │   (PTY Bridge)  │    │   (bash/zsh)    │
│  Terminal App   │ ◀── │  + Visual FX   │ ◀── │  + Your Tools   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

This approach ensures **perfect compatibility** - if it works in your shell, it works in Magic Shell.

## ⚡ Performance

- **Startup**: < 50ms typical
- **Overhead**: < 1ms per command
- **Memory**: ~ 10MB baseline
- **CPU**: Negligible during normal use

Raw bytes are forwarded without unnecessary encoding/decoding. Effects are triggered asynchronously and never block your commands.

## 🛡️ Safety & Privacy

- **No command logging** - your input/output stays private
- **Password detection** - effects disabled during no-echo prompts  
- **Signal preservation** - Ctrl-C, Ctrl-Z work exactly as expected
- **Exit code preservation** - command failures propagate correctly
- **Minimal dependencies** - only `prompt-toolkit` and `rich`

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

## 🧪 Development

```bash
# Setup development environment
git clone https://github.com/robinoscarsson/magic_shell.git
cd magic_shell
pip install -e ".[dev]"

# Run tests
pytest

# Lint code
ruff check magic_shell/
ruff format magic_shell/

# Integration tests (requires external tools)
pytest -m integration  # Tests with vim, less, ssh if available
```

## 🤝 Contributing

We welcome contributions! Key areas:

- **New themes** - create beautiful, subtle visual effects
- **Shell support** - extend hooks for fish, nushell, etc.
- **Platform support** - improve Windows/WSL integration
- **Performance** - optimize the PTY bridge and effect rendering
- **Testing** - expand integration test coverage

## 📋 Roadmap

- **v0.2**: PTY bridge + basic shell detection
- **v0.3**: Shell hooks + precise command timing  
- **v0.4**: Visual effects + themes + config system
- **v0.5**: Integration tests + Windows support
- **v1.0**: Production ready + PyPI release

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

*"Any sufficiently advanced terminal is indistinguishable from magic."*

**Made with ✨ and respect for your existing workflow**

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
