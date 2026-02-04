import os
import json
import sys

# Constants
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_1 = 1  # User (Yellow)
PLAYER_2 = 2  # Opponent (Red)

# File Paths
DATA_DIR = "data"
BOARD_FILE = os.path.join(DATA_DIR, "board.json")
README_FILE = "README.md"

def load_board():
    if not os.path.exists(BOARD_FILE):
        return [[EMPTY] * COLS for _ in range(ROWS)], PLAYER_1
    with open(BOARD_FILE, 'r') as f:
        data = json.load(f)
        return data.get('board', [[EMPTY] * COLS for _ in range(ROWS)]), data.get('turn', PLAYER_1)

def save_board(board, turn):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(BOARD_FILE, 'w') as f:
        json.dump({'board': board, 'turn': turn}, f)

def drop_piece(board, col, player):
    if board[0][col] != EMPTY:
        return False # Column full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = player
            return True
    return False

def check_win(board, piece):
    # Check horizontal
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Check positive diagonal
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Check negative diagonal
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

def generate_svg(board):
    # Simple SVG generation for the board
    cell_size = 50
    padding = 5
    width = COLS * cell_size
    height = ROWS * cell_size
    
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    svg += f'<rect width="{width}" height="{height}" fill="#0000FF" />' # Blue background
    
    for r in range(ROWS):
        for c in range(COLS):
            cx = c * cell_size + cell_size // 2
            cy = r * cell_size + cell_size // 2
            radius = (cell_size - padding * 2) // 2
            
            color = "#FFFFFF" # Empty (White)
            if board[r][c] == PLAYER_1:
                color = "#FFFF00" # Yellow
            elif board[r][c] == PLAYER_2:
                color = "#FF0000" # Red
                
            svg += f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{color}" />'
            
    svg += '</svg>'
    return svg

def update_readme(svg_content):
    # This is a placeholder. In a real scenario, we'd save the SVG to a file and link it.
    # For now, we'll save it to 'connect4.svg'
    with open("connect4.svg", "w") as f:
        f.write(svg_content)

def main():
    # Argument 1: Column index (0-6) from Issue Title usually
    try:
        col = int(sys.argv[1])
    except:
        print("Invalid move")
        return

    board, turn = load_board()
    
    if col < 0 or col >= COLS:
        print("Invalid column")
        return

    # User move
    if drop_piece(board, col, PLAYER_2): # Assumption: User via issue is Player 2 (Red)
        if check_win(board, PLAYER_2):
            print("Player 2 Wins!")
            # Reset logic could go here
        
        # AI/System move (Player 1 - Yellow) - Random or simple
        # For simplicity, just next available spot in random column or simple logic
        import random
        ai_col = random.randint(0, COLS-1)
        # simplistic ai retry
        for _ in range(10):
            if drop_piece(board, ai_col, PLAYER_1):
                break
            ai_col = random.randint(0, COLS-1)
            
        if check_win(board, PLAYER_1):
            print("Player 1 Wins!")
            
        save_board(board, turn)
        svg = generate_svg(board)
        update_readme(svg)
    else:
        print("Column full")

if __name__ == "__main__":
    main()
