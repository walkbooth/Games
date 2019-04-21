import sys, termios, tty 
# v1.1
import grid 
import yaml
import os

"""
Gets a character or arrow key input from user. Thanks to Newb for the answer here: 
https://stackoverflow.com/questions/22397289/finding-the-values-of-the-arrow-keys-in-python-why-are-they-triples
"""
def getchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if (ch == '\x1b'):
                ch = sys.stdin.read(2)
    finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def reveal(grid):
    grid.reveal_tile()

def flag(grid):
    grid.flag_tile()

def up(grid):
    grid.up()

def down(grid):
    grid.down()    

def left(grid):    
    grid.left()

def right(grid):  
    grid.right()  

def leave(grid):
    exitpoint()

def invalid(grid):
    return "Invalid option selected: options are r|f|q or arrow keys"

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def exitpoint():
    print("Press any key to continue... \033[1;0;0m")
    getchar()
    clearscreen()
    exit(0)

options = {
    "r": reveal,
    "f": flag, 
    "q": leave, 
    "[A": up,
    "[B": down,
    "[C": right,
    "[D": left
}

def launch_console(width, height, bombs):
    # Set game color
    print("\033[1;37;40m")
    clearscreen()

    # Initialize and print grid 
    game_grid = grid.Grid(width, height, bombs)
    print( game_grid.to_s() )

    # Selection for first tile 
    option = None  
    while option != "r":

        option = getchar()
        clearscreen()

        func = options.get(option, invalid)
        func(game_grid)
        print ( game_grid.to_s() )

    # Remainder of game
    while game_grid.game_state() == 0:
        
        # Get input and convert to a 0-based array 
        option = getchar()

        clearscreen()

        func = options.get(option, invalid)
        func(game_grid)
        print ( game_grid.to_s() )

    # End game 
    game_grid.reveal_all()
    clearscreen()
    print(game_grid.to_s())
    if game_grid.game_state() == 1: 
        print ("You win!")
    elif game_grid.game_state() == -1:
        print ("You lose :(")

"""
Game logic, i/o for a standard game of minesweeper
Preconditions:
    - util/config.yml contains configuration parameters, such as grid dimensions and number of bombs.
"""
def main():

    # Parse util/config.yml for game settings 
    game_settings = {}
    with open("util/config.yml", 'r') as stream:
        try:
            game_settings = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Import settings into variables 
    width = int(game_settings['width'])
    height = int(game_settings['height'])
    bombs = int(game_settings['bombs'])
    
    # Start the game
    launch_console(width, height, bombs)

    # Exit the game 
    exitpoint()

# Standard python script boilerplate, calls main method 
if __name__ == '__main__':
    main()

        