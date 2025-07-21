# 2D Fighting Game with Nemesis System

## Overview
This is a 2D fighting game built in Python using the Raylib library (`raylibpy`). It features a player-controlled character and a CPU opponent with an adaptive "Nemesis System" that adjusts the CPU's strategy based on the player's actions. The game includes multiple rounds, health bars, combo counters, screen shake effects, and audio integration. For a detailed analysis, refer to the [summary PDF](FightingGameAnalysis.pdf).

## Installation
1. **Prerequisites**:
   - Python 3.x
   - Raylib Python bindings (`raylibpy`): Install via `pip install raylib`.
   - Ensure all texture and audio files are in the correct directory structure (e.g., `player movement/`, `cpu/`, root for `b.mp3`, `p1.mp3`, `p2.mp3`, `flore.jpg`).

2. **Setup**:
   - Clone or download the repository.
   - Update file paths in `game.py` to match your local directory structure (e.g., replace `D:\programs\c++\games\game_5\` with relative paths).
   - Run the game: `python game.py`.

## Controls
- **Movement**:
  - `A`: Move left
  - `D`: Move right
  - `W`: Jump
  - `S`: Crouch
- **Actions**:
  - `K`: Punch (combine with `A`, `D`, `W`, `S` for variations)
  - `L`: Kick (combine with `A`, `D`, `W`, `S` for variations)
  - `SPACE`: Block
- **Debug**:
  - `R`: Reset move log (`player_moves.txt`)

## Features
- **Gameplay**: Fight in rounds (best-of-three) with health bars and combo counters.
- **Nemesis System**: CPU adapts to player actions by analyzing moves logged in `player_moves.txt`.
- **Visuals**: Screen shake, particle effects, and state-based character animations.
- **Audio**: Background music and hit sound effects.

## Notes
- Ensure all asset files (textures, audio) are accessible to avoid crashes.
- The game uses absolute file paths, which may need adjustment for portability.
- For a comprehensive analysis, including strengths, issues, and improvement suggestions, see the [summary PDF](FightingGameAnalysis.pdf).

## License
This project is unlicensed. Use and modify at your own discretion.