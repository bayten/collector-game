#!/usr/bin/env python3
"""
run_me.py -- main module
========================
This is main module, which contains main game classes and launches the game.
"""

from CollectorGame import modes
import tests


def run_game(do_check: bool = True) -> None:
    """Main game code"""
    if do_check:
        tests.do_ultimate_check()
    new_universe = modes.Universe()
    new_universe.process_game(modes.CollectorGame())
