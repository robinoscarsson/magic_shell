# 🧙‍♂️ Magic Shell

A whimsical command-line shell with magical powers! Magic Shell enhances your terminal experience with colorful visuals, special "spells," and user-friendly features.

## ✨ Features

- **Magical Interface**: Colorful welcome screens with ASCII art and inspirational quotes
- **Wizard Mode**: Cast special spell commands for enhanced functionality
- **Command History**: Easily recall and reuse previous commands
- **Tab Completion**: Quickly complete commands, spells, and directory names
- **Color Output**: Beautiful color-coded messages and prompts

## 🪄 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/magic_shell.git
   cd magic_shell
   ```

2. Make sure you have Python 3.6+ installed:
   ```bash
   python3 --version
   ```

3. Run the shell:
   ```bash
   python3 main.py
   ```

## 📚 Usage

### Basic Commands

- `help` - Display available commands
- `exit` or `quit` - Exit the shell
- `cd <directory>` - Change directory
- `history` - View command history
- `!<number>` - Execute a command from history by its number

### Wizard Mode

Enter wizard mode to cast magical spells:

```
wizard
```

Available spells:
- `lumos` - Creates a magical light (clears the screen)
- `alohomora <file/directory>` - Opens files or directories
- `accio <pattern>` - Fetches files matching a pattern
- `wingardium <text>` - Levitates text on the screen

To exit wizard mode:

```
normal
```

## 🧩 Project Structure

```
magic_shell/
├── main.py                  # Entry point
├── core/                    # Core functionality
│   ├── shell.py             # Main shell functionality
│   ├── commands.py          # Command handling
│   └── history.py           # History management
├── spells/                  # Wizard mode functionality
│   └── wizard.py            # Spell casting and wizard logic
└── utils/                   # Helper utilities
    ├── welcome.py           # Welcome screen
    ├── colors.py            # Color definitions
    └── prompt.py            # Prompt formatting
```

## 🌟 Extending Magic Shell

You can add your own spells by modifying the `spells/wizard.py` file:

1. Add your spell to the `spells` dictionary in the `Wizard` class
2. Create a new method to handle your spell's functionality
3. Restart Magic Shell to use your new spell

## 🔮 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🧙‍♀️ Acknowledgments

- The ASCII art wizards, books, and crystal balls that make our shell magical
- Everyone who believes in the power of command-line magic

---

*"Those who don't believe in magic will never find it." — Roald Dahl*