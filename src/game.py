import random

from grid import Grid
from player import Player

class Game:

    row_prefix = " │ "
    row_suffix = " │"
    max_player_name_len = 38

    def greet(self):
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

    def __init__(self):
        self.player  = 0
        self.players = [ Player(), Player() ]
        self.turns   = []
        self.hit     = False
        self.greet()

    def show_row_prefix(self):
        print(Game.row_prefix, end="")

    def show_row_middle(self):
        self.show_row_prefix()

    def show_row_suffix(self):
        print(Game.row_suffix)

    def show_grid_prefix(self):
        print("  ", end="")    

    def show_grid_suffix(self):
        print("   ", end="")

    def show_margin(self, left, middle, right):
        print(" {}────────────────────────────────────────{}────────────────────────────────────────{}".format(left, middle, right))

    def show_active_player_name(self):
        print("{}".format(self.active_player.name), end="")

    def show_spanned_player_name(self, index):
        print("{:38}".format(self.players[index].name), end="")

    def show_player_ships(self, index):
        result = []
        for i in range(1, len(self.players[index].ships_count)):
            result.append("{}x {}".format(self.players[index].ships_count[i], \
                                          self.players[index].ships_views[i]))
        print(", ".join(result), end="")

    def show_players(self):
        self.show_row_prefix()
        self.show_spanned_player_name(0)
        self.show_row_middle()
        self.show_spanned_player_name(1)
        self.show_row_suffix()
        self.show_row_prefix()
        self.show_player_ships(0)
        self.show_row_middle()
        self.show_player_ships(1)
        self.show_row_suffix()

    def show_grids(self):
        for row in range(Grid.rows + 1):
            self.show_row_prefix()
            self.show_grid_prefix()
            self.players[1].opponent_grid.show_row(row)
            self.show_grid_suffix()
            self.show_row_middle()
            self.show_grid_prefix()
            self.players[0].opponent_grid.show_row(row)
            self.show_grid_suffix()
            self.show_row_suffix()

    def show_turns(self):
        pass
        self.show_row_prefix()
        self.show_active_player_name()

        length = 3 + len(self.active_player.name) + 1
        for t in range(len(self.turns)):

            # wrap
            if (length + len(turns[t]) > 100):
                self.show_row_prefix()
                length = 3 + len(turns[t]).__repr__()
                print(turns[t], end="")
            
            # no wrap
            else:
                length += 1 + len(turns[t].__repr__())
                print(" {}".format(turns[t]))
        
        self.show_row_suffix()

    def show(self):
        self.show_margin("┌", "┬", "┐")
        self.show_players()
        self.show_margin("├", "┼", "┤")
        self.show_grids()
        self.show_margin("├", "┴", "┤")
        self.show_turns()
        self.show_margin("└", "─", "┘")

    def report_grid_is_set(self, p):
        input(" {} has been set, press Enter to continue.".format(p.name))

    def set_hi_player(self, p, n):

        '''Dialog for setting up the user player.'''

        p.type = "hi"
        
        # set name, length must be < than max_length
        p.name = " " * 100
        while len(p.name) > Game.max_player_name_len:
            player_order = "1st" if n == 0 else "2nd"
            p.name = input(" Enter name of the {} player: ".format(player_order))
            if len(p.name) > Game.max_player_name_len:
                print(" Entered name is too long, only {} chars are allowed.".format(Game.max_player_name_len))

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
                    confirmed = input(" (a)gree or (d)isagree? ")
                
                # set ships manually
                elif user_input == "s":
                    p.set_ships()
                    confirmed = "a"

        self.report_grid_set(p)

    def set_ai_player(self, p, n):

        '''Computer player always gets generated ships.'''

        p.type = "ai"
        p.name = "PC" + (n + 1).__repr__()
        p.gen_ships()
        
    def user_vs_user(self):
        for i in range(2): self.set_hi_player(self.players[i], i)

    def user_vs_computer(self):
        order = ""

        while order not in [ "1", "2" ]:
            order = input(" Start (1)st or (2)nd? ")
            orders = [0, 1] if order == "1" else [1, 0]

        self.set_hi_player(self.players[orders[0]], orders[0])
        self.set_ai_player(self.players[orders[1]], orders[1])

    def computer_vs_computer(self):
        for i in range(2): self.set_ai_player(self.players[i], i)

    def set_players(self):
        print()

        # get option from the user
        option = ""
        while option not in ["0", "1", "2"]:
            option = input(" Select option: ")
            print()
        
        if   option == "0": self.user_vs_user()
        elif option == "1": self.user_vs_computer()
        elif option == "2": self.computer_vs_computer()
        
        print(" The game has been started!")
        print()

    def active_player(self) -> Player():
        return self.players[self.player]

    def opponent(self) -> Player():
        return self.players[1 - self.player]

    # TODO
    def try_ai_strike(self, row, col) -> bool:
        
        '''
            Evaluate strike made by a computer player. Returns True if
            opponent's ship is hit, otherwise returns False.
        '''

        cell = opponent.grid.get_view(row, col)
        active_player().opponent_grid.set_ship_cell(row, col)

        if Grid.is_ship(cell):
            self.active_player.ship_cells_found.append((row, col))
            self.active_player.ship_cells_found.sort()


            return True
        
        return False

    def eval_hi_strike(self,rC,cC,agent,enemy):

        '''Evaluate strike made by a user.'''
        
        pass

    def strike(self):

        if self.active_player.is_ai():

            if not self.active_player.has_ship_cells_found:
                

            # has good cell candidates to verify
            if self.active_player.has_cells_to_check():
                index = random.randrange(len(active_player.to_check))
                row, col  = self.active_player.checkout_cell(index)
                if self.opponent.grid.is_ship_cell(row, col):


            # try any random unknown cell
            else:





            while ok and enemy.ships_m > 0:
                free_cells = agent.find_enemy_free_cells()      # recalculate free cells
                if len(agent.ships_f) == 0:                     # select random "∙" point
                    rC,cC = random.choice(free_cells)
                    ok = self.evaluate_point_ai(rC,cC,agent,enemy)
                    self.last_turns.append((rC,cC))
                elif len(agent.ships_f) == 1:                   # only one "■" found
                    rS,cS = agent.ships_f[0]
                    if agent.to_check == []:                    # find candidates, random order
                        direct = [(0,1),(1,0),(0,-1),(-1,0)]
                        random.shuffle(direct)
                        for i in direct:
                            if (rS+i[0],cS+i[1]) in free_cells:
                                agent.to_check.append((rS+i[0],cS+i[1]))
                    rC,cC = agent.to_check.pop()                # take last candidate
                    ok = self.evaluate_point_ai(rC,cC,agent,enemy)
                    self.last_turns.append((rC,cC))
                elif len(agent.ships_f) > 1:                    # more than one "■" found
                    if agent.to_check == []:                    # maximum 2 candidates
                        r1 = agent.ships_f[0][0] - (agent.ships_f[1][0] - agent.ships_f[0][0])
                        c1 = agent.ships_f[0][1] - (agent.ships_f[1][1] - agent.ships_f[0][1])
                        if (r1,c1) in free_cells: agent.to_check.append((r1,c1))
                        r2 = agent.ships_f[-1][0] - (agent.ships_f[-2][0] - agent.ships_f[-1][0])
                        c2 = agent.ships_f[-1][1] - (agent.ships_f[-2][1] - agent.ships_f[-1][1])
                        if (r2,c2) in free_cells: agent.to_check.append((r2,c2))
                        random.shuffle(agent.to_check)
                    rC,cC = agent.to_check.pop()
                    ok = self.evaluate_point_ai(rC,cC,agent,enemy)
                    self.last_turns.append((rC,cC))
        
        else:
            ok = True
            while ok and enemy.ships_m > 0:
                rC,cC = agent.enter_point_manually()
                ok = self.evaluate_point_hi(rC,cC,agent,enemy)
                self.last_turns.append((rC,cC))
                if ok:
                    self.print_board()

    def play(self):

        '''Main game loop alternates player turns.'''

        while self.player1.has_ships() and self.player2.has_ships():
            self.strike()
            if not self.hit:
                self.player = 1 - self.player
                self.turns  = []
            self.show()
        for player in self.players: player.opponent_grid.finalize()
        self.show()
        winner = self.player1.name if self.player1.has_ships() else self.player2.name
        print(" {} wins. Game over!".format(winner))        
        print()
