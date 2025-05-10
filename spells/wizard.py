"""Wizard mode functionality for the Magic Shell."""

import os
import random
import time
from utils.colors import COLORS as colors

class Wizard:
    """Wizard mode for the Magic Shell."""
    
    def __init__(self):
        """Initialize wizard mode."""
        self.spells = {
            "lumos": self._spell_light,
            "alohomora": self._spell_open,
            "accio": self._spell_fetch,
            "wingardium": self._spell_levitate,
        }
        
    def cast_spell(self, command: str) -> None:
        """
        Cast a spell in wizard mode.
        
        Args:
            command: The command/spell to cast
        """
        # Extract spell name (first word)
        parts = command.split()
        spell_name = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        
        # Handle special spells
        if spell_name in self.spells:
            self.spells[spell_name](args)
            return
            
        # Default behavior for unknown spells
        print(f"{colors['purple']}🧙‍♂️ Casting spell: {command}...{colors['end']}")
        time.sleep(0.5)
        os.system(command)
        print(f"{colors['cyan']}✨ The magic has been conjured! ✨{colors['end']}")
        
    def _spell_light(self, args):
        """Create magical light."""
        print(f"{colors['yellow']}💡 A bright light appears at the tip of your wand! 💡{colors['end']}")
        time.sleep(1)
        os.system("clear" if os.name == "posix" else "cls")
        
    def _spell_open(self, args):
        """Open files with magic."""
        if not args:
            print(f"{colors['red']}The spell needs a target to open!{colors['end']}")
            return
            
        target = args[0]
        print(f"{colors['green']}🔓 Magically opening {target}...{colors['end']}")
        
        if os.path.isfile(target):
            os.system(f"cat {target}")
        elif os.path.isdir(target):
            os.system(f"ls -la {target}")
        else:
            print(f"{colors['red']}Cannot find {target} to open!{colors['end']}")
            
    def _spell_fetch(self, args):
        """Fetch files with magic."""
        if not args:
            print(f"{colors['red']}The spell needs a target to summon!{colors['end']}")
            return
            
        target = args[0]
        print(f"{colors['blue']}🧲 Accio {target}! Summoning...{colors['end']}")
        os.system(f"find . -name '{target}*' 2>/dev/null")
        
    def _spell_levitate(self, args):
        """Levitate text."""
        text = " ".join(args) if args else "Leviosa!"
        
        print(f"{colors['purple']}Wingardium Leviosa!{colors['end']}")
        time.sleep(1)
        
        # Make text float upward
        for i in range(10):
            os.system("clear" if os.name == "posix" else "cls")
            print("\n" * (10 - i))
            print(f"{colors['cyan']}{text}{colors['end']}")
            time.sleep(0.2)