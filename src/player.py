import random
from typing import List, Tuple

from grid import Grid
from reporter import Reporter


class Player:
    """
        A player could be controlled either by a computer or a real player.
        From the beginning of the game each of two players gets standard
        collection of ships: 4x ■, 3x ■■, 2x ■■■, 1x ■■■■ and 1x ■■■■■.
    """

    ai_type = "ai"
    hi_type = "hi"
    ship_views = ["", "■", "■■", "■■■", "■■■■", "■■■■■"]

    @staticmethod
    def get_user_position(message) -> Tuple[int, int]:
        while True:
            try:
                print()
                print("{}".format(message), end="")
                line = input().split()
                if len(line) != 2:
                    Reporter.report_invalid_input()
                else:
                    row = int(line[0])
                    col = int(line[1])
                    if not Grid.within_bounds(row, col):
                        Reporter.report_invalid_input()
                    else:
                        return row, col
            except ValueError:
                Reporter.report_invalid_input()

    @staticmethod
    def get_user_interval() -> Tuple[int, int, int, int]:
        row_fr, col_fr = Player.get_user_position(" position from ")
        row_to, col_to = Player.get_user_position(" position to   ")
        return row_fr, col_fr, row_to, col_to

    @staticmethod
    def map_dim_lower_higher(a, b, c, d) -> Tuple[int, int, int, bool]:
        return a, min(b, c), max(b, c), d

    @staticmethod
    def show_ships_count(ships_count) -> None:
        result = []
        for i in range(1, len(ships_count)):
            result.append("{}x {}".format(ships_count[i], Player.ship_views[i]))
        print(", ".join(result), end="")

    def __init__(self):
        self.name = ""
        self.type = ""
        self.ships_count = [0, 4, 3, 2, 1, 1]
        self.ship_cells_found = []
        self.grid = Grid()
        self.opponent_grid = Grid()

    def is_ai(self) -> bool:
        return self.type == Player.ai_type

    def has_ships(self) -> bool:
        return sum(self.ships_count) > 0

    def has_ship_cells_found(self) -> bool:
        return len(self.ship_cells_found) > 0

    def borrow_longest_ship(self) -> int:
        for length in range(len(self.ships_count) - 1, 0, -1):
            if self.ships_count[length] > 0:
                self.ships_count[length] -= 1
                return length

    def release_longest_ship(self, length) -> None:
        self.ships_count[length] += 1

    def check_cells_unknown(self, cells: List[Tuple[int, int]]) -> bool:
        """Verify list of positions if all of them are unknown"""
        are_unknown = True

        for row, col in cells:
            are_unknown = are_unknown and self.grid.is_unknown(row, col)

        return are_unknown

    def try_fit_ship(self, length, row, col, row_dir, col_dir) -> List[Tuple[int, int]]:
        """
            Given starting position and direction, try to add ship surrounded
            by the water. Ships cannot occupy adjacent positions in any
            direction. This method returns list of modified cells if success,
            otherwise empty list.
        """

        # calculate possible positions the ship will occupy
        ship_segments = []
        for i in range(length):
            ship_segments.append((row + row_dir * i, col + col_dir * i))

        # verify that all positions will be within bounds
        for r, c in ship_segments:
            if not Grid.within_bounds(r, c):
                return []

        # verify that all positions will occupy unknown cells
        for r, c in ship_segments:
            if not self.grid.is_unknown(r, c):
                return []

        # add ship, certainly possible
        for r, c in ship_segments:
            self.grid.set_ship(r, c)

        # try to add water around each ship cell
        water_segments = self.grid.add_water_around(ship_segments)

        # return all changes made into the grid
        return ship_segments + water_segments

    def unroll_changes(self, occupied) -> None:
        """Remove all changes made into the grid."""

        for row, col in occupied:
            self.grid.set_unknown(row, col)

    def gen_ships(self) -> bool:
        """
            Ship generation. Find the longest ship to be placed on the board.
            Randomly select a starting point from all available cells. Try to
            fit new ship. Fit remaining ships recursively.
        """

        if sum(self.ships_count) > 0:

            success = False
            length = self.borrow_longest_ship()

            # make own randomly ordered copy of cells to try
            cells_to_try = self.grid.get_unknown_cells()
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
                    if occupied:
                        success = self.gen_ships()

                    # no success in tried direction, unroll changes
                    if not success:
                        self.unroll_changes(occupied)

                # solution is found
                if success:
                    break

            self.release_longest_ship(length)

            # either solution is found or no success
            return success

        # no more ships, recursion bottom
        else:
            return True

    def add_oriented_ship(self, dim: int, lower: int, higher: int, is_horizontal: bool) -> bool:
        """Add either horizontal or vertical ship."""

        # get positions of ship segments
        pos = []
        while lower <= higher:
            pos.append((dim, lower)) if is_horizontal else pos.append((lower, dim))
            lower += 1

        # all positions must be vacant (unknown)
        ship_set = self.check_cells_unknown(pos)

        if ship_set:
            self.grid.add_ship_segments(pos)

        return ship_set

    def add_ship(self, ships_count) -> List[int]:
        """Get termination segments from the user and add ship."""

        dim = lower = higher = 0
        ship_set = is_h = False

        while not ship_set:
            row_fr, col_fr, row_to, col_to = self.get_user_interval()

            if row_fr == row_to or col_fr == col_to:
                if row_fr == row_to:
                    dim, lower, higher, is_h = self.map_dim_lower_higher(row_fr, col_fr, col_to, True)
                if col_fr == col_to:
                    dim, lower, higher, is_h = self.map_dim_lower_higher(col_fr, row_fr, row_to, False)
                length = higher - lower + 1

                if 1 <= length <= 5 and ships_count[length] > 0:
                    ships_count[length] -= 1
                    ship_set = self.add_oriented_ship(dim, lower, higher, is_h)
                    if not ship_set:
                        ships_count[length] += 1

            if not ship_set:
                Reporter.report_invalid_input()

        return ships_count

    def remove_water_cell(self, row: int, col: int) -> None:
        """ Water cell can be removed if no adjacent ship exists. """

        is_ship_adjacent = False

        for row_dir in range(-1, 2):
            for col_dir in range(-1, 2):
                is_ship_adjacent = is_ship_adjacent or self.grid.is_ship(row + row_dir, col + col_dir)

        if not is_ship_adjacent:
            self.grid.set_unknown(row, col)

    def remove_ship_segments(self, ship_segments: List[Tuple[int, int]]) -> None:

        # first set segments to unknown cells
        for row, col in ship_segments:
            self.grid.set_unknown(row, col)

        # for each such segment try to remove water around
        for row, col in ship_segments:
            for row_dir in range(-1, 2):
                for col_dir in range(-1, 2):
                    if self.grid.is_water(row + row_dir, col + col_dir):
                        self.remove_water_cell(row + row_dir, col + col_dir)

    def remove_ship(self, ships_count: List[int]) -> List[int]:
        """ The user selects any segment of a ship on the current board
            and remove the entire ship. """

        row = col = 0
        ship_set = False

        while not ship_set:
            row, col = self.get_user_position(" ship segment ")
            ship_set = self.grid.is_ship(row, col)
            if not ship_set:
                Reporter.report_invalid_input()

        # find all segments
        ship_segments = self.grid.find_ship_segments(row, col)
        ships_count[len(ship_segments)] += 1
        self.remove_ship_segments(ship_segments)

        return ships_count

    def set_ships(self):
        """The user sets ships manually."""

        ships_count = self.ships_count[:]

        while sum(ships_count) > 0:
            self.show_ship_header(ships_count)
            self.grid.show()

            opt = ''
            valid_opts = ["a", "r"]
            while opt not in valid_opts:
                print()
                opt = input(" (a)dd or (r)emove ship? ")
                if opt not in valid_opts:
                    Reporter.report_invalid_input()

            if opt == "a":
                ships_count = self.add_ship(ships_count)
            else:
                if sum(ships_count) < sum(self.ships_count):
                    ships_count = self.remove_ship(ships_count)
                else:
                    print(" no ships can be removed.")

    def get_user_strike(self) -> Tuple[int, int]:
        """Get valid point from the user, returns tuple."""

        while True:
            try:
                row, col = map(int, input(" enter row and column ").split())
                if self.opponent_grid.is_unknown(row, col):
                    return row, col

            except ValueError:
                Reporter.report_invalid_input()

    def show_ship_header(self, ships_count) -> None:
        print()
        print(" ", end="")
        self.show_ships_count(ships_count)
        print()
        print()
