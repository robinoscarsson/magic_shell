#!/usr/bin/env python3
"""Test script to verify the command registry functionality."""

import sys
import os

# Add magic_shell to Python path
sys.path.insert(0, '/home/robin/code/python/magic_shell')

# Import the registry and test functionality
from magic_shell.core.registry import registry, command
from magic_shell.core.commands import CommandManager

def test_registry():
    """Test the command registry system."""
    print("🧪 Testing Magic Shell Command Registry System")
    print("=" * 50)
    
    # Initialize the command manager (this will auto-discover spells)
    test_state = {"wizard_mode": False, "running": True}
    cmd_manager = CommandManager(test_state)
    
    print(f"✅ Total commands registered: {len(registry.commands)}")
    print()
    
    # Test auto-discovery
    print("📡 Auto-discovered commands from spells/:")
    spell_commands = [cmd for cmd in registry.list_commands(True) if cmd.category in ["Spells", "Demo"]]
    for cmd in sorted(spell_commands, key=lambda x: x.name):
        aliases = f" ({', '.join(cmd.aliases)})" if cmd.aliases else ""
        wizard_indicator = " [WIZARD ONLY]" if cmd.wizard_only else ""
        print(f"  🪄 {cmd.name}{aliases}{wizard_indicator} - {cmd.help_text}")
    
    print()
    
    # Test help command
    print("🔍 Testing help command functionality:")
    try:
        print("--- Normal Mode Help ---")
        registry.execute_command("help", wizard_mode=False)
        print("\n--- Wizard Mode Help ---") 
        registry.execute_command("help", wizard_mode=True)
        print("✅ Help commands work correctly!")
    except Exception as e:
        print(f"❌ Help command failed: {e}")
    
    print()
    
    # Test command lookup
    print("🔍 Testing command lookup:")
    test_commands = ["help", "wizard", "light", "fetch", "time", "fortune"]
    
    for cmd_name in test_commands:
        cmd_info = registry.get_command(cmd_name)
        if cmd_info:
            print(f"  ✅ Found '{cmd_name}' -> {cmd_info.name} ({cmd_info.category})")
        else:
            print(f"  ❌ Command '{cmd_name}' not found")
    
    print()
    
    # Test categories
    print("📂 Available command categories:")
    categories = set(cmd.category for cmd in registry.list_commands(True))
    for category in sorted(categories):
        count = len([cmd for cmd in registry.list_commands(True) if cmd.category == category])
        print(f"  📁 {category}: {count} commands")
    
    print()
    print("🎉 Command Registry Test Complete!")
    
    return True

def test_new_command():
    """Test adding a new command dynamically."""
    print("\n🔬 Testing Dynamic Command Registration")
    print("=" * 40)
    
    # Register a new test command
    @command("test_spell", "A test spell for demonstration", 
             aliases=["test"], category="Testing", wizard_only=True)
    def my_test_spell():
        print("🧪 Test spell successfully executed!")
        return "spell_result"
    
    # Test that it was registered
    cmd_info = registry.get_command("test_spell")
    if cmd_info:
        print("✅ New command 'test_spell' registered successfully")
        print(f"   Aliases: {cmd_info.aliases}")
        print(f"   Category: {cmd_info.category}")
        print(f"   Wizard only: {cmd_info.wizard_only}")
        
        # Test execution
        result = registry.execute_command("test_spell")
        print(f"   Execution result: {result}")
        
        # Test alias
        alias_cmd = registry.get_command("test") 
        if alias_cmd and alias_cmd.name == "test_spell":
            print("✅ Alias 'test' works correctly")
        else:
            print("❌ Alias 'test' not working")
    else:
        print("❌ New command registration failed")

if __name__ == "__main__":
    try:
        test_registry()
        test_new_command()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()