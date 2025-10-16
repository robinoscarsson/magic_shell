"""Wizard mode functionality for the Magic Shell."""

import os
import time
from ..utils.colors import COLORS as colors
from ..core.registry import command

# Spell definitions using the command registry

@command("illuminatus_perpetuum", "Create magical light that looks rather surprised about its own existence", 
         aliases=["light"], category="Spells", wizard_only=True)
def spell_light(*args):
    """Create magical light, or at least the impression of it."""
    print(f"{colors['yellow']}A light springs into existence at the tip of your staff, looking rather surprised about the whole affair. It's the kind of light that doesn't so much illuminate as draw attention to just how dark everything else is.{colors['end']}")
    time.sleep(1.5)
    os.system("clear" if os.name == "posix" else "cls")


@command("opendoorus_immedius", "Open files or directories, assuming they're not feeling particularly stubborn",
         aliases=["open"], category="Spells", wizard_only=True) 
def spell_open(*args):
    """Open files with magic, assuming they're not feeling particularly stubborn today."""
    if not args:
        print(f"{colors['red']}The spell fizzles pathetically. Magic, like bureaucracy, requires a specific target to inconvenience.{colors['end']}")
        return
        
    target = args[0]
    print(f"{colors['green']}You mutter the ancient words of Opening, first transcribed by the great Wizard Lockpicker of Quirm (who was, incidentally, banned from most banking establishments).{colors['end']}")
    
    if os.path.isfile(target):
        print(f"{colors['yellow']}The file reluctantly reveals its contents, rather like a bashful actor who's forgotten their lines but has to perform anyway.{colors['end']}")
        os.system(f"cat {target}")
    elif os.path.isdir(target):
        print(f"{colors['blue']}The directory sighs and unfolds itself, displaying its contents with the enthusiasm of someone showing vacation pictures to uninterested relatives.{colors['end']}")
        os.system(f"ls -la {target}")
    else:
        print(f"{colors['red']}The target appears to have mastered the first principle of magical defense: not being there when someone tries to find it.{colors['end']}")


@command("fetchum_fileium", "Summon files from the mysterious ether of the filesystem",
         aliases=["fetch"], category="Spells", wizard_only=True)
def spell_fetch(*args):
    """Fetch files with magic, a spell popular with wizards too occupied with lunch to get up."""
    if not args:
        print(f"{colors['red']}The spell needs a target, just as a pointy hat needs a head (preferably attached to a wizard).{colors['end']}")
        return
        
    target = args[0]
    print(f"{colors['blue']}With a dramatic gesture that would have impressed absolutely no one at Unseen University, you attempt to summon '{target}' from the mysterious ether of the filesystem.{colors['end']}")
    time.sleep(0.5)
    print(f"{colors['purple']}Distant objects rustle ominously as the spell takes effect. Something approaches, hopefully the right something...{colors['end']}")
    os.system(f"find . -name '{target}*' 2>/dev/null")


@command("antigravitonia_selectivus", "Elevate text in defiance of gravity's objections",
         aliases=["float"], category="Spells", wizard_only=True)
def spell_levitate(*args):
    """Levitate text, a mostly harmless spell unless attempted on something heavy or annoyed.""" 
    text = " ".join(args) if args else "This text appears to be rising despite the objections of gravity!"
    
    print(f"{colors['purple']}You cast Antigravitonia Selectivus, a spell that, according to 'Woddeley's Occult Annotations', was invented when the great mage Woddeley was too short to reach the top shelf of his library.{colors['end']}")
    time.sleep(1)
    
    print(f"{colors['yellow']}The text begins to float, looking somewhat surprised at its newfound liberation from the tyranny of gravity.{colors['end']}")
    
    # Make text float upward
    for i in range(10):
        os.system("clear" if os.name == "posix" else "cls")
        print("\n" * (10 - i))
        print(f"{colors['cyan']}{text}{colors['end']}")
        if i == 5:
            print(f"{colors['red']}The text pauses briefly, as if wondering whether this is really a sensible career move.{colors['end']}")
        time.sleep(0.3)
    
    print(f"{colors['green']}The text has successfully achieved escape velocity and has gone to join the other free-range sentences in the upper atmosphere.{colors['end']}")


class Wizard:
    """Wizard mode for the Magic Shell (legacy class for compatibility)."""
    
    def __init__(self):
        """Initialize wizard mode, or as wizards call it, 'making sure the pointy hat is on straight'."""
        # Legacy spell mapping for backward compatibility
        self.spells = {
            "illuminatus_perpetuum": lambda args: spell_light(*args),
            "light": lambda args: spell_light(*args),
            "opendoorus_immedius": lambda args: spell_open(*args), 
            "open": lambda args: spell_open(*args),
            "fetchum_fileium": lambda args: spell_fetch(*args),
            "fetch": lambda args: spell_fetch(*args),
            "antigravitonia_selectivus": lambda args: spell_levitate(*args),
            "float": lambda args: spell_levitate(*args),
        }
        
    def cast_spell(self, command: str) -> None:
        """
        Cast a spell in wizard mode (legacy method).
        
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