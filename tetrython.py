import pygame, sys, random
from sys import exit

JLSTZ_KICKS = {
    (0, 1): [(0, 0), (-1, 0), (-1,  1), (0, -2), (-1, -2)],
    (1, 0): [(0, 0), ( 1, 0), ( 1, -1), (0,  2), ( 1,  2)],
    (1, 2): [(0, 0), ( 1, 0), ( 1, -1), (0,  2), ( 1,  2)],
    (2, 1): [(0, 0), (-1, 0), (-1,  1), (0, -2), (-1, -2)],
    (2, 3): [(0, 0), ( 1, 0), ( 1,  1), (0, -2), ( 1, -2)],
    (3, 2): [(0, 0), (-1, 0), (-1, -1), (0,  2), (-1,  2)],
    (3, 0): [(0, 0), (-1, 0), (-1, -1), (0,  2), (-1,  2)],
    (0, 3): [(0, 0), ( 1, 0), ( 1,  1), (0, -2), ( 1, -2)],
}

I_KICKS = {
    (0, 1): [( 0, 0), (-2, 0), ( 1, 0), (-2, -1), ( 1,  2)],
    (1, 0): [( 0, 0), ( 2, 0), (-1, 0), ( 2,  1), (-1, -2)],
    (1, 2): [( 0, 0), (-1, 0), ( 2, 0), (-1,  2), ( 2, -1)],
    (2, 1): [( 0, 0), ( 1, 0), (-2, 0), ( 1, -2), (-2,  1)],
    (2, 3): [( 0, 0), ( 2, 0), (-1, 0), ( 2,  1), (-1, -2)],
    (3, 2): [( 0, 0), (-2, 0), ( 1, 0), (-2, -1), ( 1,  2)],
    (3, 0): [( 0, 0), ( 1, 0), (-2, 0), ( 1, -2), (-2,  1)],
    (0, 3): [( 0, 0), (-1, 0), ( 2, 0), (-1,  2), ( 2, -1)],
}

class Colors:
	dark_grey = (26, 31, 40)
	green = (47, 230, 23)
	red = (232, 18, 18)
	orange = (226, 116, 17)
	yellow = (237, 234, 4)
	purple = (166, 0, 247)
	cyan = (21, 204, 209)
	blue = (13, 64, 216)
	white = (255, 255, 255)
	dark_blue = (44, 44, 127)
	light_blue = (59, 85, 162)

	@classmethod
	def get_cell_colors(cls):
		return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]

