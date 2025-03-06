import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 500, 600
GRID_SIZE = 4 
TILE_SIZE = 105
GRID_PADDING = 15
FONT_SIZE = 40 
ANIMATION_SPEED = 15

# Define colors for the game
BACKGROUND_COLOR = (40, 44, 52)
EMPTY_TILE_COLOR = (60, 64, 72)
TILE_COLORS = {
    0: (60, 64, 72),
    2: (78, 90, 115),
    4: (95, 129, 157),
    8: (124, 153, 180),
    16: (141, 175, 199),
    32: (152, 195, 121),
    64: (229, 192, 123),
    128: (224, 108, 117),
    256: (198, 120, 221),
    512: (171, 178, 191),
    1024: (130, 170, 255),
    2048: (255, 135, 135)
}
TEXT_COLORS = {
    2: (220, 223, 228),
    4: (220, 223, 228),
    8: (220, 223, 228),
    16: (220, 223, 228),
    32: (220, 223, 228),
    64: (220, 223, 228),
    128: (220, 223, 228),
    256: (220, 223, 228),
    512: (220, 223, 228),
    1024: (220, 223, 228),
    2048: (220, 223, 228)
}

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
small_font = pygame.font.SysFont("Arial", 24)

# Initialize AI mode
use_ai = False

