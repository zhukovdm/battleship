import random

from grid import Grid
from player import Player
from reporter import Reporter


class Game:
    """Game control, implements main game loop"""

    row_prefix = " │ "
    row_suffix = " │"
    max_player_name_len = 38

    @staticmethod
    def greet() -> None:
        print()
        print("  ____        _   _   _           _     _       ")
        print(" | __ )  __ _| |_| |_| | ___  ___| |__ (_)_ __  ")
        print(" |  _ \\ / _` | __| __| |/ _ \\/ __| '_ \\| | '_ \\ ")
        print(" | |_) | (_| | |_| |_| |  __/\\__ \\ | | | | |_) |")
        print(" |____/ \\__,_|\\__|\\__|_|\\___||___/_| |_|_| .__/ ")
        print("                                         |_|  ")
        print()
        print("           0: Player   vs. Player")
        print("           1: Player   vs. Computer")
        print("           2: Computer vs. Computer")

    @staticmethod
    def show_row_prefix() -> None:
        print(Game.row_prefix, end="")

    @staticmethod
    def show_row_suffix() -> None:
        print(Game.row_suffix)

    @staticmethod
    def show_row_middle() -> None:
        Game.show_row_prefix()

    @staticmethod
    def show_grid_prefix() -> None:
        print("  ", end="")

    @staticmethod
    def show_grid_suffix() -> None:
        print("   ", end="")

    @staticmethod
    def show_margin(left, middle, right) -> None:
        print(" {}────────────────────────────────────────{}────────────────────────────────────────{}".format(left, middle, right))

    @staticmethod
    def set_hi_player(p: Player(), n: int) -> None:
        """Dialog for setting up the real player."""
        p.type = "hi"

        # set name, length must be < than max_length
        p.name = " " * 100
        while len(p.name) > Game.max_player_name_len:
            player_order = "1st" if n == 0 else "2nd"
            p.name = input(" enter name of the {} player ".format(player_order))
            if len(p.name) > Game.max_player_name_len:
                Reporter.report_player_name_is_too_long(Game.max_player_name_len)

        # construct grid
        confirmed = "?"
        while confirmed != "a":
            print()
            user_input = "?"
            while user_input not in ["g", "s"]:
                user_input = input(" (g)enerate or (s)et ships manually? ")

                # generate ships until agreed
                if user_input == "g":
                    p.gen_ships()
                    p.grid.show()
                    print()
                    confirmed = input(" (a)gree or (d)isagree? ")

                # set ships manually
                elif user_input == "s":
                    p.set_ships()
                    confirmed = "a"

        Reporter.report_player_set(p.name)

    @staticmethod
    def set_ai_player(p: Player(), n: int) -> None:
        """Computer player always gets generated ships."""

        p.type = "ai"
        p.name = "PC" + (n + 1).__repr__()
        p.gen_ships()
        Reporter.report_player_set(p.name)

    def __init__(self):
        self.player = 0
        self.players = [Player(), Player()]
        self.turns = []
        Game.greet()

    def active_player(self) -> Player:
        return self.players[self.player]

    def opponent(self) -> Player:
        return self.players[1 - self.player]

    def show_active_player_name(self) -> None:
        print("{}".format(self.active_player().name), end="")

    def show_spanned_player_name(self, index: int) -> None:
        print("{:38}".format(self.players[index].name), end="")

    def show_player_ship_count(self, index: int) -> None:
        Player.show_ships_count(self.players[index].ships_count)

    def show_players(self) -> None:
        Game.show_row_prefix()
        self.show_spanned_player_name(0)
        Game.show_row_middle()
        self.show_spanned_player_name(1)
        Game.show_row_suffix()
        Game.show_row_prefix()
        self.show_player_ship_count(0)
        Game.show_row_middle()
        self.show_player_ship_count(1)
        Game.show_row_suffix()

    def show_grids(self):
        """ Present grids already uncovered by a player. """

        for row in range(Grid.rows + 1):
            Game.show_row_prefix()
            Game.show_grid_prefix()
            self.players[1].opponent_grid.show_row(row)
            Game.show_grid_suffix()
            Game.show_row_middle()
            Game.show_grid_prefix()
            self.players[0].opponent_grid.show_row(row)
            Game.show_grid_suffix()
            Game.show_row_suffix()

    def show_turns(self) -> None:
        """ Present turns made by an active player. """

        Game.show_row_prefix()
        self.show_active_player_name()

        length = len(Game.row_prefix) + len(self.active_player().name) + 1
        for t in range(len(self.turns)):

            # wrap
            if length + len(self.turns[t]) > 100:
                Game.show_row_prefix()
                length = 3 + len(self.turns[t].__repr__())
                print(self.turns[t], end="")
            
            # no wrap
            else:
                length += 1 + len(self.turns[t].__repr__())
                print(" {}".format(self.turns[t]))
        
        self.show_row_suffix()

    def show(self) -> None:
        Game.show_margin("┌", "┬", "┐")
        self.show_players()
        Game.show_margin("├", "┼", "┤")
        self.show_grids()
        Game.show_margin("├", "┴", "┤")
        self.show_turns()
        Game.show_margin("└", "─", "┘")
        
    def user_vs_user(self) -> None:
        for i in range(2):
            self.set_hi_player(self.players[i], i)

    def user_vs_computer(self) -> None:
        order = ""
        options = [ "1", "2" ]

        # get user input
        while order not in options:
            order = input(" start (1)st or (2)nd? ")
            if order not in options: Reporter.report_invalid_input()

        orders = [0, 1] if order == "1" else [1, 0]

        self.set_hi_player(self.players[orders[0]], orders[0])
        self.set_ai_player(self.players[orders[1]], orders[1])

    def computer_vs_computer(self) -> None:
        for i in range(2):
            self.set_ai_player(self.players[i], i)

    def set_players(self) -> None:
        """ Set up players based on the user option choice. """

        # get option from the user
        option = ""
        options = ["0", "1", "2"]
        while option not in options:
            print()
            option = input(" select option: ")
            if option not in options: Reporter.report_invalid_input()

        # initialize game accordingly
        if   option == "0": self.user_vs_user()
        elif option == "1": self.user_vs_computer()
        elif option == "2": self.computer_vs_computer()
        
        Reporter.report_game_started()

    def process_strike(self, row, col) -> None:
        """ Strike could drown the ship if all segments are found, uncover the
            next segment or miss opportunity. """

        is_ship_segment = self.opponent().grid.is_ship(row, col)

        if is_ship_segment:
            self.turns.append((row, col))
            self.active_player().ship_cells_found.append((row, col))
            self.active_player().opponent_grid.set_ship(row, col)
            candidate_ship = self.active_player().opponent_grid.find_ship_segments(row, col)
            candidate_ship.sort()
            opponents_ship = self.opponent().grid.find_ship_segments(row, col)
            opponents_ship.sort()
            
            # the ship is drown
            if candidate_ship == opponents_ship:
                self.active_player().ship_cells_found = []
                self.opponent().ships_count[len(candidate_ship)] -= 1
                self.active_player().opponent_grid.add_ship_segments(candidate_ship)

        else:
            self.active_player().opponent_grid.set_water(row, col)

    def strike_ai(self) -> bool:
        """ Computer strike. """
        row = col = -1

        length = len(self.active_player().ship_cells_found)

        # no tips, look for a ship
        if length == 0:
            unknown_cells = self.active_player().opponent_grid.get_unknown_cells()
            random.shuffle(unknown_cells)
            row, col = unknown_cells[0]

        # oriented ship, try to prolong in two directions
        elif length > 1:
            self.active_player().ship_cells_found.sort()
            row_lower, col_lower = self.active_player().ship_cells_found[0]
            row_upper, col_upper = self.active_player().ship_cells_found[length - 1]
            row_dir = 0 if row_upper == row_lower else 1
            col_dir = 0 if col_upper == col_lower else 1

            candidates = [(row_lower - row_dir, col_lower - col_dir),
                          (row_upper + row_dir, col_upper + col_dir)]
            random.shuffle(candidates)

            for row, col in candidates:
                if self.active_player().opponent_grid.is_unknown(row, col):
                    break

        # 1-segment ship, 4 directions are possible
        else:
            row_old, col_old = self.active_player().ship_cells_found[0]
            dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(dirs)

            # find unknown cell in any direction
            for row_dir, col_dir in dirs:
                row = row_old + row_dir
                col = col_old + col_dir
                if self.active_player().grid.is_unknown(row, col):
                    break

        self.process_strike(row, col)

        return self.opponent().grid.is_ship(row, col)

    def strike_hi(self) -> bool:
        """ User strike. """

        row, col = self.active_player().get_user_strike()
        self.process_strike(row, col)
        return self.opponent().grid.is_ship(row, col)

    def strike(self) -> bool:
        """ This method calls either ai_strike or hi_strike based on an active
            player type. Such weird implementation is chosen because Python does
            not support abstract classes without additional dependencies. """

        return self.strike_ai() if self.active_player().is_ai() else self.strike_hi()
            

    def play(self):
        """ Main game loop alternates player turns. """

        self.show()

        # determine the winner
        while self.active_player().has_ships() and self.opponent().has_ships():
            hit = self.strike()
            if not hit:
                self.player = 1 - self.player
                self.turns = []
            self.show()

        # uncover ships
        self.active_player().opponent_grid = self.opponent().grid
        self.opponent().opponent_grid = self.active_player().grid
        self.show()

        # report winner
        winner_name = self.active_player().name if self.active_player().has_ships() \
            else self.opponent().name

        Reporter.report_winner(winner_name)