class Button:
    def __init__(self, pos, image, text_input, base_clr, hover_clr):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.image = image
        self.base_clr = base_clr
        self.hover_clr = hover_clr
        self.text_input = text_input
        self.text = game_font.render(self.text_input, True, "white")
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos + 3, self.y_pos-3))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkClick(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = game_font.render(self.text_input, True, self.hover_clr)
        else:
            self.text = game_font.render(self.text_input, True, self.base_clr)

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 35
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def inside_grid(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False

    def is_empty(self,row,column):
        if self.grid[row][column] == 0:
            return True
        return False

    def row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def row_clear(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_rows(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def reset_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column]=0
                
    def clear_full_rows(self):
        global highscore
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.row_full(row):
                self.row_clear(row)
                channel1.play(clear)
                completed += 1
                mgame.score += 100
                if mgame.score > highscore:
                    highscore = mgame.score
                    save_high_score(mgame.score, "highscore.txt")
            elif completed > 0:
                self.move_rows(row,completed)
        return completed

    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size + 480, row*self.cell_size + 11, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
        
        for col in range(self.num_cols + 1):
            x = 480 + col * self.cell_size
            pygame.draw.line(screen, (0,0,0), (x, 11), (x, 11 + self.num_rows * self.cell_size), 1)

        for row in range(self.num_rows + 1):
            y = 11 + row * self.cell_size
            pygame.draw.line(screen, (0,0,0), (480, y), (480 + self.num_cols * self.cell_size, y), 1)

        border_x = 480
        border_y = 11
        border_width = self.num_cols * self.cell_size
        border_height = self.num_rows * self.cell_size
        pygame.draw.rect(screen, Colors.white, (border_x - 6, border_y - 5, border_width + 12, border_height + 11), width=5)

class MGame:
    def __init__ (self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.block_held = None
        self.can_hold = True
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.lock_delay = 400
        self.lock_timer = None
        self.fail = False

    def get_random_block(self):
        if len(self.blocks)==0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move_block(0,-1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move_block(0, 1)

    def move_right(self):
        self.current_block.move_block(0,1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move_block(0, -1)

    def can_move_down(self):
        self.current_block.move_block(1, 0)
        ok = self.block_inside()
        self.current_block.move_block(-1, 0)
        return ok

    def block_supported(self):
        self.current_block.move_block(1, 0)
        fits = self.block_fits()
        self.current_block.move_block(-1, 0)
        return not fits

    def move_down(self):
        global score
        self.current_block.move_block(1,0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move_block(-1, 0)
            if self.lock_timer is None:
                self.lock_timer = pygame.time.get_ticks()
        else:
            self.lock_timer = None

    def hard_drop(self):
        steps = 0
        while True:
            self.current_block.move_block(1, 0)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move_block(-1, 0)
                break
            steps += 1

        self.lock_timer = None
        result = self.lock_block()
        return result, steps

    def get_ghost_pos(self):
        ghost_block = self.current_block
        offset = 0
        tiles = ghost_block.get_cell_positions()

        while True:
            for tile in tiles:
                row = tile.row + offset
                column = tile.column
                if not self.grid.inside_grid(row,column) or not self.grid.is_empty(row,column):
                    offset -= 1
                    break
            else:
                offset += 1
                continue
            break

        ghost_pos=[]
        for tile in tiles:
            ghost_pos.append(Position(tile.row + offset, tile.column))

        return ghost_pos

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.inside_grid(tile.row, tile.column) == False:
                return False
        return True

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.inside_grid(tile.row, tile.column) == False:
                return False
            if self.grid.is_empty(tile.row,tile.column) == False:
                return False
        return True

    def rotate_block(self):
        block = self.current_block
        old_state = block.rotation_state
        old_row, old_col = block.row_offset, block.column_offset
        new_state = (old_state + 1) % len(block.cells)
        block.rotation_state = new_state
        kicks = I_KICKS if block.id == 3 else JLSTZ_KICKS
        tests = kicks.get((old_state, new_state), [(0,0)])
        
        for dx, dy in tests:
            block.column_offset += dx
            block.row_offset += dy
            if self.block_fits():
                return

            block.column_offset -= dx
            block.row_offset -= dy
        
        block.rotation_state = old_state
        block.row_offset, block.column_offset = old_row, old_col

    def reset(self):
        self.grid.reset_grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        self.score = 0
        self.level = 1
        self.block_held = None
        self.can_hold = True

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        channel1.play(place)

        cleared_lines = self.grid.clear_full_rows()
        base_points = {1: 40, 2: 100, 3: 300, 4: 600}
        if cleared_lines > 0:
            self.lines_cleared += cleared_lines
            self.level = 1 + (self.lines_cleared // 10)
            if self.level < 21:
                self.score += base_points.get(cleared_lines, 0) * (self.level - 1)
            else:
                self.score += base_points.get(cleared_lines, 0) * 20
            update_fall_speed(self.level)
                
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        self.grid.clear_full_rows()
        if self.block_fits() == False:
            self.fail = True
        self.can_hold = True

    def hold_block(self):
        if not self.can_hold or self.fail:
            return

        old = self.current_block
        if self.block_held is None:
            self.block_held = old
            self.current_block = self.next_block
            self.next_block = self.get_random_block()
        else:
            self.current_block = self.block_held

        self.block_held = old
        self.current_block.row_offset = 0
        self.block_held.rotation_state = 0
        self.current_block.column_offset = (self.grid.num_cols // 2) - 1
        if isinstance(self.current_block, IBlock):
            self.current_block.row_offset = -1
        self.can_hold = False

    def draw(self, screen):
        self.grid.draw(screen)
        ghost_pos = self.get_ghost_pos()
        self.current_block.draw_ghost_block(screen, ghost_pos)
        self.current_block.draw_block(screen, 480, 11)

        if self.block_held:
            temp_block = self.block_held
            original_row = temp_block.row_offset
            original_col = temp_block.column_offset
            
            temp_block.row_offset = 0
            temp_block.column_offset = 0
            
            if temp_block.id == 3:
                temp_block.draw_block(screen, 276, 120)
            elif temp_block.id == 4:
                temp_block.draw_block(screen, 310, 135)
            else:
                temp_block.draw_block(screen, 293, 135)
            
            temp_block.row_offset = original_row
            temp_block.column_offset = original_col

        if self.next_block.id == 3:
            self.next_block.draw_block(screen, 755, 280)
        elif self.next_block.id == 4:
            self.next_block.draw_block(screen, 790, 270)
        else:
            self.next_block.draw_block(screen, 772, 270)

class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column

class Block:
    def __init__(self,id):
        self.id = id
        self.cells = {}
        self.cell_size = 35
        self.rotation_state = 0
        self.row_offset = 0
        self.column_offset = 0
        self.colors = Colors.get_cell_colors()

    def draw_ghost_block(self, screen, ghost_pos):
        ghost_clr = [min(c + 100, 255) for c in self.colors[self.id]]
        for tile in ghost_pos:
            tile_rect = pygame.Rect((tile.column*self.cell_size + 480), (tile.row*self.cell_size + 11), self.cell_size, self.cell_size)
            pygame.draw.rect(screen, ghost_clr, tile_rect,1)

    def draw_block(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(tile.column * self.cell_size + offset_x, tile.row * self.cell_size + offset_y, self.cell_size+1, self.cell_size+1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
            pygame.draw.rect(screen, (0,0,0), tile_rect, width=1)

    def move_block(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotate(self):
        self.rotation_state -= 1
        if self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1

class LBlock(Block):
    def __init__(self):
        super().__init__(id = 1)
        self.cells = {
            0: [Position(0, 2), Position(1, 2), Position(1, 1), Position(1,0)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(2, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        start_col = (10 // 2) - 1
        self.move_block(0, start_col)

class JBlock(Block):
    def __init__(self):
        super().__init__(id = 2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        start_col = (10 // 2) - 1
        self.move_block(0, start_col)

class IBlock(Block):
    def __init__(self):
        super().__init__(id = 3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        start_col = (10 // 2) - 1
        self.move_block(-1, start_col)

class OBlock(Block):
    def __init__(self):
        super().__init__(id = 4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }
        start_col = (10 // 2) - 1
        self.move_block(0, start_col)

class SBlock(Block):
    def __init__(self):
        super().__init__(id = 5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        start_col = (10 // 2) - 1
        self.move_block(0, start_col)

class TBlock(Block):
    def __init__(self):
        super().__init__(id = 6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        start_col = (10 // 2) - 1
        self.move_block(0, start_col)

class ZBlock(Block):
    def __init__(self):
        super().__init__(id = 7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        start_col = (10 // 2) - 1
        self.move_block(0, start_col)

#inițializări
pygame.init()
pygame.font.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2**12)
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Tetrython")
icon = pygame.image.load('assets/Images/icon.jpg').convert()
pygame.display.set_icon(icon)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#font-uri
title_font = pygame.font.Font(None, 40)
logo_font = pygame.font.Font('assets/Fonts/Gamer.ttf', 150)
game_font = pygame.font.Font('assets/Fonts/Gamer.ttf', 55)
subtitle_font = pygame.font.Font('assets/Fonts/Gamer.ttf', 90)
score_surface = title_font.render("Score", True, (255,255,255))
next_surface = title_font.render("Next", True, (255,255,255))
hold_surface = title_font.render("Hold", True, (255,255,255))
game_over_surface = title_font.render("GAME OVER", True, (255,255,255))

#imagini
logo = pygame.transform.scale_by(pygame.image.load('assets/Images/logo.png'), 0.30).convert_alpha()
logo_rect = logo.get_rect()
bg_surface=pygame.transform.scale_by(pygame.image.load('assets/Images/bg.png'), 1).convert_alpha()
bg_surface_rect = bg_surface.get_rect()
button_surface = pygame.transform.scale_by(pygame.image.load('assets/Images/button.png'), 1.70).convert_alpha()
button1_surface = pygame.transform.scale_by(pygame.image.load('assets/Images/button1.png'),1.90).convert_alpha()
score_rect = pygame.Rect(880, 85, 170, 60)
next_rect = pygame.Rect(880, 215, 170, 170)
hold_rect = pygame.Rect(260, 85, 170, 170)

#sunet
vol_mus = 0.3
vol_sfx = 0.2
channel1 = pygame.mixer.Channel(1)
select = pygame.mixer.Sound('assets/Audio/button_select.mp3')
place = pygame.mixer.Sound('assets/Audio/place.mp3')
clear = pygame.mixer.Sound('assets/Audio/clear_line.mp3')
bgm = pygame.mixer.music.load('assets/Audio/bgm.mp3')

highscore = 0

clock = pygame.time.Clock()

mgame = MGame()

GAME_UPDATE = pygame.USEREVENT

def update_fall_speed(level):
    speed = max(75, 1000 - (level - 1) * 100)
    pygame.time.set_timer(GAME_UPDATE, speed)

#încarcă scorul maxim
def load_high_score(filename=("highscore.txt","mp_highscore.txt")):
    try:
        with open(filename, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

#salvează scorul maxim
def save_high_score(score, filename=("highscore.txt","mp_highscore.txt")):
    with open(filename, "w") as file:
        file.write(str(score))

#bara de volum
def volumeBar(vols, slider_x, slider_y):
    slider_width = 500
    slider_height = 50
    pygame.draw.rect(screen, (0,0,0), (slider_x-3.5, slider_y-3.5, slider_width+8, slider_height+8), border_radius=8)

    pygame.draw.rect(screen, (100, 100, 100), (slider_x, slider_y, slider_width, slider_height), border_radius=5)

    filled_width = int(slider_width * vols)
    pygame.draw.rect(screen, (0, 200, 0), (slider_x, slider_y, filled_width, slider_height), border_radius=5)

    volume_text = game_font.render(f"{int(vols*100)}%", True, (255, 255, 255))
    screen.blit(volume_text, (SCREEN_WIDTH // 2 - volume_text.get_width() // 2, slider_y-1))

#meniul principal
def main_menu():
    play_button = Button(pos=(SCREEN_WIDTH // 2, 350), image=button_surface, text_input="Play", base_clr="white", hover_clr="Green")
    options_button = Button(pos=(SCREEN_WIDTH // 2, 450), image=button_surface, text_input="Options", base_clr="white", hover_clr="Green")
    quit_button = Button(pos=(SCREEN_WIDTH // 2, 550), image=button_surface, text_input="Quit", base_clr="white", hover_clr="Green")

    while True:
        screen.blit(bg_surface, (0,0))

        menu_MousePos = pygame.mouse.get_pos()

        screen.blit(logo, ((SCREEN_WIDTH//2 - 245),(SCREEN_HEIGHT//2 - 250)))

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_MousePos)
            button.update(screen)

        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkClick(menu_MousePos):
                    channel1.play(select)
                    return "game"
                
                if options_button.checkClick(menu_MousePos):
                    channel1.play(select)
                    return "options"

                if quit_button.checkClick(menu_MousePos):
                    channel1.play(select)
                    return "quit"

        pygame.display.update()
        clock.tick(60)

#pauză
def pause_overlay():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    pause_text = subtitle_font.render("Paused", True, "white")
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

    hint_text = game_font.render("Press ESC to resume", True, "white")
    hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))

    restart_button = Button(pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 +50), image=button_surface, text_input="Restart", base_clr="white", hover_clr="Green")
    menu_button = Button(pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 +150), image=button_surface, text_input="Menu", base_clr="white", hover_clr="Green")

    while True:
        mgame.draw(screen)
        screen.blit(overlay, (0, 0))
        screen.blit(pause_text, pause_rect)
        screen.blit(hint_text, hint_rect)

        menu_MousePos = pygame.mouse.get_pos()

        for button in [restart_button, menu_button]:
            button.changeColor(menu_MousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    channel1.play(select)
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.checkClick(menu_MousePos):
                    channel1.play(select)
                    return "game"
                
                if menu_button.checkClick(menu_MousePos):
                    channel1.play(select)
                    return "main_menu"

        pygame.display.update()
        clock.tick(60)

#bucla jocului
def game():
    global highscore
    pygame.mixer.music.rewind()
    mgame.fail = False
    move_delay = 500
    soft_drop_delay = 15
    lock_delay = mgame.lock_delay
    das_delay = 180

    last_move_time = 0
    move_left_held = False
    move_right_held = False
    soft_drop_held = False

    arr_speed = 15

    last_left_press = 0
    last_right_press = 0
    last_soft_drop_time = 0
    next_left_move = 0
    next_right_move = 0

    update_fall_speed(mgame.level)

    while True:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_a, pygame.K_LEFT] and mgame.fail == False:
                    move_left_held = True
                    last_left_press = pygame.time.get_ticks()
                    next_left_move = last_left_press + das_delay
                    mgame.move_left()
                    if mgame.lock_timer is not None:
                        mgame.lock_timer = pygame.time.get_ticks()

                if event.key in [pygame.K_d, pygame.K_RIGHT] and mgame.fail == False:
                    move_right_held = True
                    last_right_press = pygame.time.get_ticks()
                    next_right_move = last_right_press + das_delay
                    mgame.move_right()
                    if mgame.lock_timer is not None:
                        mgame.lock_timer = pygame.time.get_ticks()

                if event.key == pygame.K_SPACE and mgame.fail == False:
                    result = mgame.hard_drop()
                    if result == "game_over":
                        mgame.game_over = True
                    else:
                        mgame.score += 2
                        if mgame.score > highscore:
                            highscore = mgame.score
                            save_high_score(mgame.score, "highscore.txt")
                    mgame.lock_timer = None

                if event.key == pygame.K_c and mgame.fail == False:
                    mgame.hold_block()

                if event.key in [pygame.K_s, pygame.K_DOWN] and mgame.fail == False:
                    soft_drop_held = True
                    mgame.move_down()

                if event.key in [pygame.K_w, pygame.K_UP] and mgame.fail == False:
                    mgame.rotate_block()
                    if mgame.lock_timer is not None:
                        mgame.lock_timer = pygame.time.get_ticks()

                if event.key == pygame.K_ESCAPE and mgame.fail == False:
                    channel1.play(select)
                    result = pause_overlay()
                    if result == "main_menu":
                        pygame.mixer.music.rewind()
                        return "main_menu"
                    elif result == "game":
                        pygame.mixer.music.rewind()
                        mgame.reset()

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    move_left_held = False
                if event.key in [pygame.K_d, pygame.K_RIGHT]:
                    move_right_held = False
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    soft_drop_held = False

            if event.type == GAME_UPDATE and mgame.fail == False:
                mgame.move_down()

        current_time = pygame.time.get_ticks()

        if move_left_held and current_time >= next_left_move:
            mgame.move_left()
            next_left_move = current_time + arr_speed

        if move_right_held and current_time >= next_right_move:
            mgame.move_right()
            next_right_move = current_time + arr_speed

        if soft_drop_held and current_time - last_soft_drop_time > soft_drop_delay:
            mgame.move_down()
            last_soft_drop_time = current_time

        if mgame.lock_timer is not None and now - mgame.lock_timer >= mgame.lock_delay:
            if mgame.block_supported():
                mgame.lock_block()
                mgame.score += 1
                if mgame.score > highscore:
                    highscore = mgame.score
                    save_high_score(mgame.score, "highscore.txt")
                mgame.lock_timer = None

        #Drawing
        score_value_surface = title_font.render(f"{mgame.score}", True, (255,255,255))
        level_surface = title_font.render(f"Level: {mgame.level}", True, (255, 255, 255))
        lines_surface = title_font.render(f"Lines: {mgame.lines_cleared}", True, (255, 255, 255))

        screen.blit(bg_surface, (0,0))
        screen.blit(score_surface, (880, 50, 50, 50))
        screen.blit(next_surface, (880, 180, 50, 50))
        screen.blit(hold_surface, (260, 50, 50, 50))
        screen.blit(level_surface, (880, 400))
        screen.blit(lines_surface, (880, 450))

        if mgame.fail == True:
            return "game_over"

        pygame.draw.rect(screen, (100,100,100), score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, 
        centery = score_rect.centery))
        pygame.draw.rect(screen, (100,100,100), next_rect, 0, 10)
        pygame.draw.rect(screen, (100,100,100), hold_rect, 0, 10)
        mgame.draw(screen)

        pygame.display.update()
        clock.tick(60)

#meniul de sunet
def volume():
    global vol_sfx, vol_mus
    volume_Text = subtitle_font.render("Volume", True, "white")
    volume_rect = volume_Text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT // 2 - 250))

    vol_sfx_txt = game_font.render("SFX:", True, "white")
    vol_sfx_rect = vol_sfx_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT // 2 - 160))
    vol_sfx1_button = Button(pos=(SCREEN_WIDTH//2 + 320, SCREEN_HEIGHT // 2 -100), image=button1_surface, text_input="+1", base_clr="white", hover_clr=(74, 87, 34))
    vol_sfx2_button = Button(pos=(SCREEN_WIDTH//2 - 320, SCREEN_HEIGHT // 2 -100), image=button1_surface, text_input="-1", base_clr="white", hover_clr=(74, 87, 34))
    vol_sfx3_button = Button(pos=(SCREEN_WIDTH//2 + 420, SCREEN_HEIGHT // 2 -100), image=button1_surface, text_input="+10", base_clr="white", hover_clr=(74, 87, 34))
    vol_sfx4_button = Button(pos=(SCREEN_WIDTH//2 - 420, SCREEN_HEIGHT // 2 -100), image=button1_surface, text_input="-10", base_clr="white", hover_clr=(74, 87, 34))

    vol_mus_txt = game_font.render("BGM:", True, "white")
    vol_mus_rect = vol_mus_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT // 2 - 10))
    vol_mus1_button = Button(pos=(SCREEN_WIDTH//2 + 320, SCREEN_HEIGHT // 2 + 50), image=button1_surface, text_input="+1", base_clr="white", hover_clr=(74, 87, 34))
    vol_mus2_button = Button(pos=(SCREEN_WIDTH//2 - 320, SCREEN_HEIGHT // 2 + 50), image=button1_surface, text_input="-1", base_clr="white", hover_clr=(74, 87, 34))
    vol_mus3_button = Button(pos=(SCREEN_WIDTH//2 + 420, SCREEN_HEIGHT // 2 + 50), image=button1_surface, text_input="+10", base_clr="white", hover_clr=(74, 87, 34))
    vol_mus4_button = Button(pos=(SCREEN_WIDTH//2 - 420, SCREEN_HEIGHT // 2 + 50), image=button1_surface, text_input="-10", base_clr="white", hover_clr=(74, 87, 34))

    back_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT // 2 + 200), image=button_surface, text_input="Back", base_clr="white", hover_clr=(74, 87, 34))
    while True:
        
        screen.blit(bg_surface,bg_surface_rect)
        screen.blit(vol_sfx_txt, vol_sfx_rect)
        screen.blit(vol_mus_txt, vol_mus_rect)
        volume_MousePos = pygame.mouse.get_pos()
        volumeBar(vol_sfx, SCREEN_WIDTH//2 -250, SCREEN_HEIGHT // 2 - 123)
        volumeBar(vol_mus, SCREEN_WIDTH//2 -250, SCREEN_HEIGHT // 2 + 27)
        
        screen.blit(volume_Text, volume_rect)

        for button in [back_button, vol_sfx1_button, vol_sfx2_button, vol_sfx3_button, vol_sfx4_button, vol_mus1_button, vol_mus2_button, vol_mus3_button, vol_mus4_button]:
            button.changeColor(volume_MousePos)
            button.update(screen)

        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkClick(volume_MousePos):
                    channel1.play(select)
                    return "options"

                if vol_sfx1_button.checkClick(volume_MousePos):
                    vol_sfx = round(min(vol_sfx + 0.01, 1.0), 2)
                    channel1.set_volume(vol_sfx)
                    channel1.play(select)

                if vol_sfx2_button.checkClick(volume_MousePos):
                    vol_sfx = round(max(vol_sfx - 0.01, 0.0), 2)
                    channel1.set_volume(vol_sfx)
                    channel1.play(select)
                
                if vol_sfx3_button.checkClick(volume_MousePos):
                    vol_sfx = round(min(vol_sfx + 0.1, 1.0), 2)
                    channel1.set_volume(vol_sfx)
                    channel1.play(select)

                if vol_sfx4_button.checkClick(volume_MousePos):
                    vol_sfx = round(max(vol_sfx - 0.1, 0.0), 2)
                    channel1.set_volume(vol_sfx)
                    channel1.play(select)

                if vol_mus1_button.checkClick(volume_MousePos):
                    vol_mus = round(min(vol_mus + 0.01, 1.0), 2)
                    pygame.mixer.music.set_volume(vol_mus)
                    channel1.play(select)

                if vol_mus2_button.checkClick(volume_MousePos):
                    vol_mus = round(max(vol_mus - 0.01, 0.0), 2)
                    pygame.mixer.music.set_volume(vol_mus)
                    channel1.play(select)
                
                if vol_mus3_button.checkClick(volume_MousePos):
                    vol_mus = round(min(vol_mus + 0.1, 1.0), 2)
                    pygame.mixer.music.set_volume(vol_mus)
                    channel1.play(select)

                if vol_mus4_button.checkClick(volume_MousePos):
                    vol_mus = round(max(vol_mus - 0.1, 0.0), 2)
                    pygame.mixer.music.set_volume(vol_mus)
                    channel1.play(select)

        pygame.display.update()
        clock.tick(60)

#setările
def options():
    options_Text = subtitle_font.render("Options", True, "white")
    options_rect = options_Text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 - 150))

    controls_button = Button(pos=(SCREEN_WIDTH // 2 - 360, SCREEN_HEIGHT//2), image=button_surface, text_input="Controls", base_clr="white", hover_clr=(74, 87, 34))
    volume_button = Button(pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2), image=button_surface, text_input="Volume", base_clr="white", hover_clr=(74, 87, 34))
    back_button = Button(pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 + 150), image=button_surface, text_input="Back", base_clr="white", hover_clr=(74, 87, 34))
    fullscreen_button = Button(pos=(SCREEN_WIDTH // 2 + 360, SCREEN_HEIGHT//2), image=button_surface, text_input="Fullscreen", base_clr="white", hover_clr=(74, 87, 34))
    while True:
        screen.blit(bg_surface,bg_surface_rect)

        options_MousePos = pygame.mouse.get_pos()

        screen.blit(options_Text, options_rect)

        for button in [controls_button, volume_button, fullscreen_button, back_button]:
            button.changeColor(options_MousePos)
            button.update(screen)

        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if fullscreen_button.checkClick(options_MousePos):
                    channel1.play(select)
                    pygame.display.toggle_fullscreen()

                if controls_button.checkClick(options_MousePos):
                    channel1.play(select)
                    return "controls"
                
                if volume_button.checkClick(options_MousePos):
                    channel1.play(select)
                    return "volume"

                if back_button.checkClick(options_MousePos):
                    channel1.play(select)
                    return "main_menu"

        pygame.display.update()
        clock.tick(60)

#controale
def controls():
    controls_Text = subtitle_font.render("Controls", True, "white")
    controls_rect = controls_Text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 - 200))

    controls_mr = game_font.render("Move Right: D", True, "white")
    controls_mr_rect = controls_mr.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2 - 100))
    controls_r = game_font.render("Rotate: W", True, "white")
    controls_r_rect = controls_r.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2 -50))
    controls_ml = game_font.render("Move Left: A", True, "white")
    controls_ml_rect = controls_ml.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2))
    controls_sd = game_font.render("Soft Drop: S", True, "white")
    controls_sd_rect = controls_sd.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2 + 50))
    controls_hd = game_font.render("Hard Drop: Space", True, "white")
    controls_hd_rect = controls_hd.get_rect(center=(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT//2 + 100))

    controls_mr2 = game_font.render("Move Right: R-Arrow", True, "white")
    controls_mr2_rect = controls_mr2.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT//2 - 100))
    controls_r2 = game_font.render("Rotate: U-Arrow", True, "white")
    controls_r2_rect = controls_r2.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT//2 -50))
    controls_ml2 = game_font.render("Move Left: L-Arrow", True, "white")
    controls_ml2_rect = controls_ml2.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT//2))
    controls_sd2 = game_font.render("Soft Drop: D-Arrow", True, "white")
    controls_sd2_rect = controls_sd2.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT//2 + 50))
    controls_hd2 = game_font.render("Hard Drop: Space", True, "white")
    controls_hd2_rect = controls_hd2.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT//2 + 100))

    back_button = Button(pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 + 200), image=button_surface, text_input="Back", base_clr="white", hover_clr="Green")
    while True:
        screen.blit(bg_surface,bg_surface_rect)

        controls_MousePos = pygame.mouse.get_pos()

        screen.blit(controls_Text, controls_rect)
        screen.blit(controls_mr, controls_mr_rect)
        screen.blit(controls_r, controls_r_rect)
        screen.blit(controls_ml, controls_ml_rect)
        screen.blit(controls_sd, controls_sd_rect)
        screen.blit(controls_hd, controls_hd_rect)

        screen.blit(controls_mr2, controls_mr2_rect)
        screen.blit(controls_r2, controls_r2_rect)
        screen.blit(controls_ml2, controls_ml2_rect)
        screen.blit(controls_sd2, controls_sd2_rect)
        screen.blit(controls_hd2, controls_hd2_rect)

        for button in [back_button]:
            button.changeColor(controls_MousePos)
            button.update(screen)

        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkClick(controls_MousePos):
                    channel1.play(select)
                    return "options"

        pygame.display.update()
        clock.tick(60)

#meniul după moarte
def game_over():
    game_over_text = subtitle_font.render("Game Over", True, "white")
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))

    highscore_Text = game_font.render(f"High Score: {load_high_score("highscore.txt")}", True, (255,255,255))
    highscore_rect = highscore_Text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//3+70))

    retry_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +50), image=button_surface, text_input="Retry", base_clr="white", hover_clr=(74, 87, 34))
    back_button = Button(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150), image=button_surface, text_input="Back", base_clr="white", hover_clr=(74, 87, 34))

    while True:
        screen.blit(bg_surface,bg_surface_rect)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(game_over_text, game_over_rect)
        screen.blit(highscore_Text, highscore_rect)

        for button in [retry_button, back_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    channel1.play(select)
                    mgame.reset()
                    return "game"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    return "main_menu"
                if retry_button.checkClick(mouse_pos):
                    channel1.play(select)
                    pygame.mixer.music.rewind()
                    mgame.reset()
                    return "game"

        pygame.display.update()
        clock.tick(60)

#funcția principală
def main():
    level = 1
    state = "main_menu"

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    channel1.set_volume(0.2)

    while True:
        if state == "main_menu":
            state = main_menu()
        elif state == "game":
            mgame.reset()
            state = game()
        elif state == "volume":
            state = volume()
        elif state == "options":
            state = options()
        elif state == "controls":
            state = controls()
        elif state == "game_over":
            state = game_over()
        elif state == "quit":
            pygame.quit()
            exit()

main()