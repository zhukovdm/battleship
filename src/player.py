import random

from grid import Grid

class Player:
    
    """
        A player could be controlled either by a computer or a real player.
        From the beginning of the game each of two players gets standard
        collection of ships: 4x ■, 3x ■■, 2x ■■■, 1x ■■■■ and 1x ■■■■■.
    """

    ai_type = "ai"
    hi_type = "hi"
    ship_views = ["", "■", "■■", "■■■", "■■■■", "■■■■■"]

    def __init__(self):
        self.name             = ""
        self.type             = ""
        self.ships_count      = [0, 4, 3, 2, 1, 1]
        self.unknown_cells    = [(i, j) for i in range(1, Grid.rows + 1) for j in range(1, Grid.cols + 1)]
        self.ship_cells_found = []
        self.cells_to_check   = []
        self.grid             = Grid()
        self.opponent_grid    = Grid()
    
    def has_ships(self) -> bool:
        return sum(self.ships_count) == 0

    def is_ai(self) -> bool:
        return self.type == Player.ai_type

    def has_ship_cells_found(self) -> bool:
        return len(self.ship_cells_found) > 0

    def has_cells_to_check(self) -> bool:
        return len(self.to_check) > 0

    def check_cell(self, index) -> (int, int):
        cell = self.to_check.pop(index)
        self.unknown_cells.remove(self.unknown_cells.index(cell))
        return cell

    def borrow_longest_ship(self) -> int:
        for length in range(len(self.ships_count) - 1, 0, -1):
            if self.ships_count[length] > 0:
                self.ships_count[length] -= 1
                return length

    def release_longest_ship(self, length):
        self.ships_count[length] += 1

    def try_fit_ship(self, length, row, col, row_dir, col_dir) -> list():
        
        '''
            Given starting position and direction, try to add ship surrounded
            by the water. Ships cannot occupy adjacent positions in any
            direction. This method returns list of modified cells if success,
            otherwise empty list.
        '''

        # calculate possible positions the ship will occupy
        ship = []
        for l in range(length):
            ship.append((row + row_dir * l, col + col_dir * l))

        # verify that all positions will be within bounds
        for r, c in ship:
            if not Grid.within_bounds(r, c):
                return []

        # verify that all positions will occupy unknown cells
        for r, c in ship:
            cell = self.grid.get_cell(r, c)
            if not Grid.is_unknown(cell):
                return []

        # add ship, certainly possible
        for r, c in ship:
            self.grid.set_ship_cell(r, c)

        # try to add water around each ship cell
        water = []
        for r, c in ship:
            for r_dir in range(-1, 2):
                for c_dir in range(-1, 2):
                    new_r = r + r_dir
                    new_c = c + c_dir
                    if Grid.within_bounds(new_r, new_c):
                        cell  = self.grid.get_cell(new_r, new_c)
                        if self.grid.is_unknown(cell):
                            water.append((new_r, new_c))
                            self.grid.set_water_cell(new_r, new_c)

        # return all changes made into the grid
        return ship + water

    def unroll(self, occupied):
        
        '''Remove all changes made into the grid.'''

        for row, col in occupied:
            self.grid.set_unknown_cell(row, col)

    def gen_ships(self) -> bool:
        
        '''
            Ship generation. Find the longest ship to be placed on the board.
            Randomly select a starting point from all available cells. Try to
            fit new ship. Fit remaining ships recursively.
        '''

        if sum(self.ships_count) > 0:

            success  = False
            length   = self.borrow_longest_ship()

            # make own randomly ordered copy of cells to try
            cells_to_try = self.grid.collect_unknown_cells()
            random.shuffle(cells_to_try)

            # for each such cell
            for row, col in cells_to_try:
                
                # prepare possible directions
                dirs_to_try = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(dirs_to_try)

                # for a given length, point and direction, try fit a ship
                for row_dir, col_dir in dirs_to_try:
                    occupied = self.try_fit_ship(length, row, col, row_dir, col_dir)

                    # ship fits, recursive call
                    if occupied: success = self.gen_ships()

                    # no success in tried direction, unroll changes
                    if not success: self.unroll(occupied)
                
                # solution is found
                if success: break
            
            self.release_longest_ship(length)

            # either solution is found or no success
            return success

        # no more ships, recursion bottom
        else: return True

    def report_invalid_input(self):
        print(" invalid input, try again")
        
    def get_user_position(self, message) -> (int, int):
        while True:
            try:
                print()
                print("{}".format(message), end="")
                line = input().split()
                if len(line) != 2: self.report_invalid_input()
                else:
                    row = int(line[0])
                    col = int(line[1])
                    if not Grid.within_bounds(row, col): self.report_invalid_input()
                    else:
                        return (row, col)
            except:
                self.report_invalid_input()

    def get_user_interval(self) -> (int, int, int, int):
        row_fr, col_fr = self.get_user_position(" position from ")
        row_to, col_to = self.get_user_position(" position to   ")
        return (row_fr, col_fr, row_to, col_to) 

    def add_water_around(self, row, col):
        for dir_r in range(-1, 2):
            for dir_c in range(-1, 2):
                new_r = row + dir_r
                new_c = col + dir_c
                if self.grid.is_unknown(new_r, new_c):
                    self.grid.set_water(new_r, new_c)

    def positions_unknown(self, positions) -> bool:
        are_unknown = True
        for row, col in positions:
            are_unknown = are_unknown and self.grid.is_unknown(row, col)
        return are_unknown

    def add_ship_pieces(self, pieces):
        '''Add ship pieces and water around.'''
        for row, col in pieces: self.grid.set_ship(row, col)
        for row, col in pieces: self.add_water_around(row, col)

    def add_oriented_ship(self, dim, lower, higher, is_horizontal) -> bool:
        pos = []
        while lower <= higher:
            pos.append((dim, lower)) if is_horizontal else pos.append((lower, dim))
            lower += 1
        ship_set = self.positions_unknown(pos)
        if ship_set: self.add_ship_pieces(pos)
        return ship_set

    def map_values(self, a, b, c) -> (int, int, int):
        return (a, min(b, c), max(b, c))

    def add_ship(self, ships_count) -> list():

        ship_set = False
        length   = 0

        while not ship_set:
            row_fr, col_fr, row_to, col_to = self.get_user_interval()

            dim = lower = higher = 0 # declare vars
            is_h = False

            if row_fr == row_to:
                dim, lower, higher = self.map_values(row_fr, col_fr, col_to)
                is_h = True
            if col_fr == col_to:
                dim, lower, higher = self.map_values(col_fr, row_fr, row_to)
                is_h = False
            length = higher - lower + 1

            if length >= 1 and length <= 5 and ships_count[length] > 0:
                ships_count[length] -= 1
                ship_set = self.add_oriented_ship(dim, lower, higher, is_h)
                if not ship_set: ships_count[length] += 1
            
            if not ship_set: self.report_invalid_input()
            
        return ships_count

    def find_ship_segments(self, row, col) -> list():
        segments = []
        segments.append((row, col))
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for row_dir, col_dir in dirs:
            mul = 1
            while True:
                row_new = row + row_dir * mul
                col_new = col + col_dir * mul
                if not self.grid.is_ship(row_new, col_new): break
                segments.append((row_new, col_new))
                mul += 1

        return segments

    def remove_water_cell(self, row, col):
        is_ship_adjacent = False
        for row_dir in range(-1, 2):
            for col_dir in range(-1, 2):
                row_new = row + row_dir
                col_new = col + col_dir
                is_ship_adjacent = is_ship_adjacent or self.grid.is_ship(row_new, col_new)
        if not is_ship_adjacent: self.grid.set_unknown(row, col)

    def remove_ship_segments(self, segments):
        
        # first set segments to unknown cells
        for row, col in segments:
            self.grid.set_unknown(row, col)

        # for each such segment try to remove water around
        for row, col in segments:
            for row_dir in range(-1, 2):
                for col_dir in range(-1, 2):
                    row_new = row + row_dir
                    col_new = col + col_dir
                    if self.grid.is_water(row_new, col_new):
                        self.remove_water_cell(row_new, col_new)

    def remove_ship(self, ships_count) -> list():
        '''
            The user select a ship piece on the current board and removes
            the entire ship.
        '''
        ship_set = False

        while not ship_set:
            row, col = self.get_user_position(" ship segment ")
            ship_set = self.grid.is_ship(row, col)
        
        # find all segments
        ship_segments = self.find_ship_segments(row, col)
        ships_count[len(ship_segments)] += 1
        self.remove_ship_segments(ship_segments)

        return ships_count

    def set_ships(self):
        '''The user sets ships manually.'''

        ships_count = self.ships_count[:]

        while sum(ships_count) > 0:
            self.show_header(ships_count)
            self.grid.show()

            opt = ''
            valid_opts = [ "a", "r" ]
            while opt not in valid_opts:
                print()
                opt = input(" (a)dd or (r)emove ship? ")
                if opt not in valid_opts: self.report_invalid_input()
            
            if opt == "a": ships_count = self.add_ship(ships_count)
            else:
                if sum(ships_count) < sum(self.ships_count):
                    ships_count = self.remove_ship(ships_count)
                else: print(" no ships can be removed.")

    def get_user_strike(self) -> (int, int):

        '''Get valid point from the user, returns tuple.'''
        
        while True:
            try:
                row, col = map(int, input(" Enter row and column: ").split())

                if self.opponent_grid.within_bounds(row, col) and \
                    self.opponent_grid.is_unchecked(row, col):
                    return (row, col)
            
            except:
                print(" Entered coordinates are invalid, try again.")

    def show_header(self, ships_count):
        print()
        print(" ", end="")
        self.show_ships(ships_count)
        print()
        print()

    def show_ships(self, ships_count):
        result = []
        for i in range(1, len(ships_count)):
            result.append("{}x {}".format(ships_count[i], Player.ships_views[i]))
        print(", ".join(result), end="")
