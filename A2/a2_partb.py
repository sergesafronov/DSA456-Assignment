from a1_partc import Queue
from a1_partd import absolute_value, overflow


# Constants
WINNING_SCORE = 1000000
LOSING_SCORE = -1000000
WINNING_THRESHOLD = 999999
LOSING_THRESHOLD = -999999
PLAYER_ONE = 1
PLAYER_TWO = -1


# This function duplicates and returns the board. You may find this useful
def copy_board(board):
        current_board = []
        height = len(board)
        for i in range(height):
            current_board.append(board[i].copy())
        return current_board


# Determine the score valuation for a given board
# Player 1 and player 2 must be treated differently to accommodate for the positive/negative sign
def evaluate_board(board, player):
    
    player_score = 0
    opponent_score = 0

    for row in board:
        for cell in row:
            if (player == PLAYER_ONE and cell > 0) or (player == PLAYER_TWO and cell < 0):
                player_score += absolute_value(cell)  
            else:
                opponent_score += absolute_value(cell)  

    if player_score > 0 and opponent_score == 0:
        return WINNING_SCORE
    elif player_score == 0 and opponent_score > 0:
        return LOSING_SCORE
    return player_score - opponent_score


# Determine valid moves for a player on a given board state.
# Moves can only be made on cells that contain your own gems. 
# Positive or negative depending on player or empty (zero).
def get_possible_moves(board, player):
    
    height = len(board)
    width = len(board[0])
    moves = []
    
    for i in range(height):
        for j in range(width):
            if player == PLAYER_ONE:
                if board[i][j] >= 0:
                    moves.append((i, j))
            elif player == PLAYER_TWO:
                if board[i][j] <= 0:
                    moves.append((i, j))
    return moves


class GameTree:

    class Node:
        # Initializes Node
        def __init__(self, board, depth, player, tree_height = 4):
            self.board = copy_board(board) # A copy of the game board state
            self.depth = depth                   # The current depth of the node
            self.player = player                 # Current player
            self.tree_height = tree_height       # Maximum height of the game tree
            self.parent = None                   # Parent node of a current node
            self.children = []                   # A list of child nodes
            self.score = None                    # Score of this node
            self.previous_move = None            # Previous move that led to this board state

        # Checks if the current game is in a winning state
        def is_game_won(self):
            current_score = evaluate_board(self.board, self.player)
            if current_score > WINNING_THRESHOLD:
                return True
            elif current_score < LOSING_THRESHOLD:
                return True
            return False

        # Returns true if the node has reached the maximum depth
        # otherwise returns false
        def is_max_height(self):
            if self.depth >= self.tree_height - 1:
                return True
            else:
                return False
        
        # Adds a child node to this node's list of children
        # and sets this node as the parent of the child
        def add_child(self, node):
            self.children.append(node)
            node.parent = self 

        # Sets the score
        def set_score(self, score):
            self.score = score
        
        # Returns a list of child nodes
        def get_children(self):
            return self.children
        
        # Returns the parent of this node
        def get_parent(self):
            return self.parent


    # Initializes GameTree
    def __init__(self, board, player, tree_height = 4):
        self.board = copy_board(board)
        self.player = player
        self.tree_height = tree_height
        #Initialize the root node of the tree
        self.root = self.Node(self.board, 0, self.player, tree_height)
        #Start tree creation from the root node
        self.create_tree(self.root)


    # Builds the game tree by expanding each node
    # if it hasn't reached the maximum height or a win state
    def create_tree(self, node):

        # If the node is at maximum height (depth) or in a winning state
        # calculate and set its score
        if node.is_max_height() or node.is_game_won():
            board_score = evaluate_board(node.board, node.player) * node.player
            node.set_score(board_score)
        
        else:
            # Get all possible moves for the current player and board
            possible_moves = get_possible_moves(node.board, node.player)

            for move in possible_moves:
                
                # Copy board
                # For each possible move set a cell to a players's identifier (1 or -1)
                board = copy_board(node.board)
                board[move[0]][move[1]] += node.player

                # Overflow the board
                queue = Queue()
                overflow(board, queue)       

                # Create a new node in the tree with the overflowed board
                # Store the move that lead to the state
                # Add the new node as a child, continue building the tree recursively
                new_node = self.Node(board, node.depth + 1, node.player * -1, self.tree_height)
                new_node.previous_move = move  
                node.add_child(new_node)
                self.create_tree(new_node)
        

    def minimax(self, node, depth, is_max_player):
        #Base case: If the game ends in a win/loss/draw
        #Or we reach the maximum height
        if node.is_max_height() or node.is_game_won():
            return (node, node.score)

        #Ensuring the max player starts with the lowest possible score, and the min player with the highest possible score
        if is_max_player:
            best_score = float('-inf')
        else:
            best_score = float('inf')

        best_move = None

        #Cycles through the next possible moves, alternating turns between the min and max player
        for child in node.get_children():
            _, child_score = self.minimax(child, depth + 1, not is_max_player)

            #Updates the min/max score if a better score is found
            if is_max_player and child_score > best_score:
                best_score = child_score
                best_move = child
            elif not is_max_player and child_score < best_score:
                best_score = child_score
                best_move = child
                    
        #Return the best move
        return (best_move, best_score)

    # Finds the optimal move from the current board state
    # using the minimax algorithm
    def get_move(self): 
           
        maximized_moves = self.minimax(self.root, 0, True if self.player == 1 else False)

        # Hols the optimal next node or best move
        current_move = maximized_moves[0]

        # Find the move that led to the current move
        optimal_move = current_move.previous_move
        
        # Moves up the tree to trace the sequence of moves
        # from the root to the chosen node
        while current_move.get_parent() is not None and current_move.get_parent() != self.root:
            current_move = current_move.get_parent()
            optimal_move = current_move.previous_move

        return optimal_move   
    
    # Unlinks all nodes to allow the garbage collector
    # to clear the memory
    def clear_tree(self):
        def clear_node(node):
            for child in node.children:
                clear_node(child)
            node.children = None
        self.root = clear_node(self.root)  
