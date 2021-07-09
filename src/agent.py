import random

class Agent:
    
    """
        Agent control
            Ships : 4x ■, 3x ■■, 2x ■■■, 1x ■■■■, 1x ■■■■■
            Grid  : ∙ empty, ■ ship, o discrete zone
    """

# Init agent

    def __init__(self,name):
        self.name = name
        self.kind = "undefined"                             # "ai", "hi"
        self.ships_c = [0, 4, 3, 2, 1, 1]                   # ships counter
        self.ships_s = ["","■","■■","■■■","■■■■","■■■■■"]   # ships shape
        self.ships_m = self.find_ships_needed()             # maximum ships
        self.ships_f = []                                   # ships found
        self.to_check = []
        self.set_hi = set()
        self.grid_agent = self.gen_grid()
        self.grid_enemy = self.gen_grid()

# Miscellaneous

    def gen_grid(self):
        '''
            Generate empty grid
        '''
        rows = 10
        cols = 10
        grid = [[0 for i in range(cols+1)] for i in range(rows+1)]
        grid[0][0] = "\\"
        for i in range(1,cols+1):
            grid[0][i] = i
        for i in range(1,rows+1):
            grid[i][0] = i
        for i in range(1,rows+1):
            for j in range(1,cols+1):
                grid[i][j] = "∙"
        return grid

    def clean_grid(self):
        '''
            Set all signs in the grid to ∙
        '''
        rows = len(self.grid_agent)
        cols = len(self.grid_agent[0])
        for i in range(1,rows):
            for j in range(1,cols):
                self.grid_agent[i][j] = "∙"

    def print_grid(self,option):
        '''
            Print the grid while setting it up
        '''
        if option == "a":
            grid = self.grid_agent
        elif option == "e":
            grid = self.grid_enemy
        rows = len(grid)
        cols = len(grid[0])
        for i in range(rows):
            print("   ",end="")
            for j in range(cols):
                print("{:3}".format(str(grid[i][j])),end="")
            print()

    def finalize_grid(self):
        '''
            Set all ∙ to o after the winner is determined
        '''
        rows = len(self.grid_agent)
        cols = len(self.grid_agent[0])
        for i in range(1,rows):
            for j in range(1,cols):
                if self.grid_agent[i][j] == "∙":
                    self.grid_agent[i][j] = "o"

