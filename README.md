
# AlloyForge: Educational Game (v1.0.0)

A metallurgy game written in Python and Pygame. You mix metals, watch the density and strength change as you go, hit a hammer timing bar while the metal is hot, and quench the alloy to finish client contracts.

<img width="1073" height="737" alt="Screenshot 2026-10-02 at 12 56 30 PM" src="https://github.com/user-attachments/assets/f0bf43a0-74ee-4841-b33f-ef05124064d9" />
<img width="1077" height="749" alt="Screenshot 2026-10-02 at 12 56 45 PM" src="https://github.com/user-attachments/assets/e74006b7-b99f-4dc3-976a-337d76850a42" />

## Key Features

* It only needs Python 3 and Pygame. There are no asset files, because all the sounds and visuals are made in code.
* You pick the weight percentages for your alloy, and the game works out the density, yield strength, and cost as you change them.
* You have to heat the metal above 450°C to hammer it and above 650°C to quench it.
* If you hit the hammer in the sweet spot on the timing bar, your alloy gets a higher strength multiplier and a higher quality cap.
* You get client contracts, a recipe codex for alloys you've found, workshop upgrades, and your progress saves automatically.
* The audio is built from raw sample arrays, so you don't need any `.wav` or `.mp3` files.

## Usage

Install Pygame if you don't have it yet.

```bash
pip3 install pygame
```

Download the file and run it in your terminal.

```bash
python3 Alloy.py
```

### Controls

| Key | What it does |
|---|---|
| 1 / 2 | Change the element in Slot 1 and Slot 2 |
| H | Heat the furnace |
| SPACE | Hammer strike (hit it when the indicator is in the green zone) |
| Q | Quench the metal |
| S | Submit the alloy to the client |
| C | Open or close the Recipe Codex |
| ESC | Save and exit |

## Limitations in Version 1.0

I kept a few things simple in this first version.

The alloy solver uses weighted averages for density, strength, and cost. It doesn't use real phase diagrams, so things like eutectic melting points and crystal phase changes aren't in there.

You can only mix two elements at a time.

The audio uses the normal `pygame.mixer` setup. If your computer doesn't have a working sound device, the game just runs without sound.

Your save is a single JSON file called `.alloy_forge_save.json` in your home directory.

## Testing

The easiest way to check that the physics, the sliders, and saving all work is to play one short round.

1. Mix 60% Copper and 40% Zinc. This should unlock Brass.
2. Press `H` to heat the metal, hit `SPACE` a few times in the green zone, press `Q` to quench, and click **SUBMIT**.
3. Press `ESC` to exit, then run `python3 Alloy.py` again.
4. Check that your gold and your unlocked recipes are still there.

## Why I Built This

Most crafting systems in RPGs and sim games use made-up recipes, like mixing two iron ingots to get a sword. None of it has anything to do with real metallurgy. I wanted to make a game where the material properties, like density, yield strength, and mix ratios, decide if your item works or fails. I also wanted it to feel like a fun arcade forge game with no outside assets.