# Define the game class
# Define the Game2048 class
class Game2048:
    # Initialize the game
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.animations = []
        self.add_new_tile()
        self.add_new_tile()
    
    # Add a new tile to the grid
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
            self.animations.append({
                'type': 'new',
                'row': i,
                'col': j,
                'progress': 0,
                'duration': 10
            })

    # Move the tiles in the grid
    def move(self, direction):
        if self.game_over:
            return False
        
        moved = False
        if direction == "up":
            moved = self.move_up()
        elif direction == "down":
            moved = self.move_down()
        elif direction == "left":
            moved = self.move_left()
        elif direction == "right":
            moved = self.move_right()
        
        if moved:
            self.add_new_tile()
            self.check_game_over()
        
        return moved

    # Move the tiles to the left
    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            for j in range(1, GRID_SIZE):
                if self.grid[i][j] != 0:
                    k = j
                    while k > 0 and self.grid[i][k-1] == 0:
                        self.grid[i][k-1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k -= 1
                        moved = True
                        self.animations.append({
                            'type': 'slide',
                            'from_row': i,
                            'from_col': j,
                            'to_row': i,
                            'to_col': k,
                            'progress': 0,
                            'duration': 8
                        })
                    
                    if k > 0 and self.grid[i][k-1] == self.grid[i][k]:
                        value = self.grid[i][k] * 2
                        self.grid[i][k-1] = value
                        self.score += value
                        self.grid[i][k] = 0
                        moved = True
                        self.animations.append({
                            'type': 'merge',
                            'row': i,
                            'col': k-1,
                            'progress': 0,
                            'duration': 8,
                            'value': value
                        })
                        if value == 2048 and not self.won:
                            self.won = True
        return moved

    # Move the tiles to the right
    def move_right(self):
        moved = False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE-2, -1, -1):
                if self.grid[i][j] != 0:
                    k = j
                    while k < GRID_SIZE-1 and self.grid[i][k+1] == 0:
                        self.grid[i][k+1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k += 1
                        moved = True
                        self.animations.append({
                            'type': 'slide',
                            'from_row': i,
                            'from_col': j,
                            'to_row': i,
                            'to_col': k,
                            'progress': 0,
                            'duration': 8
                        })
                    
                    if k < GRID_SIZE-1 and self.grid[i][k+1] == self.grid[i][k]:
                        value = self.grid[i][k] * 2
                        self.grid[i][k+1] = value
                        self.score += value
                        self.grid[i][k] = 0
                        moved = True
                        self.animations.append({
                            'type': 'merge',
                            'row': i,
                            'col': k+1,
                            'progress': 0,
                            'duration': 8,
                            'value': value
                        })
                        if value == 2048 and not self.won:
                            self.won = True
        return moved

    # Move the tiles up
    def move_up(self):
        moved = False
        for j in range(GRID_SIZE):
            for i in range(1, GRID_SIZE):
                if self.grid[i][j] != 0:
                    k = i
                    while k > 0 and self.grid[k-1][j] == 0:
                        self.grid[k-1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k -= 1
                        moved = True
                        self.animations.append({
                            'type': 'slide',
                            'from_row': i,
                            'from_col': j,
                            'to_row': k,
                            'to_col': j,
                            'progress': 0,
                            'duration': 8
                        })
                    
                    if k > 0 and self.grid[k-1][j] == self.grid[k][j]:
                        value = self.grid[k][j] * 2
                        self.grid[k-1][j] = value
                        self.score += value
                        self.grid[k][j] = 0
                        moved = True
                        self.animations.append({
                            'type': 'merge',
                            'row': k-1,
                            'col': j,
                            'progress': 0,
                            'duration': 8,
                            'value': value
                        })
                        if value == 2048 and not self.won:
                            self.won = True
        return moved

    # Move the tiles down
    def move_down(self):
        moved = False
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE-2, -1, -1):
                if self.grid[i][j] != 0:
                    k = i
                    while k < GRID_SIZE-1 and self.grid[k+1][j] == 0:
                        self.grid[k+1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k += 1
                        moved = True
                        self.animations.append({
                            'type': 'slide',
                            'from_row': i,
                            'from_col': j,
                            'to_row': k,
                            'to_col': j,
                            'progress': 0,
                            'duration': 8
                        })
                    
                    if k < GRID_SIZE-1 and self.grid[k+1][j] == self.grid[k][j]:
                        value = self.grid[k][j] * 2
                        self.grid[k+1][j] = value
                        self.score += value
                        self.grid[k][j] = 0
                        moved = True
                        self.animations.append({
                            'type': 'merge',
                            'row': k+1,
                            'col': j,
                            'progress': 0,
                            'duration': 8,
                            'value': value
                        })
                        if value == 2048 and not self.won:
                            self.won = True
        return moved

    # Check if the game is over
    def check_game_over(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if j < GRID_SIZE-1 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if i < GRID_SIZE-1 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
        
        self.game_over = True
        return True

    # Reset the game
    def reset(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.animations = []
        self.add_new_tile()
        self.add_new_tile()

    # Update the animations
    def update_animations(self):
        completed = []
        for i, anim in enumerate(self.animations):
            anim['progress'] += 1
            if anim['progress'] >= anim['duration']:
                completed.append(i)
        
        for i in sorted(completed, reverse=True):
            self.animations.pop(i)

    # Make a move using the AI
    def ai_move(self):
        try:
            best_move = self.expectimax()
            if best_move:
                self.move(best_move)
        except Exception as e:
            print(f"AI Error: {e}")

    # Use the expectimax algorithm to find the best move
    def expectimax(self, depth=2):
        def max_value(grid, depth):
            if depth == 0:
                return self.evaluate(grid)
            max_utility = float('-inf')
            for move in ["up", "down", "left", "right"]:
                new_grid, moved = self.simulate_move(grid, move)
                if moved:
                    max_utility = max(max_utility, exp_value(new_grid, depth - 1))
            return max_utility if max_utility != float('-inf') else self.evaluate(grid)

        def exp_value(grid, depth):
            empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
            if not empty_cells:
                return max_value(grid, depth)
            
            total_utility = 0
            for i, j in empty_cells:
                for value, prob in [(2, 0.9), (4, 0.1)]:
                    new_grid = [row[:] for row in grid]
                    new_grid[i][j] = value
                    total_utility += prob * max_value(new_grid, depth)
            return total_utility / len(empty_cells)

        best_move = None
        max_utility = float('-inf')
        for move in ["up", "down", "left", "right"]:
            new_grid, moved = self.simulate_move(self.grid, move)
            if moved:
                utility = exp_value(new_grid, depth - 1)
                if utility > max_utility:
                    max_utility = utility
                    best_move = move
        return best_move

    # Simulate a move in the grid
    def simulate_move(self, grid, move):
        new_grid = [row[:] for row in grid]
        moved = False
        
        if move == "left":
            moved = self._simulate_move_left(new_grid)
        elif move == "right":
            moved = self._simulate_move_right(new_grid)
        elif move == "up":
            moved = self._simulate_move_up(new_grid)
        elif move == "down":
            moved = self._simulate_move_down(new_grid)
            
        return new_grid, moved

    # Simulate a move to the left
    def _simulate_move_left(self, grid):  
        moved = False
        for i in range(GRID_SIZE):
            for j in range(1, GRID_SIZE):
                if grid[i][j] != 0:
                    k = j
                    while k > 0 and grid[i][k-1] == 0:
                        grid[i][k-1] = grid[i][k]
                        grid[i][k] = 0
                        k -= 1
                        moved = True
                    
                    if k > 0 and grid[i][k-1] == grid[i][k]:
                        grid[i][k-1] *= 2
                        grid[i][k] = 0
                        moved = True
        return moved

    # Simulate a move to the right
    def _simulate_move_right(self, grid):
        moved = False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE-2, -1, -1):
                if grid[i][j] != 0:
                    k = j
                    while k < GRID_SIZE-1 and grid[i][k+1] == 0:
                        grid[i][k+1] = grid[i][k]
                        grid[i][k] = 0
                        k += 1
                        moved = True
                    
                    if k < GRID_SIZE-1 and grid[i][k+1] == grid[i][k]:
                        grid[i][k+1] *= 2
                        grid[i][k] = 0
                        moved = True
        return moved

    # Simulate a move up
    def _simulate_move_up(self, grid):
        moved = False
        for j in range(GRID_SIZE):
            for i in range(1, GRID_SIZE):
                if grid[i][j] != 0:
                    k = i
                    while k > 0 and grid[k-1][j] == 0:
                        grid[k-1][j] = grid[k][j]
                        grid[k][j] = 0
                        k -= 1
                        moved = True
                    
                    if k > 0 and grid[k-1][j] == grid[k][j]:
                        grid[k-1][j] *= 2
                        grid[k][j] = 0
                        moved = True
        return moved

    # Simulate a move down
    def _simulate_move_down(self, grid):
        moved = False
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE-2, -1, -1):
                if grid[i][j] != 0:
                    k = i
                    while k < GRID_SIZE-1 and grid[k+1][j] == 0:
                        grid[k+1][j] = grid[k][j]
                        grid[k][j] = 0
                        k += 1
                        moved = True
                    
                    if k < GRID_SIZE-1 and grid[k+1][j] == grid[k][j]:
                        grid[k+1][j] *= 2
                        grid[k][j] = 0
                        moved = True
        return moved

    # Evaluate the grid
    def evaluate(self, grid):
        empty_cells = sum(1 for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0)
        max_tile = max(max(row) for row in grid)
        monotonicity = self._calculate_monotonicity(grid)
        
        return empty_cells * 10.0 + max_tile * 2.0 + monotonicity * 5.0

    # Calculate the monotonicity of the grid
    def _calculate_monotonicity(self, grid):
        score = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if grid[i][j] >= grid[i][j + 1] and grid[i][j] != 0:
                    score += 1

        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 1):
                if grid[i][j] >= grid[i + 1][j] and grid[i][j] != 0:
                    score += 1
        return score

# Function to draw a tile
def draw_tile(x, y, value, animations=None):
    # Determine the color of the tile based on its value
    color = TILE_COLORS.get(value, TILE_COLORS[2048])
    scale = 1.0 
    if animations:
        # Adjust scale based on animations
        for anim in animations:
            if anim['type'] == 'new' and value != 0:
                scale = anim['progress'] / anim['duration']
            elif anim['type'] == 'merge':
                progress_ratio = anim['progress'] / anim['duration']
                if progress_ratio < 0.5:
                    scale = 1.0 + 0.2 * (progress_ratio * 2)
                else:
                    scale = 1.0 + 0.2 * (1 - (progress_ratio - 0.5) * 2)
    
    # Calculate the scaled size of the tile
    scaled_size = int(TILE_SIZE * scale)
    offset = (TILE_SIZE - scaled_size) // 2  
    pygame.draw.rect(screen, color, (x + offset, y + offset, scaled_size, scaled_size), border_radius=5)
    
    # Draw the value of the tile if it's not zero
    if value != 0:
        text_color = TEXT_COLORS.get(value, TEXT_COLORS[2048])
        text_size = FONT_SIZE if value < 512 else FONT_SIZE - 8
        font = pygame.font.SysFont("Arial", text_size, bold=True)
        text = font.render(str(value), True, text_color)
        text_rect = text.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
        screen.blit(text, text_rect)

# Function to draw the game grid
def draw_grid(game):
    screen.fill(BACKGROUND_COLOR)  
    
    # Draw the AI mode button
    ai_button_rect = pygame.Rect(WIDTH - 180, 20, 160, 60)
    pygame.draw.rect(screen, (60, 64, 72), ai_button_rect, border_radius=10)
    ai_label = small_font.render("AI MODE", True, (171, 178, 191))
    ai_status = small_font.render("ON" if use_ai else "OFF", True, 
                          (152, 195, 121) if use_ai else (224, 108, 117))
    screen.blit(ai_label, (ai_button_rect.centerx - ai_label.get_width()//2, ai_button_rect.y + 10))
    screen.blit(ai_status, (ai_button_rect.centerx - ai_status.get_width()//2, ai_button_rect.y + 30))
    
    # Draw the grid outline
    grid_rect = pygame.Rect(GRID_PADDING, 100, WIDTH - 2*GRID_PADDING, WIDTH - 2*GRID_PADDING)
    pygame.draw.rect(screen, (50, 54, 62), grid_rect, border_radius=5)
    
    # Draw each tile in the grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = GRID_PADDING + j * (TILE_SIZE + GRID_PADDING)
            y = 100 + i * (TILE_SIZE + GRID_PADDING)
            pygame.draw.rect(screen, EMPTY_TILE_COLOR, (x, y, TILE_SIZE, TILE_SIZE), border_radius=5)
            
            if game.grid[i][j] != 0:
                tile_animations = [a for a in game.animations if 
                               (a['type'] == 'new' and a['row'] == i and a['col'] == j) or
                               (a['type'] == 'merge' and a['row'] == i and a['col'] == j)]
                draw_tile(x, y, game.grid[i][j], tile_animations)
    
    # Draw the score background and text
    score_bg = pygame.Rect(20, 20, 160, 60)
    pygame.draw.rect(screen, (60, 64, 72), score_bg, border_radius=10)
    score_label = small_font.render("SCORE", True, (171, 178, 191))
    score_text = small_font.render(f"{game.score}", True, (220, 223, 228))  # Changed font to small_font for smaller text
    screen.blit(score_label, (score_bg.centerx - score_label.get_width()//2, score_bg.y + 10))
    screen.blit(score_text, (score_bg.centerx - score_text.get_width()//2, score_bg.y + 30))
    
    # Draw game over or win screens if necessary
    if game.game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        game_over_text = font.render("Game Over!", True, (255, 255, 255))
        restart_text = small_font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))
    
    elif game.won:
        win_text = font.render("You Win!", True, (152, 195, 121))
        continue_text = small_font.render("Keep playing or press R to restart", True, (171, 178, 191))
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, 65))
        screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT - 30))


def main():
    try:
        # Initialize the game and set up the game loop
        game = Game2048()
        running = True
        global use_ai 
        use_ai = False
        clock = pygame.time.Clock()
        ai_delay = 300  # Delay between AI moves in milliseconds
        last_ai_move = 0  # Timestamp of the last AI move
        ai_button_rect = pygame.Rect(WIDTH - 180, 20, 160, 60)  # Rectangle for the AI button

        while running:
            current_time = pygame.time.get_ticks()  # Get the current time
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ai_button_rect.collidepoint(event.pos):
                        use_ai = not use_ai  # Toggle AI mode
                        print("AI:", "Enabled" if use_ai else "Disabled")
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()  # Reset the game
                    elif event.key == pygame.K_SPACE:  
                        use_ai = not use_ai  # Toggle AI mode
                        print("AI:", "Enabled" if use_ai else "Disabled")
                    elif not use_ai:  # If AI mode is off, allow manual moves
                        if event.key == pygame.K_LEFT:
                            game.move("left")
                        elif event.key == pygame.K_RIGHT:
                            game.move("right")
                        elif event.key == pygame.K_UP:
                            game.move("up")
                        elif event.key == pygame.K_DOWN:
                            game.move("down")
            
            # Check if it's time for the AI to make a move
            if use_ai and current_time - last_ai_move >= ai_delay and not game.game_over:
                game.ai_move()  # Make the AI move
                last_ai_move = current_time  # Update the last move time

            # Update animations and draw the grid
            game.update_animations()
            draw_grid(game)
            pygame.display.flip()  # Update the display
            clock.tick(60)  # Cap the frame rate

    except Exception as e:
        print(f"Error: {e}")  # Print any errors that occur
        import traceback
        traceback.print_exc()  # Print the traceback for debugging
    finally:
        pygame.quit()  # Quit pygame
        sys.exit()  # Exit the program
if __name__ == "__main__":
    main()
