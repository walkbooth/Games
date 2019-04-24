import tile
import random

RED = "\033[1;31;40m"
NORMAL = "\033[1;37;40m"
GREEN = "\033[1;32;40m"
YELLOW = "\033[1;33;40m"

COLOR_MAP = {
    "B": RED,
    "_": GREEN,
    "!": RED,
    "*": NORMAL
}

class Grid ():

    """
    Helper function to increment the bomb counter of a tile which has a bomb adjacent to it 
    @param x the x coordinate of the bomb 
    @param y the y coordinate of the bomb 
    """
    def _notify_adj_tiles(self, x, y):
        # Iterate over all possible tiles which should be notified
        for rows in range(y-1, y+2):
            for cols in range(x-1, x+2):
                if (cols != x or rows != y):
                    # If a tile is not valid, ignore and continue 
                    try:
                        self._get_tile(cols, rows).add_adj_bomb()
                    except IndexError:
                        continue 

    """
    Helper function to randomly generate valid locations for bombs based on game configuration. 
    @return bombs a list of valid locations for bombs to be placed in the grid 
    """ 
    def _generate_bomb_locations(self):

        x = self._selected["x"]
        y = self._selected["y"]

        # Locate and place bombs, excluding first tile from the potential bomb spots 
        valid_spots = set(range(0, self._width * self._height))
        if not x == None and not y == None:
            upper_left = (y - 1) * self._width + x - 1 
            valid_spots -= set(list(range(upper_left, upper_left + 3)) +
                               list(range(upper_left + self._width, upper_left + self._width + 3)) +
                               list(range(upper_left + 2 * self._width, upper_left + 2 * self._width + 3)))    

        bomb_spots = random.sample(valid_spots, self._num_bombs)
        return bomb_spots 

    """
    Constructor for a grid object. Initializes all tiles in grid, and places bombs 
    randomly. 
    @param width the width of the grid
    @param height the height of the grid 
    @param num_bombs the number of bombs to place in the grid 
    """
    def __init__ (self, width, height, num_bombs):  
        
        # Validate arguments
        try:
            if num_bombs < 0 or num_bombs > width * height: 
                raise ValueError("Invalid arguments to create a grid.")
        except TypeError:
            raise ValueError("Invalid arguments to create a grid.")
        
        # Grid of tiles, tile locations in grid for bombs, and metrics for iteration through grid 
        self._grid_array = []
        self._width = width
        self._height = height 
        self._revealed_tiles = 0
        self._num_bombs = num_bombs 
        self._uncovered_bomb = False
        self._selected = {"x": 0, "y": 0}
        self.flags_placed = 0
       
        # Iterate over grid, placing bombs and notifying tiles next to each bomb 
        for y in range(0, self._height):
            self._grid_array.append([])
            for x in range(0, self._width):
                self._grid_array[y].append(tile.Tile())

    """
    Spawns bombs with selected tile as a "safe selection"
    """
    def begin(self):
        bomb_spots = self._generate_bomb_locations()
        for bomb_spot in bomb_spots:
            x = int(bomb_spot / self._height)
            y = int(bomb_spot % self._height)
            self._get_tile(x, y).convert_to_bomb()
            self._notify_adj_tiles(x, y)

    """
    Reveals all tiles in the grid (called when game ends).
    """
    def reveal_all(self):
        for y in range(0, self._height):
            for x in range(0, self._width):
                self._grid_array[y][x].reveal()

    """
    Reveals a tile in the grid. 
    @return true if a bomb was uncovered, false if not 
    """
    def reveal_tile(self, x = None, y = None):
        
        # Default to selected tile 
        if ( x == None and y == None):
            uncovered_tile = self._get_selected_tile()
            x = self._selected["x"]
            y = self._selected["y"]
        else: 
            uncovered_tile = self._get_tile(x, y)

        # Spawns bombs with selected tile as "safe selection"
        if (self._revealed_tiles == 0):
            self.begin()
        
        # Do not reveal a tile that is already revealed 
        if ( uncovered_tile.revealed ):
            return False 

        # Reveal selected tile, recording if the tile is a bomb, and incremend revealed tiles 
        is_bomb = uncovered_tile.reveal()
        self._revealed_tiles += 1 

        # Chain reveal if unveiled tile has no value 
        if not is_bomb and uncovered_tile.adj_bombs == 0:
            for rows in range(y-1, y+2):
                for cols in range(x-1, x+2):
                    if (cols != x or rows != y):
                        # If a tile is not valid, ignore and continue 
                        try:
                            if not self._get_tile(cols, rows).revealed:
                                self.reveal_tile(cols, rows)
                        except IndexError:
                            continue 
        elif is_bomb:
            self._uncovered_bomb = True 

        return is_bomb

    """
    Returns "unplaced" flags
    """
    def unflagged_bombs(self):
        return self._num_bombs - self.flags_placed

    """
    Flags/unflags selected tile in the grid, incrementing flags placed if the operation was a "flag" 
    operation and decrementing it if it was an "unflag" operation
    @param status true if flag, false if unflag
    """
    def flag_tile(self):
        if self._get_selected_tile().set_flag():
            self.flags_placed += 1
        else: 
            self.flags_placed -= 1

    def up(self):
        if ( self._selected["y"] > 0 ):
            self._selected["y"] -= 1

    def down(self):
        if ( self._selected["y"] < self._height - 1 ):
            self._selected["y"] += 1

    def left(self):
        if ( self._selected["x"] > 0 ):
            self._selected["x"] -= 1

    def right(self):
        if ( self._selected["x"] < self._width - 1 ):
            self._selected["x"] += 1

    """
    Returns this grid object as a string. 
    @return string the string representation of this grid object 
    """
    def to_s(self):
        s = ""
        for y in range(0, len(self._grid_array)):
            for x in range(0, len(self._grid_array[y])):
                grid_contents = self._grid_array[y][x].to_s()
                if ( x == self._selected["x"] and y == self._selected["y"]):
                    s += RED + grid_contents + NORMAL + " " 
                else: 
                    s += COLOR_MAP.get(grid_contents, YELLOW) + grid_contents + NORMAL + " "
            s += "\n"
        return s 

    """
    Wrapper around access to grid, more strict throwing of index errors.
    @raises IndexError if provided indices are invalid  
    @return found_tile the tile at provided coordinates 
    """
    def _get_selected_tile(self):
        x = self._selected["x"]
        y = self._selected["y"]
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            raise IndexError("Indices provided are out of range")
        return self._grid_array[y][x]

    """
    Wrapper around access to grid, more strict throwing of index errors.
    @param x the x coordinate of the tile to access
    @param y the y coordinate of the tile to access
    @raises IndexError if provided indices are invalid  
    @return found_tile the tile at provided coordinates 
    """
    def _get_tile(self, x, y):
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            raise IndexError("Indices provided are out of range")
        return self._grid_array[y][x]

    """
    Returns the state of the game at any given moment.
    @returns 1 if game is won, -1 if game is lost (a bomb is revealed), 0 if game is in progress.
    """
    def game_state(self):
        if self._uncovered_bomb:
            return -1
        elif self._revealed_tiles == self._width * self._height - self._num_bombs:
            return 1
        else:
            return 0