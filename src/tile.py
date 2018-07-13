class Tile:

    def __init__(self):
        self._adj_bombs = 0
        self._revealed = False
        self._flagged = False 

    def is_bomb(self):
        if self._adj_bombs < 0:
            return True
        else:
            return False

    @property
    def adj_bombs(self):
        return self._adj_bombs

    @property 
    def flagged(self):
        return self._flagged

    def set_flag(self):
        self._flagged = not self._flagged 

    def add_adj_bomb(self):
        self._adj_bombs += 1

    def convert_to_bomb(self):
        self._adj_bombs -= 9

    @property
    def revealed(self):
        return self._revealed

    def reveal(self):
        self._revealed = True
        return self.is_bomb()

    def to_s(self):
        if self._flagged:
            return "!"
        elif self._revealed:
            if self._adj_bombs < 0:
                return "B"
            elif self._adj_bombs == 0:
                return "_"
            else: 
                return str(self._adj_bombs)
        else:
            return "*"