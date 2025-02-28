# CHIP-8 Emulator

This project is a simple emulator for the CHIP-8 virtual machine written in Python. CHIP-8 was an interpreted programming language used on early home computers. This emulator allows you to load and run CHIP-8 ROMs, providing a graphical display of the output and support for keyboard input.

## Requirements

- Python 3.x
- Pygame library

You can install the necessary Python libraries using pip:

```bash
pip install pygame
```

## Features

- **Memory:** 4096 bytes of memory
- **Registers:** 16 general-purpose registers (V0 to VF)
- **Stack:** 16-level stack
- **Timers:** 2 timers (delay and sound)
- **Display:** 64x32 monochrome display
- **Keyboard:** Support for 16 keys mapped to the standard CHIP-8 layout
- **ROM Loading:** Load and run CHIP-8 ROM files

## Usage

To run the emulator, use the following command:

```bash
python chip8.py <Game>
```

Where `<Game>` is the path to a valid CHIP-8 ROM file.

### Controls

For each game, I have no clue what the controls are.
Play around with the controls, but it takes in:

```
1  2  3  4
Q  W  E  R
A  S  D  F
Z  X  C  V
```

- `1`, `2`, `3`, `4` correspond to `1`, `2`, `3`, `4` on the CHIP-8 keypad.
- `Q`, `W`, `E`, `R` correspond to `4`, `5`, `6`, `D`.
- `A`, `S`, `D`, `F` correspond to `7`, `8`, `9`, `E`.
- `Z`, `X`, `C`, `V` correspond to `A`, `0`, `B`, `F`.

## Emulator Details

### Memory
The CHIP-8 has 4096 bytes of memory. The first 512 bytes are reserved for the interpreter, and the remaining memory is available for the program. The display is 64x32 pixels, and its state is stored in memory starting at location 0x050.

### Timers
There are two timers in the CHIP-8:
- **Delay Timer:** Decrements at 60Hz and is used to control delays.
- **Sound Timer:** Decrements at 60Hz, and a sound is played when it reaches zero.

### Display
The display is 64 pixels wide and 32 pixels tall. The display is monochrome, with pixels represented by either 0 (off) or 1 (on). Each pixel is 10x10 pixels for visual clarity.

### Sound
When the sound timer reaches zero, a beep is triggered.

## Credits

Used some code for the opcode parsing and fonts from [Omokute Blog](https://omokute.blogspot.com). It was incredibly useful for finding everything out, learning about it, and giving the basic code framework. However, I used Pygame instead of Pyglet among other differences.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

