import random
from agent import Agent

class Game:

    """
        Game control
    """

# Init object

    def __init__(self):
        self.order = []
        self.agent1 = Agent("")
        self.agent2 = Agent("")
        self.last_agent_name = ""
        self.last_turns = []

# Init game

    def gen_ships_hi(self,agent):
        '''
            Dialog for human player to generate ships
            either in auto or manual mode
        '''
        confirmed = ""
        while confirmed != "1":
            gen_sign = ""
            while gen_sign not in ["0","1"]:
                gen_sign = input("   Auto (0) or manual (1) ship generation? ")
                print()
                if gen_sign == "0":
                    agent.ships_automatically()
                    confirmed = input("   Enter (1) if you agree. Else, enter any other key. ")
                    print()
                elif gen_sign == "1":
                    agent.ships_manually()
                    confirmed = "1"

    def gen_ships_ai(self,agent,n):
        '''
            Ships auto generation for pc player
            always in auto mode
        '''
        agent.kind = "ai"
        agent.name = "PC" + n
        agent.ships_automatically()
        input("   {} has been set. Press Enter to continue.".format(agent.name))
        print()

    def gen_hi(self,agent,n):
        '''
            Dialog for setting up human player
        '''
        agent.kind = "hi"
        agent.name = input("   Enter name of the player{}: ".format(n))
        self.gen_ships_hi(agent)
        input("   {} has been set. Press Enter to continue.".format(agent.name))
        print()

    def init_game(self):
        '''
            Function handling initial game setup such as
            mode, creating agent instances and grid generation
        '''
        print()
        print("    ____        _   _   _           _     _       ")
        print("   | __ )  __ _| |_| |_| | ___  ___| |__ (_)_ __  ")
        print("   |  _ \\ / _` | __| __| |/ _ \\/ __| '_ \\| | '_ \\ ")
        print("   | |_) | (_| | |_| |_| |  __/\\__ \\ | | | | |_) |")
        print("   |____/ \\__,_|\\__|\\__|_|\\___||___/_| |_|_| .__/ ")
        print("                                           |_|  ")
        print()
        print("            0: Player   vs. Player")
        print("            1: Player   vs. Computer")
        print("            2: Computer vs. Computer")
        print()

        option = ""
        while option not in ["0","1","2"]:
            option = input("   Select game option: ")
            print()
        
        if option == "0":
            self.gen_hi(self.agent1," 1")
            for i in range(30):
                print()
            self.gen_hi(self.agent2," 2")
            for i in range(30):
                print()
            self.order.append(self.agent1)
            self.order.append(self.agent2)

        elif option == "1":
            self.gen_hi(self.agent1,"")
            self.gen_ships_ai(self.agent2,"")
            order = ""
            while order not in ["1","2"]:
                order = input("   Do you want to start first (1) or second (2)? ")
                print()
                if order == "1":
                    self.order.append(self.agent1)
                    self.order.append(self.agent2)
                elif order == "2":
                    self.order.append(self.agent2)
                    self.order.append(self.agent1)

        elif option == "2":
            self.gen_ships_ai(self.agent1," 1")
            self.gen_ships_ai(self.agent2," 2")
            self.order.append(self.agent1)
            self.order.append(self.agent2)
        
        print("   The game has been started!")
        print()

