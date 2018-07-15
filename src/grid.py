import tile
import random

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
    @param x the x coordinate of a 'safe tile' 
    @param y the y coordinate of a 'safe tile'
    @return bombs a list of valid locations for bombs to be placed in the grid 
    """ 
    def _generate_bomb_locations(self, x, y):
        # Locate and place bombs, excluding first tile from the potential bomb spots 
        valid_spots = set(range(0, self._width * self._height))
        if not x == None and not y == None:
            upper_left = y * self._width + x 
            valid_spots -= set(range(upper_left, upper_left + 3) + 
                               range(upper_left + self._width, upper_left + self._width + 3) + 
                               range(upper_left + 2 * self._width, upper_left + 2 * self._width + 3))    

        bomb_spots = random.sample(valid_spots, self._num_bombs)
        return bomb_spots 

    """
    Constructor for a grid object. Initializes all tiles in grid, and places bombs 
    randomly. 
    @param width the width of the grid
    @param height the height of the grid 
    @param num_bombs the number of bombs to place in the grid 
    @param first_x the x coordinate of the first tile to reveal, guaranteed to be vacant. If not 
                   provided, a full grid will be generated with no revealed tiles. 
    @param first_y the y coordinate of the first tile to reveal, guaranteed to be vacant. If not 
                   provided, a full grid will be generated with no revealed tiles.
    """
    def __init__ (self, width, height, num_bombs, first_x = None, first_y = None):  
        
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
       
        # Iterate over grid, placing bombs and notifying tiles next to each bomb 
        for y in range(0, self._height):
            self._grid_array.append([])
            for x in range(0, self._width):
                self._grid_array[y].append(tile.Tile())
            
        bomb_spots = self._generate_bomb_locations(first_x, first_y)
        for bomb_spot in bomb_spots:
            y = bomb_spot / height
            x = bomb_spot % height
            self._grid_array[y][x].convert_to_bomb()
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
    @param x the x coordinate of the tile to reveal 
    @param y the y coordinate of the tile to reveal 
    @return true if a bomb was uncovered, false if not 
    """
    def reveal_tile(self, x, y):
        uncovered_tile = self._get_tile(x, y)
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
    Flags/unflags a tile in the grid. 
    @param x the x coordinate of the tile to flag 
    @param y the y coordinate of the tile to flag 
    @param status true if flag, false if unflag
    """
    def flag_tile(self, x, y):
        self._get_tile(x, y).set_flag()

    """
    Returns this grid object as a string. 
    @return string the string representation of this grid object 
    """
    def to_s(self):
        s = ""
        for y in range(0, len(self._grid_array)):
            for x in range(0, len(self._grid_array[y])):
                s += self._grid_array[y][x].to_s() + " "
            s += "\n"
        return s 

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