class Tile:

    def __init__(self):
        self._adj_bombs = 0
        self._revealed = False

    def is_bomb(self):
        if self._adj_bombs < 0:
            return True
        else:
            return False

    def get_num_adj_bombs(self):
        return self._adj_bombs

    def add_adj_bomb(self):
        self._adj_bombs += 1

    def convert_to_bomb(self):
        self._adj_bombs -= 9

    def is_revealed(self):
        return self._revealed

    def reveal(self):
        self.revealed = True

    def to_s(self):
        if self.revealed:
            if self._adj_bombs < 0:
                return "!"
            else: 
                return str(self._adj_bombs)
        else:
            return "*"