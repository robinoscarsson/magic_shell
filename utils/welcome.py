import random
import time
import os
from utils.colors import COLORS as colors

def print_welcome():
    """Display a magical welcome screen."""
    # Clear the terminal for dramatic effect
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Choose random magical ASCII art
    ascii_arts = [
        # Wizard
        f"""{colors['purple']}
          /\\
         /  \\
        /    \\
        \\    /
         \\  /
          \\/
     .-----.
    /____{colors['yellow']}O{colors['purple']}____\\
    |            |
    |   {colors['yellow']}/ \\{colors['purple']}    |
    |  {colors['yellow']}(   ){colors['purple']}   |
    |   {colors['yellow']}\\ /{colors['purple']}    |
    |            |
    |{colors['blue']}  .--.   {colors['purple']}|
    | {colors['blue']}(    ) {colors['purple']} |
    |{colors['blue']}  `--`   {colors['purple']}|
    |____________|
        """,
        
        # Magic Book
        f"""{colors['blue']}
        __________________
       /                 /|
      /                 / |
     /________________ /  |
    |   {colors['yellow']}⚡SPELLBOOK⚡{colors['blue']}  |   |
    |                  |  /
    |                  | /
    |__________________|/
        """,
        
        # Crystal Ball
        f"""{colors['cyan']}
        .---.
       /     \\
      /       \\
     |    {colors['purple']}✨{colors['cyan']}    |
     |   {colors['purple']}✨✨{colors['cyan']}   |
     |    {colors['purple']}✨{colors['cyan']}    |
      \\       /
       \\     /
        '---'
        """
    ]
    
    # Print random ASCII art with typing effect
    art = random.choice(ascii_arts)
    for line in art.split('\n'):
        print(line)
        time.sleep(0.05)
    
    # Magical quotes
    quotes = [
        "Where words fail, magic prevails.",
        "The universe is full of magical things patiently waiting for our wits to grow sharper.",
        "Magic is believing in yourself. If you can do that, you can make anything happen.",
        "Those who don't believe in magic will never find it.",
        "Magic happens when you don't give up, even though you want to."
    ]
    
    # Print welcome message with typing effect
    welcome_text = f"""
    {colors['green']}✨ Welcome to the Magical Shell! ✨{colors['end']}
    {colors['cyan']}"{random.choice(quotes)}"{colors['end']}
    
    {colors['yellow']}Type 'help' to discover the magical commands.{colors['end']}
    """
    
    for char in welcome_text:
        print(char, end='', flush=True)
        time.sleep(0.01)
    
    # Final flourish
    print(f"\n    {colors['purple']}* * * Let the magic begin * * *{colors['end']}\n")