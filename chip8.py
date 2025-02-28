import sys
import pygame
import random

DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 32
DISPLAY_SCALE = 10
MEMORY_SIZE = 4096
NUM_REGISTERS = 16
STACK_SIZE = 16

KEY_MAP = {
    pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
    pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
    pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
}   

class Chip8:
    def __init__(self):
        self.memory = [0] * MEMORY_SIZE
        self.registers = [0] * NUM_REGISTERS
        self.index_register = 0
        self.program_counter = 0x200
        self.stack = [0] * STACK_SIZE
        self.stack_pointer = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.display = [0] * (DISPLAY_WIDTH * DISPLAY_HEIGHT)
        self.keys = [0] * 16
        self.draw_flag = False
        self.fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  
            0x20, 0x60, 0x20, 0x20, 0x70,  
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  
            0x90, 0x90, 0xF0, 0x10, 0x10,  
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  
            0xF0, 0x10, 0x20, 0x40, 0x40,  
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  
            0xF0, 0x90, 0xF0, 0x90, 0x90,  
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  
            0xF0, 0x80, 0x80, 0x80, 0xF0,  
            0xE0, 0x90, 0x90, 0x90, 0xE0,  
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  
            0xF0, 0x80, 0xF0, 0x80, 0x80   
        ]
        for i in range(len(self.fontset)):
            self.memory[i] = self.fontset[i]

    def load_rom(self, rom_path):
        with open(rom_path, "rb") as f:
            rom_data = f.read()
            for i in range(len(rom_data)):
                self.memory[0x200 + i] = rom_data[i]

    def emulate_cycle(self):
        opcode = (self.memory[self.program_counter] << 8) | self.memory[self.program_counter + 1]
        self.program_counter += 2
        self.execute_opcode(opcode)
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer == 0:
                print("BEEP!")

    def execute_opcode(self, opcode):
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        n = opcode & 0x000F
        nn = opcode & 0x00FF
        nnn = opcode & 0x0FFF
        if opcode == 0x00E0:
            self.display = [0] * (DISPLAY_WIDTH * DISPLAY_HEIGHT)
            self.draw_flag = True
        elif opcode == 0x00EE:
            self.program_counter = self.stack[self.stack_pointer - 1]
            self.stack_pointer -= 1
        elif (opcode & 0xF000) == 0xA000:
            self.index_register = nnn

    def draw_sprite(self, x, y, n):
        self.registers[0xF] = 0
        for row in range(n):
            sprite_byte = self.memory[self.index_register + row]
            for col in range(8):
                if (sprite_byte & (0x80 >> col)) != 0:
                    pixel_index = (self.registers[x] + col + ((self.registers[y] + row) * DISPLAY_WIDTH)) % (DISPLAY_WIDTH * DISPLAY_HEIGHT)
                    if self.display[pixel_index] == 1:
                        self.registers[0xF] = 1
                    self.display[pixel_index] ^= 1
        self.draw_flag = True

    def wait_for_key(self, x):
        for i in range(len(self.keys)):
            if self.keys[i]:
                self.registers[x] = i
                return
        self.program_counter -= 2

    def update_keys(self, keys):
        for key, value in KEY_MAP.items():
            self.keys[value] = keys[key]

def main():
    if len(sys.argv) != 2:
        print("Usage: python chip8.py <rom_path>")
        return
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH * DISPLAY_SCALE, DISPLAY_HEIGHT * DISPLAY_SCALE))
    pygame.display.set_caption("CHIP-8 Emulator")
    clock = pygame.time.Clock()
    chip8 = Chip8()
    chip8.load_rom(sys.argv[1])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        chip8.update_keys(keys)
        chip8.emulate_cycle()
        if chip8.draw_flag:
            screen.fill((0, 0, 0))
            for i in range(DISPLAY_WIDTH * DISPLAY_HEIGHT):
                if chip8.display[i]:
                    x = (i % DISPLAY_WIDTH) * DISPLAY_SCALE
                    y = (i // DISPLAY_WIDTH) * DISPLAY_SCALE
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, DISPLAY_SCALE, DISPLAY_SCALE))
            pygame.display.flip()
            chip8.draw_flag = False
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
