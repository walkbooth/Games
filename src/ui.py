# v1.1
import grid 
import yaml
import os 
import Tkinter as tkinter 
import tkMessageBox

def helloCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

"""
Creates an example, clean grid matching the specified dimenions
@param width the width of the example grid 
@param height the height of the example grid 
"""
def plain_grid(width, height):
    s = ""
    y = 0
    while y < height:
        x = 0
        while x < width:
            s += "* "
            x += 1
        y += 1 
        s += "\n"
    print s

"""
Console output version of minesweeper, introduced in v1.0
@param width the width of the grid 
@param height the height of the grid 
@param bombs the number of bombs to spawn in the grid 
"""
def launch_console(width, height, bombs):
    # Begin program
    os.system('cls' if os.name == 'nt' else 'clear')
    plain_grid(width, height)

    # Get input values and convert to a 0-based array 
    x, y = str.split(raw_input("Enter a coordinate to reveal in the form 'x y': "))
    x = int(x) - 1
    y = int(y) - 1

    # Safe reveal first tile 
    game_grid = grid.Grid(width, height, bombs, x, y)
    game_grid.reveal_tile(x, y)
    
    # Clear screen and print new grid after change
    os.system('cls' if os.name == 'nt' else 'clear')
    print(game_grid.to_s())

    # Game flow loop
    while game_grid.game_state() == 0:
        
        # Get input and convert to a 0-based array 
        action, x, y = str.split(raw_input("Enter a coordinate and an action in the form 'action x y' where action = reveal | flag: "))
        x = int(x) - 1
        y = int(y) - 1

        # Branch based on action 
        if action == "reveal":
            print "Revealing..."
            game_grid.reveal_tile(x, y)
        elif action == "flag":
            print "Flagging..."
            game_grid.flag_tile(x, y)
        else: 
            print("Invalid action, please try again.")
            continue
        
        # Clear screen and print new grid after change
        os.system('cls' if os.name == 'nt' else 'clear')
        print(game_grid.to_s())

    # End game 
    game_grid.reveal_all()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(game_grid.to_s())
    if game_grid.game_state() == 1: 
        print "You win!"
    elif game_grid.game_state() == -1:
        print "You lose :("

def launch_gui(width, height, bombs):
    print "Launching GUI"
    window = tkinter.Tk(className="v1.1 Walker's Minesweeper")
    
    resetButton = tkinter.Button(window, text = "Reset", command = helloCallBack)
    flagToggle = tkinter.Button(window, text = "Flag", command = helloCallBack)
    resetButton.pack(side = "left")
    flagToggle.pack(side = "right")
    window.mainloop()

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

    width = int(game_settings['width'])
    height = int(game_settings['height'])
    bombs = int(game_settings['bombs'])
    ui_type = game_settings['default_ui']

    if ui_type == "console":
        launch_console(width, height, bombs)
    elif ui_type == "gui":
        launch_gui(width, height, bombs)
    else:
        print "Invalid UI specifications in util/config.yaml. Please specify either console or gui."

# Standard python script boilerplate, calls main method 
if __name__ == '__main__':
    main()
