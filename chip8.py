import sys
import pygame
import random
# CHIP-8 display dimensions
DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 32
DISPLAY_SCALE = 10
# CHIP-8 memory size
MEMORY_SIZE = 4096
# CHIP-8 registers
NUM_REGISTERS = 16
# CHIP-8 sack size
STACK_SIZE = 16
# CHIP-8 keypd mapping
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
        # Fetch opcode
        opcode = (self.memory[self.program_counter] << 8) | self.memory[self.program_counter + 1]
        self.program_counter += 2
        # Decode and execute opcode
        self.execute_opcode(opcode)
        # Update timers
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer == 0:
                print("BEEP!")  # Play sound
    def execute_opcode(self, opcode):
        # Extract componets of the opcode
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        n = opcode & 0x000F
        nn = opcode & 0x00FF
        nnn = opcode & 0x0FFF
        # Execute the opcode based on the first nible,
        # e.g operatios 
        if opcode == 0x00E0:
            self.display = [0] * (DISPLAY_WIDTH * DISPLAY_HEIGHT)
            self.draw_flag = True
        elif opcode == 0x00EE:
            self.program_counter = self.stack[self.stack_pointer - 1]
            self.stack_pointer -= 1
        elif (opcode & 0xF000) == 0x1000:
            self.program_counter = nnn
        elif (opcode & 0xF000) == 0x2000:
            self.stack[self.stack_pointer] = self.program_counter
            self.stack_pointer += 1
            self.program_counter = nnn
        elif (opcode & 0xF000) == 0x3000:
            if self.registers[x] == nn:
                self.program_counter += 2
        elif (opcode & 0xF000) == 0x4000:
            if self.registers[x] != nn:
                self.program_counter += 2
        elif (opcode & 0xF000) == 0x5000:
            if self.registers[x] == self.registers[y]:
                self.program_counter += 2
        elif (opcode & 0xF000) == 0x6000:
            self.registers[x] = nn
        elif (opcode & 0xF000) == 0x7000:
            self.registers[x] = (self.registers[x] + nn) & 0xFF
        elif (opcode & 0xF000) == 0x8000:
            if n == 0x0:
                self.registers[x] = self.registers[y]
            elif n == 0x1:
                self.registers[x] |= self.registers[y]
            elif n == 0x2:
                self.registers[x] &= self.registers[y]
            elif n == 0x3:
                self.registers[x] ^= self.registers[y]
            elif n == 0x4:
                sum_val = self.registers[x] + self.registers[y]
                self.registers[0xF] = 1 if sum_val > 0xFF else 0
                self.registers[x] = sum_val & 0xFF
            elif n == 0x5:
                self.registers[0xF] = 1 if self.registers[x] > self.registers[y] else 0
                self.registers[x] = (self.registers[x] - self.registers[y]) & 0xFF
            elif n == 0x6:
                self.registers[0xF] = self.registers[x] & 0x1
                self.registers[x] >>= 1
            elif n == 0x7:
                self.registers[0xF] = 1 if self.registers[y] > self.registers[x] else 0
                self.registers[x] = (self.registers[y] - self.registers[x]) & 0xFF
            elif n == 0xE:
                self.registers[0xF] = (self.registers[x] & 0x80) >> 7
                self.registers[x] = (self.registers[x] << 1) & 0xFF
        elif (opcode & 0xF000) == 0x9000:
            if self.registers[x] != self.registers[y]:
                self.program_counter += 2
        elif (opcode & 0xF000) == 0xA000:
            self.index_register = nnn
        elif (opcode & 0xF000) == 0xB000:
            self.program_counter = nnn + self.registers[0]
        elif (opcode & 0xF000) == 0xC000:
            self.registers[x] = random.randint(0, 255) & nn
        elif (opcode & 0xF000) == 0xD000:
            self.draw_sprite(x, y, n)
        elif (opcode & 0xF000) == 0xE000:
            if nn == 0x9E:
                if self.keys[self.registers[x]]:
                    self.program_counter += 2
            elif nn == 0xA1:
                if not self.keys[self.registers[x]]:
                    self.program_counter += 2
        elif (opcode & 0xF000) == 0xF000:
            if nn == 0x07:
                self.registers[x] = self.delay_timer
            elif nn == 0x0A:
                self.wait_for_key(x)
            elif nn == 0x15:
                self.delay_timer = self.registers[x]
            elif nn == 0x18:
                self.sound_timer = self.registers[x]
            elif nn == 0x1E:
                self.index_register += self.registers[x]
            elif nn == 0x29:
                self.index_register = self.registers[x] * 5
            elif nn == 0x33:
                self.memory[self.index_register] = self.registers[x] // 100
                self.memory[self.index_register + 1] = (self.registers[x] % 100) // 10
                self.memory[self.index_register + 2] = self.registers[x] % 10
            elif nn == 0x55:
                for i in range(x + 1):
                    self.memory[self.index_register + i] = self.registers[i]
                self.index_register += x + 1
            elif nn == 0x65:
                for i in range(x + 1):
                    self.registers[i] = self.memory[self.index_register + i]
                self.index_register += x + 1
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