# Before game

    def point_within_boundaries(self,point):
        '''
            Determine whether a point is within grid boundaries
        '''
        if (1 <= point[0] <= 10) and (1 <= point[1] <= 10): return True
        else: return False
    
    def find_cells_needed(self,ships_c):
        '''
            Function calculate how many free cells
            are required to accommodate remaining ships
        '''
        cells_needed = 0
        for i in range(1,len(ships_c)):
            cells_needed += i*ships_c[i]
        return cells_needed

    def find_ships_needed(self):
        '''
            Scan through all kinds of ships and calculate
            total amount to be created in the grid
        '''
        ships_needed = 0
        for i in range(1,len(self.ships_c)):
            ships_needed += self.ships_c[i]
        return ships_needed

    def find_all_free_cells(self):
        '''
            Scan through the entire grid and find all ∙ points
        '''
        free_cells = []
        for i in range(1,10+1):
            for j in range(1,10+1):
                if self.grid_agent[i][j] == "∙":
                    free_cells.append((i,j))
        return free_cells

    def find_cells_between(self,rS,cS,rF,cF):
        '''
            Find all cells between two entered points
            Points must form either dots, vertical or horizontal segment
            Entered points cannot form ship longer than 5 cells
        '''
        cells_between=[]
        if self.point_within_boundaries((rS,cS)) and self.point_within_boundaries((rF,cF)):     # within boundaries
            if (rS == rF) or (cS == cF):                                                        # vertical or horizontal
                ln = abs(rF-rS) + abs(cF-cS) + 1                                                # length of a ship
                if ln == 1:
                    if self.grid_agent[rS][cS] == "∙":
                        cells_between.append((rS,cS))
                elif 1 < ln < len(self.ships_c):
                    if rF-rS != 0: sgn=(rF-rS)//abs(rF-rS)                                      # sign of a direction vector
                    else: sgn=(cF-cS)//abs(cF-cS)
                    for i in range(rS,rF+sgn,sgn):
                        for j in range(cS,cF+sgn,sgn):
                            if self.grid_agent[i][j] == "∙":                                    # find those cells are available
                                cells_between.append((i,j))
                    if len(cells_between) != ln:                                                # compare length and cells found
                        cells_between = []
        return cells_between

    def find_cells_ship(self,rS,cS):
        '''
            Function is used while removind ship
            Scan all potential cells in all 4 directions
            until next point is not ■
        '''
        cells_ship = []
        direct_r = [0,0,1,-1]
        direct_c = [1,-1,0,0]
        if self.point_within_boundaries((rS,cS)):                       # boundaries?
            if self.grid_agent[rS][cS] == "■":
                cells_ship.append((rS,cS))                              # at least one is found
                for i in range(4):                                      # try different directions U,D,L,R
                    for j in range(1,len(self.ships_c)-1):              # (1..4) distances from start cell
                        rC = rS + direct_r[i]*j
                        cC = cS + direct_c[i]*j
                        if self.point_within_boundaries((rC,cC)):       # boundaries?
                            if self.grid_agent[rC][cC] != "■":
                                break
                            else:
                                cells_ship.append((rC,cC))
        return cells_ship

    def find_max_ship(self,rS,cS,ships_c):
        '''
            Find coordinates of the maximum
            possible ship for a certain cell
        '''
        direct_r = [0,0,1,-1]
        direct_c = [1,-1,0,0]
        cells_between = []
        for factor in range(len(ships_c)-2,-1,-1):                                  # the longest available ship first
            if ships_c[factor+1] != 0:                                              # check whether ship with length is available
                random_indices = list(range(4))
                random.shuffle(random_indices)                                      # random direction
                for i in random_indices:
                    cells_between = self.find_cells_between(rS,cS,rS+direct_r[i]*factor,cS+direct_c[i]*factor)
                    if cells_between != []:    # return if placement is possible
                        return cells_between
        return cells_between

    def insert_ship(self,cells_between):
        '''
            Insert ship and its discrete zone
        '''
        discrete_zone = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(-1,1)]
        for i in cells_between:                     # update grid with ship
            self.grid_agent[i[0]][i[1]] = "■"
            for j in discrete_zone:                 # update grid with discrete zone
                if (1 <= i[0]+j[0] <= 10) and (1 <= i[1]+j[1] <= 10) and (self.grid_agent[i[0]+j[0]][i[1]+j[1]]) != "■":
                    self.grid_agent[i[0]+j[0]][i[1]+j[1]] = "o"

    def remove_ship(self,cells_ship):
        '''
            Remove ship with its discrete zone
        '''
        discrete_zone = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(-1,1)]
        for i in cells_ship:                                            # for all ship cells find possible discrete zone
            self.grid_agent[i[0]][i[1]] = "∙"
            for j in discrete_zone:
                o_point = (i[0]+j[0],i[1]+j[1])
                if self.point_within_boundaries(o_point):                    # find point without adjacent ship cells
                    adj_ship = False
                    for k in discrete_zone:
                        adj_point = (o_point[0]+k[0],o_point[1]+k[1])
                        if self.point_within_boundaries(adj_point) and self.grid_agent[adj_point[0]][adj_point[1]] == "■":
                            adj_ship = True
                            break
                    if not adj_ship: self.grid_agent[o_point[0]][o_point[1]] = "∙"

    def ships_manually(self):
        '''
            Handlind manual setting of the agent grid
        '''
        ships_a = 0                                                     # ships added already
        ships_c = self.ships_c[:]                                       # ships counter
        self.clean_grid()
        while ships_a < self.ships_m:                                   # ships in total vs. maximum
            print("   Your current grid.")
            print()
            self.print_grid("a")
            print()
            opt = ''
            while opt != "a" and opt != "r":                            # option whether add or remove ship
                opt = input("   Add (a) or remove (r) ship? ")
                print()
            if opt == "a":                                              # manual addition
                print("   ",end="")
                for i in range(1,len(ships_c)-1):
                    print("{}x {}, ".format(ships_c[i], self.ships_s[i]), end="")
                print("{}x {}.".format(ships_c[len(ships_c)-1], self.ships_s[len(ships_c)-1]))
                print()
                while True:                                             # enter start coordinates
                    try:
                        rS,cS = map(int, input("   Choose start coordinate (row column): ").split())
                        break
                    except:
                        print("   Entered coordinates are invalid. Try again.")
                while True:                                             # enter end coordinates
                        try:
                            rF,cF = map(int, input("   Choose end coordinate (row column): ").split())
                            break
                        except:
                            print("   Entered coordinates are invalid. Try again.")
                print()
                cells_between = self.find_cells_between(rS,cS,rF,cF)
                if cells_between == []:                                 # no points between
                    print("   Either length, shape is wrong or ships collide. Try again.")
                    print()
                elif ships_c[len(cells_between)] == 0:                  # no ship with necessary length
                    print("   There is no ship with length {} available. Try again.")
                    print()
                else:                                                   # proceed
                    self.insert_ship(cells_between)
                    ships_a += 1
                    ships_c[len(cells_between)] -= 1
            elif opt == "r":
                while True:                                             # enter coordinate
                    try:
                        rS,cS = map(int, input("   Choose any coordinate belonging to the ship (row column): ").split())
                        print()
                        break
                    except:
                        print("   Entered coordinate is invalid. Try again.")
                cells_ship = self.find_cells_ship(rS,cS)
                if cells_ship == []:
                    print("   There is no ship in the cell ({},{}).".format(rS,cS))
                    print()
                else:
                    self.remove_ship(cells_ship)
                    ships_a -= 1
                    ships_c[len(cells_ship)] += 1
        self.finalize_grid()
        print("   Your final grid.")
        print()
        self.print_grid("a")
        print()
        input("   Press Enter to continue.")
        print()

    def ships_automatically(self):
        '''
            Automatic grid
        '''
        ships_a = 0                                                         # ships already inserted
        ships_c = self.ships_c[:]                                           # ships counter
        self.clean_grid()                                                   # clean the grid
        while ships_a < self.ships_m:
            cells_free = self.find_all_free_cells()
            cells_needed = self.find_cells_needed(ships_c)
            if len(cells_free) < cells_needed:                              # such situation is VERY rare
                ships_a = 0
                ships_c = self.ships_c[:]
                self.clean_grid()
            else:
                rS,cS = random.choice(cells_free)                           # select any random point from free
                cells_between = self.find_max_ship(rS,cS,ships_c)           # find maximum possible and available ship to insert
                if cells_between == []:                                     # randomly chosen cell cannot be used
                    self.grid_agent[rS][cS] = "o"
                else:                                                       # insert ship
                    self.insert_ship(cells_between)
                    ships_a += 1
                    ships_c[len(cells_between)] -= 1
        self.finalize_grid()
        if self.kind == "hi":
            print("   Your final grid.")
            print()
            self.print_grid("a")
            print()