# Play game

    def uncover_grid(self, grid, ref_grid):
        '''
            Both grids are uncovered after winner is defined.
        '''
        for i in range(1,len(grid)):
            for j in range(1,len(grid[0])):
                if grid[i][j] == "∙":
                    grid[i][j] = ref_grid[i][j]

    def print_board(self):
        '''
            Function handling visual representation of the grid.
            New grid is drawn after each step.
        '''
        rows = len(self.order[0].grid_enemy)
        cols = len(self.order[0].grid_enemy[0])
        print("   ┌──────────────────────────────────────────────────┬──────────────────────────────────────────────────┐")
        print("   │ {:48}".format(self.order[0].name),end="")
        print(" │ {:48} │".format(self.order[1].name),end="")
        print()
        print("   │ Rem. {:2} : ".format(self.order[0].ships_m), end="")
        for i in range(1,len(self.order[0].ships_c)-1):
            print("{}x {}, ".format(self.order[0].ships_c[i], self.order[0].ships_s[i]), end="")
        print("{}x {}".format(self.order[0].ships_c[len(self.order[0].ships_c)-1], self.order[0].ships_s[len(self.order[0].ships_c)-1]), end="")
        print(" │ Rem. {:2} : ".format(self.order[1].ships_m), end="")
        for i in range(1,len(self.order[1].ships_c)-1):
            print("{}x {}, ".format(self.order[1].ships_c[i], self.order[1].ships_s[i]), end="")
        print("{}x {} │".format(self.order[1].ships_c[len(self.order[1].ships_c)-1], self.order[1].ships_s[len(self.order[1].ships_c)-1]), end="")
        print()
        print("   ├──────────────────────────────────────────────────┼──────────────────────────────────────────────────┤")
        for i in range(rows):
            print("   │         ",end="")
            for j in range(cols):
                print("{:3}".format(str(self.order[0].grid_enemy[i][j])), end="",flush=True)
            print("        │         ", end="", flush=True)
            for j in range(cols):
                print("{:3}".format(str(self.order[1].grid_enemy[i][j])), end="", flush=True)
            print("        │")
        print("   ├──────────────────────────────────────────────────┴──────────────────────────────────────────────────┤")
        print("   │ {:15}".format(self.last_agent_name),end="")
        turns = ", ".join(map(str, self.last_turns))
        print("{:85}│".format(turns))
        print("   └─────────────────────────────────────────────────────────────────────────────────────────────────────┘")

    def evaluate_point_ai(self,rC,cC,agent,enemy):
        '''
            Evaluate each point chosen specifically by pc player.
        '''
        sign = enemy.grid_agent[rC][cC]
        agent.grid_enemy[rC][cC] = sign
        if sign == "■":
            agent.to_check = []                                 # no longer relevant
            agent.ships_f.append((rC,cC))
            agent.ships_f.sort()
            enemy_cells_ship = enemy.find_cells_ship(rC,cC)
            enemy_cells_ship.sort()
            if agent.ships_f == enemy_cells_ship:               # ship is found
                enemy.ships_c[len(agent.ships_f)] -= 1
                enemy.ships_m -= 1
                agent.insert_enemy_ship(agent.ships_f)
                agent.ships_f = []
            return True
        return False

    def evaluate_point_hi(self,rC,cC,agent,enemy):
        '''
            Evaluate each point chosen specifically by human player.
        '''
        sign = enemy.grid_agent[rC][cC]
        agent.grid_enemy[rC][cC] = sign
        if sign == "■":
            agent.set_hi.add((rC,cC))
            enemy_cells_ship = set(enemy.find_cells_ship(rC,cC))
            if agent.ship_in_set_hi(enemy_cells_ship, agent.set_hi):
                enemy.ships_c[len(enemy_cells_ship)] -= 1
                enemy.ships_m -= 1
                agent.insert_enemy_ship(enemy_cells_ship)
                agent.remove_ship_from_set_hi(enemy_cells_ship, agent.set_hi)
            return True
        return False
        
        cells_ship = enemy.find_cells_ship(rC,cC)

    def strike(self, index):
        '''
            Function controls each turn until someone hit empty cell
            or the winner is determined. Turns are repeat.
        '''
        agent = self.order[index]
        enemy = self.order[(index+1)%2]
        self.last_turns = []
        self.last_agent_name = agent.name
        if agent.kind == "ai":                                  # ai
            ok = True
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
        elif agent.kind == "hi":                                # hi
            ok = True
            while ok and enemy.ships_m > 0:
                rC,cC = agent.enter_point_manually()
                ok = self.evaluate_point_hi(rC,cC,agent,enemy)
                self.last_turns.append((rC,cC))
                if ok:
                    self.print_board()

    def play_game(self):
        '''
            Game handler, determine who makes the turn.
        '''
        index = 0
        while self.agent1.ships_m != 0 and self.agent2.ships_m != 0:
            index %= 2
            self.print_board()
            self.strike(index)
            index += 1
        self.uncover_grid(self.order[0].grid_enemy, self.order[1].grid_agent)
        self.uncover_grid(self.order[1].grid_enemy, self.order[0].grid_agent)
        self.print_board()
        if   self.agent1.ships_m == 0: print("   {} wins. Game over!".format(self.agent2.name))
        elif self.agent2.ships_m == 0: print("   {} wins. Game over!".format(self.agent1.name))
        print()
