import tile
import random

class Grid ():

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
    Constructor for a grid object. Initializes all tiles in grid, and places bombs 
    randomly. 
    @param width the width of the grid
    @param height the height of the grid 
    @param num_bombs the number of bombs to place in the grid 
    """
    def __init__ (self, width, height, num_bombs):  
        
        # Validate arguments
        try:
            if (num_bombs < 0 or num_bombs > width * height): 
                raise ValueError("Invalid arguments to create a grid.")
        except TypeError:
            raise ValueError("Invalid arguments to create a grid.")
        
        # Grid of tiles, tile locations in grid for bombs, and metrics for iteration through grid 
        self._grid_array = []
        self._width = width
        self._height = height 
       
        # Iterate over grid, placing bombs and notifying tiles next to each bomb 
        for y in range(0, self._height):
            self._grid_array.append([])
            for x in range(0, self._width):
                self._grid_array[y].append(tile.Tile())
            
        # Locate and place bombs 
        bomb_spots = sorted(random.sample(range(0, self._width*self._height), num_bombs))
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