# During the game

    def ship_in_set_hi(self, enemy_cells_ship, set_hi):
        '''
            Determine whether all ship cells are in 
        '''
        p = True
        for i in enemy_cells_ship:
            if i not in set_hi:
                p = False
        return p

    def remove_ship_from_set_hi(self, enemy_cells_ship, set_hi):
        '''
            If any ship is found, remove all associated cells from
        '''
        for i in enemy_cells_ship:
            set_hi.remove(i)

    def find_enemy_free_cells(self):
        '''
            Scan enemy grid and find all ∙ cells
        '''
        free_cells = []
        for i in range(1,len(self.grid_enemy)):
            for j in range(1,len(self.grid_enemy[0])):
                if self.grid_enemy[i][j] == "∙":
                    free_cells.append((i,j))
        return free_cells

    def insert_enemy_ship(self,ships_f):
        '''
            Insert enemy ship into the grid if such is found
            in the set of found ■ points
        '''
        discrete_zone = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(-1,1)]
        for i in ships_f:                           # update grid with ship
            self.grid_enemy[i[0]][i[1]] = "■"
            for j in discrete_zone:                 # update grid with discrete zone
                if (1 <= i[0]+j[0] <= 10) and (1 <= i[1]+j[1] <= 10) and (self.grid_enemy[i[0]+j[0]][i[1]+j[1]]) != "■":
                    self.grid_enemy[i[0]+j[0]][i[1]+j[1]] = "o"

    def enter_point_manually(self):
        '''
            Dialog for entering valid point during the game
        '''
        while True:
            try:
                rC,cC = map(int, input("   Enter coordinate (row column): ").split())
                if not self.point_within_boundaries((rC,cC)):
                    print("   Point is out of boundaries. Try another.")
                elif self.grid_enemy[rC][cC] != "∙":
                    print("   Point is already checked. Try another.")
                else:
                    return rC,cC
            except:
                print("   Entered coordinate is invalid. Try again.")
