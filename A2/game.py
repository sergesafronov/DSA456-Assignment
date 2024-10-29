#   Author: Catherine Leung
#   This is the game that you will code the bots to play.  You can also play against your bot
#   To run the game you will need pygames installed.  See: https://pypi.org/project/pygame/
#   Once you have pygames, you can run the game by using the command:
#   python game.py
#   
#   the gem images used are from opengameart.org by qubodup
#   https://opengameart.org/content/rotating-crystal-animation-8-step,
#   https://creativecommons.org/licenses/by/3.0/

import pygame
import sys
import math

from a1_partd import overflow
from a1_partc import Queue
from player1 import PlayerOne
from player2 import PlayerTwo 

class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window, enabled = True):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        
        # Undo
        # Gray text color to demonstrate inactive button
        text_color = BLACK if enabled else GRAY 

        text = font.render(self.options[self.current_option], 1, text_color)
        window.blit(text, (self.x + 5, self.y + 5))

    # Undo
    # Return statements added to register 
    # mouse clicks specifically for undo button
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)
                return True # Undo
        return False # Undo

    def get_choice(self):
        return self.current_option



class Board:
    def __init__(self,width,height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height-1][self.width-1] = -1
        self.turn = 0

        # Undo        
        self.last_human_board = None # Track the last human board state
        self.is_undo = False # Helps to trigger or prevent AI move after undoing last move

        #Animation:
        self.overflow_animation = False
        self.overflow_position = None
        #Counter to manage animation duration
        self.animation_counter = 0
        #Tracks the current player (To determine what color the overflow animation is)
        self.current_player = 1
        self.animation_color = (0, 0, 0)
        #Rate in which the overflow animation fades
        self.fade_step = 30

        # Overflow counter
        self.p1_overflow_num = 0 # Counts Player 1's overflows
        self.p2_overflow_num = 0 # Counts Player 2's overflows
        self.p1_undo_overflow_num = 0 # Counts Player 1's oveflows for Undo
        self.p2_undo_overflow_num = 0 # Counts Player 2's oveflows for Undo

    #Animation:
    #Gradually fades the color to white by manually lerping the rgb values to white
    def fade_to_white(self, current_color, step):
        #Assuming current_color is (r,g,b) format:
        r = min(255, current_color[0] + step)
        g = min(255, current_color[1] + step)
        b = min(255, current_color[2] + step)
        return (r, g, b)
    
    #Animation:
    #Initializes the overflow animation
    def start_overflow_animation(self, row, col, player):
        self.overflow_animation = True
        self.overflow_position = (row, col)
        self.animation_counter = 10
        self.current_player = player
        if player > 0:
            self.animation_color = (0, 0, 255)
        else:
            self.animation_color =(0, 255, 0)

    #Animation:
    #Counter for the animation, updates the overflow animation's counter along its lifetime
    def update_overflow_animation(self):
        if self.overflow_animation is True:
            #Update the transparency of the animation over its lifetime
            self.animation_color = self.fade_to_white(self.animation_color, self.fade_step)
            self.animation_counter -= 1
            if self.animation_counter <= 0:
                self.overflow_animation = False
                self.overflow_position = None
                #Manually set the animation to white if the animation counter ends
                self.animation_color = (255, 255, 255)

    def get_board(self):
        current_board = []
        for i in range(self.height):
            current_board.append(self.board[i].copy())
        return current_board

    def valid_move(self, row,col,player):
        if row >= 0  and row < self.height and col >= 0 and col < self.width and (self.board[row][col]==0 or self.board[row][col]/abs(self.board[row][col]) == player):
            return True
        return False

    def add_piece(self, row, col, player):
        if self.valid_move(row, col, player):
            self.board[row][col] += player
            self.turn += 1
            return True
        return False
        
    # Undo
    # Rewinds the currant board to the last human board and ONLY one step back
    # Dose not rewinds AI's moves when the both players are AI 
    def undo_move(self):
        if self.last_human_board:
            self.board = self.last_human_board
            self.last_human_board = None
            self.is_undo = True  
            self.turn -= 1            

    def check_win(self):
        if(self.turn > 0):
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if(self.board[i][j] > 0):
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif(self.board[i][j] < 0):
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if(num_p1 == 0):
                return -1
            if(num_p2== 0):
                return 1
        return 0

    def do_overflow(self,q):
        oldboard = []
        for i in range(self.height):
            oldboard.append(self.board[i].copy())
        numsteps = overflow(self.board, q)
        if(numsteps != 0):
            self.set(oldboard)
        return numsteps
    
    def set(self, newboard):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE+Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    if self.board[row][col] > 0:
                        sprite = p1_sprites
                    else:
                        sprite = p2_sprites
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE //2 - 16
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

                    elif abs(self.board[row][col]) == 3:
                        cpos += CELL_SIZE //2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        cpos += CELL_SIZE //2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

        #Animation:
        #Draws the overflow animation during the draw loop (if an overflow is happening)
        #Note, the overflow colors can be changed, but they are right now set to the same color as the current player (blue/green)
        if self.overflow_animation is True and self.overflow_position is not None:
            row, col = self.overflow_position
            animation = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE + Y_OFFSET, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, self.animation_color, animation)
            #Redraws the border over the animation
            pygame.draw.rect(window, BLACK, animation, 1)


# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5

# hate the colours?  there are other options.  Just change the lines below to another colour's file name.  
# the following are available blue, pink, yellow, orange, grey, green
p1spritesheet = pygame.image.load('blue.png')
p2spritesheet = pygame.image.load('green.png')
p1_sprites = []
p2_sprites = []


player_id = [1 , -1]


for i in range(8):
    curr_sprite = pygame.Rect(32*i,0,32,32)
    p1_sprites.append(p1spritesheet.subsurface(curr_sprite))
    p2_sprites.append(p2spritesheet.subsurface(curr_sprite))    


frame = 0

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((1200,800))

pygame.font.init()
font = pygame.font.Font(None, 36)  # Change the size as needed
bigfont = pygame.font.Font(None, 108)
# Create the game board
# board = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
player1_dropdown = Dropdown(900, 50, 200, 50, ['Player 1', 'Player 1 (AI)'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Player 2', 'Player 2 (AI)'])

# Undo
# Creates an instance of the button
undo_button = Dropdown(900, 170, 200, 50, ['Undo'])

status=["",""]
current_player = 0
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)

# Game loop
running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]

while running:

    # Undo
    # Resets is_undo state during the game loop 
    # to allow human or AI make a move during their turn  
    board.is_undo = False
   
    # Undo
    # Allows AI to make moves if both players selected are AIs 
    # and prohibits undo board for them 
    if choice[0] == 1 and choice[1] == 1:
        board.is_undo = False
        board.last_human_board = None   

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)
            choice[0] = player1_dropdown.get_choice()
            choice[1] = player2_dropdown.get_choice()

            # Undo
            # Performs undo when the button is clicked,
            # switches the turn to the right player,
            # clears the last AI move information (message)
            if undo_button.handle_event(event):
                if board.last_human_board is not None:
                    board.undo_move()                    
                    current_player = (current_player - 1) % 2

                    # Overflow Counter for Undo
                    # Reverts the overflow counter to its previous state when an Undo action is performed
                    if current_player == 0:
                        board.p1_overflow_num = board.p1_undo_overflow_num
                    else:
                        board.p2_overflow_num = board.p2_undo_overflow_num

                    status[0] = "" 
                    status[1] = "" 

            if event.type == pygame.MOUSEBUTTONDOWN:        
                x,y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET    
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE

    win = board.check_win()
    if win != 0:
        winner = 1
        if win == -1:
            winner = 2
        has_winner = True

    if not has_winner:  

        # Overflow Counter
        # Sets a text area for overflow counter for the both players
        p1_counter_surface = font.render(f'P1\'s Overflows: {board.p1_overflow_num}', True, BLACK)
        p2_counter_surface = font.render(f'P2\'s Overflows: {board.p2_overflow_num}', True, BLACK)    

        if overflowing:
            status[0] = "Overflowing"
            if not overflow_boards.is_empty():
                if repeat_step == FULL_DELAY:
                    next = overflow_boards.dequeue()
                    board.set(next)
                                        
                    # Overflow Counter
                    # Increments the number of overflows for the current player whenever an overflow occurs
                    if current_player == 0:
                        board.p1_overflow_num += 1
                    else:
                        board.p2_overflow_num += 1
                    
                    repeat_step = 0
                else:
                    repeat_step += 1
            else:
                overflowing = False

                # goes between 0 and 1
                current_player = (current_player + 1) % 2

        else:
            status[0] = "Player " + str(current_player + 1) + "'s turn"
            make_move = False           
                      

            if choice[current_player] == 1:
                
                # Undo
                # Prohibits AI from making a move right after undo button was clicked 
                # AI will wait until human will make a move after the last human's move was undone  
                if not board.is_undo:

                    (grid_row,grid_col) = bots[current_player].get_play(board.get_board())
                    status[1] = "Bot chose row {}, col {}".format(grid_row, grid_col)
                    if not board.valid_move(grid_row, grid_col, player_id[current_player]):
                        has_winner = True
                        # if p1 makes an invalid move, p2 wins.  if p2 makes an invalid move p1 wins
                        winner = ((current_player + 1) % 2) + 1                    
                make_move = True

            else:
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True
                    board.is_undo = False

            if make_move:
                
                # Undo
                # Determines if the current player is human for various AI vs human selection
                # and overrides the last human board
                if (player1_dropdown.get_choice() == 0 if current_player == 0 else player2_dropdown.get_choice() == 0):
                    board.last_human_board = board.get_board()


                board.add_piece(grid_row, grid_col, player_id[current_player])
                numsteps = board.do_overflow(overflow_boards)

                # Overflow Counter
                # Captures the current number of overflows for both players 
                # to accurately revert to the previous state (for Undo) 
                board.p1_undo_overflow_num = board.p1_overflow_num
                board.p2_undo_overflow_num = board.p2_overflow_num


                if numsteps != 0:
                    overflowing = True
                    repeat_step = 0
                    #Call the overflow animation
                    board.start_overflow_animation(grid_row, grid_col, player_id[current_player])
                else:
                    current_player = (current_player + 1) % 2
                grid_row = -1
                grid_col = -1   

    # Draw the game board
    window.fill(WHITE)
    board.draw(window,frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))
    frame = (frame + 0.5) % 8
    player1_dropdown.draw(window)
    player2_dropdown.draw(window)

    # Undo
    # Draws the button on the game window
    # and sets it active or inactive based on the last human board
    undo_button.draw(window, board.last_human_board is not None)

    # Oveflow Counter
    # Draws text areas to diplay each player's numbers of oveflows
    window.blit(p1_counter_surface, (900, 230))
    window.blit(p2_counter_surface, (900, 290))



    if not has_winner:  
        text = font.render(status[0], True, BLACK)  
        window.blit(text, (X_OFFSET, 750 ))
        text = font.render(status[1], True, BLACK) 
        window.blit(text, (X_OFFSET,  700 ))
    else:
        text = bigfont.render("Player " + str(winner)  + " wins!", True, BLACK)  
        window.blit(text, (300, 250))


        # Overflow Counter
        # Overrides text areas to display the final total number of overflows for each player at the end
        p1_counter_surface = font.render(f'P1\'s Overflows: {board.p1_overflow_num}', True, BLACK)
        p2_counter_surface = font.render(f'P2\'s Overflows: {board.p2_overflow_num}', True, BLACK) 

        # Undo
        # Makes the button inactive in case any player wins
        board.last_human_board = None

    #Animation:
    #Updates the overflow animation
    board.update_overflow_animation()
    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()