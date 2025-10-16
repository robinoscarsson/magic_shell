"""Demo spells to showcase the command registry system."""

import time
from ..core.registry import command
from ..utils.colors import COLORS as colors


@command("time", "Show the current time with magical flair", 
         aliases=["clock"], category="Demo", wizard_only=True)
def spell_time():
    """Display current time with magical effects."""
    import datetime
    
    print(f"{colors['purple']}🕐 Consulting the ancient chronometer spells...{colors['end']}")
    time.sleep(0.5)
    
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    print(f"{colors['cyan']}⏰ The cosmic timekeeper reveals:{colors['end']}")
    print(f"{colors['yellow']}   Time: {current_time}{colors['end']}")
    print(f"{colors['yellow']}   Date: {current_date}{colors['end']}")
    print(f"{colors['green']}✨ Time magic successfully conjured!{colors['end']}")


@command("fortune", "Dispense mystical wisdom from the shell oracles",
         aliases=["wisdom", "oracle"], category="Demo", wizard_only=True) 
def spell_fortune():
    """Share magical wisdom with the user."""
    import random
    
    fortunes = [
        "The command line sees all, knows all, compiles most things.",
        "A wizard's true power lies not in the spell, but in the tab completion.",
        "Beware of infinite loops - they are neither infinite nor particularly loopy.",
        "The greatest magic is a bug-free deployment on Friday afternoon.",
        "In the depths of /dev/null, all errors become enlightenment.",
        "A good backup spell is worth a thousand 'git push --force' incantations.",
        "The shell whispers: 'sudo make me a sandwich' works on both computers and relationships.",
    ]
    
    print(f"{colors['purple']}🔮 Gazing into the mystical command-line crystal ball...{colors['end']}")
    time.sleep(1)
    
    fortune = random.choice(fortunes)
    print(f"{colors['cyan']}✨ The Oracle speaks:{colors['end']}")
    print(f"{colors['yellow']}   \"{fortune}\"{colors['end']}")
    print(f"{colors['green']}🧙‍♂️ Wisdom has been dispensed!{colors['end']}")


@command("ls", "List directory contents with magical enhancement",
         category="System")
def enhanced_ls(*args):
    """Enhanced ls command with magical flair.""" 
    import subprocess
    
    # Build ls command with arguments
    cmd = ["ls", "--color=auto"] + list(args)
    
    print(f"{colors['blue']}📁 Magically revealing directory contents...{colors['end']}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"{colors['red']}{result.stderr}{colors['end']}")
    except Exception as e:
        print(f"{colors['red']}Directory revelation spell failed: {e}{colors['end']}")