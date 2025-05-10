"""Wizard mode functionality for the Magic Shell."""

import os
import random
import time
from utils.colors import COLORS as colors

class Wizard:
    """Wizard mode for the Magic Shell."""
    
    def __init__(self):
        """Initialize wizard mode, or as wizards call it, 'making sure the pointy hat is on straight'."""
        self.spells = {
            # A simple illumination spell, favored by wizards who've had 
            # enough of unexpected encounters with furniture in the dark
            "illuminatus_perpetuum": self._spell_light,
            
            # From "The Compleat Opener of Doors and Windows and Also Some Cupboards", 
            # written by the great Unseen University Archchancellor "Locksmith" Ridcully
            "opendoorus_immedius": self._spell_open,
            
            # Developed by lazy wizards who couldn't be bothered to get up from 
            # their comfortable chairs after lunch (which is most of them)
            "fetchum_fileium": self._spell_fetch,
            
            # A rather controversial spell that caused quite a stir at the last 
            # Grand Wizards' Convention after it was used to elevate all the 
            # refreshments just out of reach
            "antigravitonia_selectivus": self._spell_levitate,
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
        """Create magical light, or at least the impression of it."""
        print(f"{colors['yellow']}A light springs into existence at the tip of your staff, looking rather surprised about the whole affair. It's the kind of light that doesn't so much illuminate as draw attention to just how dark everything else is.{colors['end']}")
        time.sleep(1.5)
        os.system("clear" if os.name == "posix" else "cls")
        
    def _spell_open(self, args):
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
            
    def _spell_fetch(self, args):
        """Fetch files with magic, a spell popular with wizards too occupied with lunch to get up."""
        if not args:
            print(f"{colors['red']}The spell needs a target, just as a pointy hat needs a head (preferably attached to a wizard).{colors['end']}")
            return
            
        target = args[0]
        print(f"{colors['blue']}With a dramatic gesture that would have impressed absolutely no one at Unseen University, you attempt to summon '{target}' from the mysterious ether of the filesystem.{colors['end']}")
        time.sleep(0.5)
        print(f"{colors['purple']}Distant objects rustle ominously as the spell takes effect. Something approaches, hopefully the right something...{colors['end']}")
        os.system(f"find . -name '{target}*' 2>/dev/null")
        
    def _spell_levitate(self, args):
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