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
    views         = [unknown_cell, water_cell, ship_cell]

    def __init__(self):

        # table shall be a private member as much as possible

        self.__table = [[Grid.unknown_cell for i in range(Grid.cols + 1)] for j in range(Grid.rows + 1)]
        self.__table[0][0] = "\\"
        for col in range(1, Grid.cols + 1): self.__table[0][col] = col
        for row in range(1, Grid.rows + 1): self.__table[row][0] = row

    @staticmethod
    def within_bounds(row, col) -> bool:
        return (1 <= row <= Grid.rows) and (1 <= col <= Grid.cols)

    @staticmethod
    def is_unknown(cell) -> bool:
        return cell == Grid.unknown_cell

    @staticmethod
    def is_water(cell) -> bool:
        return cell == Grid.water_cell

    @staticmethod
    def is_ship(cell) -> bool:
        return cell == Grid.ship_cell

    def set_unknown_cell(self, row, col):
        self.__table[row][col] = Grid.unknown_cell

    def set_water_cell(self, row, col):
        self.__table[row][col] = Grid.discrete_cell

    def set_ship_cell(self, row, col):
        self.__table[row][col] = Grid.ship_cell

    def get_view(self, row, col) -> str:
        return self.__table[row][col]

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
