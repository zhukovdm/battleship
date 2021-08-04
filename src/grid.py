from typing import List, Tuple


class Grid:
    """
        Grid is a 10x10 table. The representation is explicit, the content
        of the grid is also used for showing the grid.
    """

    rows = 10
    cols = 10
    unknown_cell = "·"
    water_cell = "▢"
    ship_cell = "■"

    def __init__(self):

        # __table shall be a private member as much as possible

        self.__table = [[Grid.unknown_cell for i in range(Grid.cols + 1)] for j in range(Grid.rows + 1)]
        self.__table[0][0] = "\\"
        for row in range(1, Grid.rows + 1):
            self.__table[row][0] = row
        for col in range(1, Grid.cols + 1):
            self.__table[0][col] = col

    @staticmethod
    def within_bounds(row, col) -> bool:
        return (0 < row < Grid.rows + 1) and (0 < col < Grid.cols + 1)

    def get_cell(self, row, col) -> str:
        return self.__table[row][col]

    def is_unknown(self, row, col) -> bool:
        return Grid.within_bounds(row, col) and \
            self.get_cell(row, col) == Grid.unknown_cell

    def is_water(self, row, col) -> bool:
        return Grid.within_bounds(row, col) and \
            self.get_cell(row, col) == Grid.water_cell

    def is_ship(self, row, col) -> bool:
        return Grid.within_bounds(row, col) and \
            self.get_cell(row, col) == Grid.ship_cell

    def set_unknown(self, row, col) -> None:
        self.__table[row][col] = Grid.unknown_cell

    def set_water(self, row, col) -> None:
        self.__table[row][col] = Grid.water_cell

    def set_ship(self, row, col) -> None:
        self.__table[row][col] = Grid.ship_cell

    def add_water_around(self, cells: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Replace unknown cells with water cell, return changes."""
        water = []

        for row, col in cells:
            for row_dir in range(-1, 2):
                for col_dir in range(-1, 2):
                    row_new = row + row_dir
                    col_new = col + col_dir
                    if self.is_unknown(row_new, col_new):
                        water.append((row_new, col_new))
                        self.set_water(row_new, col_new)

        return water

    def add_ship_segments(self, ship_segments: List[Tuple[int, int]]) -> None:
        """Add ship pieces and water around."""

        # add ship itself first
        for row, col in ship_segments:
            self.set_ship(row, col)

        # add water around all segments
        _ = self.add_water_around(ship_segments)

    def get_unknown_cells(self) -> List[Tuple[int, int]]:
        cells = []
        for row in range(1, Grid.rows + 1):
            for col in range(1, Grid.cols + 1):
                if self.__table[row][col] == Grid.unknown_cell:
                    cells.append((row, col))
        return cells

    def finalize(self) -> None:
        """
            Set all unknown cells to water. Grid shall be finalized after
            all ships are generated or set manually.
        """

        for row in range(1, Grid.rows + 1):
            for col in range(1, Grid.cols + 1):
                if self.__table[row][col] == Grid.unknown_cell:
                    self.__table[row][col] = Grid.water_cell

    def find_ship_segments(self, row, col) -> List[Tuple[int, int]]:
        """
            Given row and column, try to prolong ship in all directions.
            (row, col) is known to be a ship cell.
        """

        ship_segments = [(row, col)]
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for row_dir, col_dir in dirs:
            mul = 1
            while True:
                row_new = row + row_dir * mul
                col_new = col + col_dir * mul

                if not self.is_ship(row_new, col_new):
                    break

                ship_segments.append((row_new, col_new))
                mul += 1

        return ship_segments

    def show_row(self, row) -> None:
        """Show certain row."""

        for col in range(Grid.cols + 1):
            print("{:>3}".format(self.__table[row][col]), end="")

    def show(self) -> None:
        """Show current grid."""
        print()
        for row in range(Grid.rows + 1):
            self.show_row(row)
            print()
