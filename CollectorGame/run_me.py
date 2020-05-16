#!/usr/bin/env python3
"""
run_me.py -- main module
========================
This is main module, which contains main game classes and launches the game.
"""

from CollectorGame import modes


def run_game() -> None:
    """Main game code"""
    new_universe = modes.Universe()
    new_universe.process_game(modes.CollectorGame())
