import tile
import random

class Grid ():

    def _notify_adj_tiles(self, x, y, width, height):
        possible_x = {
            'x' : True,
            'x-1' : (x-1 >= 0),
            'x+1' : (x+1 < width)
        }

        possible_y = {
            'y' : True,
            'y-1' : (y-1 >= 0),
            'y+1' : (y+1 < height)
        }

        for ky, vy in possible_y.items():
            for kx, vx in possible_x.items():
                if (kx != 'x' and ky != 'y') and vy and vx:
                    xval = eval(kx)
                    yval = eval(ky)
                    self._grid_array[yval][xval]._add_adj_bomb()

    def __init__ (self, width, height, num_bombs):
        self._grid_array = []
        bomb_spots = sorted(random.sample(range(1, width*height,), num_bombs))
        num_placed_bombs = 0
        tile_num = 0
        for y in range(0, height-1):
            self._grid_array[y] = []
            for x in range(0, width-1):
                self._grid_array[y][x] = tile.Tile()
                if num_placed_bombs < num_bombs and tile_num == bomb_spots[num_placed_bombs]:
                    self._grid_array[y][x].convert_to_bomb()
                    self._notify_adj_tiles(x, y, width, height)
                x += 1
                tile_num += 1