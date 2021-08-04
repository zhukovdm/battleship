class Grid:
    
    '''
        Grid is a 10x10 table. The representation is explicit, the content
        of the grid is also used for showing the grid.
    '''

    rows          = 10
    cols          = 10
    unknown_cell  = "·"
    water_cell    = "▢"
    ship_cell     = "■"

    def __init__(self):

        # __table shall be a private member as much as possible

        self.__table = [[Grid.unknown_cell for i in range(Grid.cols + 1)] for j in range(Grid.rows + 1)]
        self.__table[0][0] = "\\"
        for row in range(1, Grid.rows + 1): self.__table[row][0] = row
        for col in range(1, Grid.cols + 1): self.__table[0][col] = col

    @staticmethod
    def within_bounds(row, col) -> bool:
        return (1 <= row <= Grid.rows) and (1 <= col <= Grid.cols)

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

    def set_unknown(self, row, col):
        self.__table[row][col] = Grid.unknown_cell

    def set_water(self, row, col):
        self.__table[row][col] = Grid.water_cell

    def set_ship(self, row, col):
        self.__table[row][col] = Grid.ship_cell

    def collect_unknown_cells(self) -> list():
        cells = []
        for row in range(1, Grid.rows + 1):
            for col in range(1, Grid.cols + 1):
                if self.__table[row][col] == Grid.unknown_cell:
                    cells.append((row, col))
        return cells

    def finalize(self):
        '''
            Set all unknown cells to water. Grid shall be finalized after
            all ships are generated or set manually.
        '''

        for row in range(1, Grid.rows + 1):
            for col in range(1, Grid.cols + 1):
                if self.__table[row][col] == Grid.unknown_cell:
                    self.__table[row][col] = Grid.water_cell

    def show_row(self, row):

        '''Show certain row.'''

        for col in range(Grid.cols + 1):
            print("{:>3}".format(self.__table[row][col]), end="")

    def show(self):

        '''Show current grid.'''

        for row in range(Grid.rows + 1):
            self.show_row(row)
            print()
