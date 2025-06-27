import math
import heapq
import random
import time
import os

# =========================================================
#   DLSU NODES
# =========================================================

class DLSUNodes:
    """
    Purpose:
        Provides the list of eatery nodes, their cost, and their coordinates
    """
    def __init__(self):
        self.node_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J1', 'J2', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
        self.node_names = {
            "A": "University Mall",
            "B": "McDonald's",
            "C": "Pericos",
            "D": "Bloemen Hall",
            "E": "WH Taft",
            "F": "24 Chicken",
            "G": "Dixie's",
            "H": "Agno Food Court",
            "I": "One Archer's",
            "J1": "Kitchen Hall",
            "J2": "La Casita",
            "K": "Green Mall",
            "L": "Green Court",
            "M": "Sherwood",
            "N": "Jollibee",
            "O": "Tinuhog ni Benny",
            "P": "Zark's",
            "Q": "El Poco",
            "R": "Domino's",
            "S": "Kanto Freestyle",
            "T": "Samgyup Salamat",
            "U": "The Barn"
        }

        self.closed_nodes = []
        self.dlsu_eateries = {
            'A':  [('B', 60),  ('T', 300)],
            'B':  [('A', 60),  ('C', 115),   ('E', 280)],
            'C':  [('B', 115),  ('D', 350),  ('R', 130)],
            'D':  [('C', 350), ('E', 140)],
            'E':  [('B', 280), ('D', 140),   ('F', 35), ('O', 280)],
            'F':  [('E', 35),  ('G', 75),   ('O', 250)],
            'G':  [('F', 75),  ('H', 120),   ('I', 50)],
            'H':  [('G', 120),  ('L', 85)],
            'I':  [('G', 50),  ('J1', 65),  ('L', 170), ('N', 100)],
            'J1': [('I', 65),  ('K', 65)],
            'J2': [('L', 60),  ('K', 65)],
            'K':  [('J1', 65), ('J2', 65), ('M', 200), ('U', 80)],
            'L':  [('H', 85),  ('I', 170),   ('J2',60)],
            'M':  [('K', 200),  ('N', 60)],
            'N':  [('I', 100),  ('M', 60)],
            'O':  [('E', 280),  ('F', 250),   ('P', 145), ('S', 180)],
            'P':  [('O', 145),  ('S', 200)],
            'Q':  [('R', 280),   ('S', 170)],
            'R':  [('C', 130),  ('Q', 280),   ('T', 350)],
            'S':  [('O', 180),  ('P', 200),   ('Q', 170)],
            'T':  [('A', 300), ('R', 350)],
            'U':  [('K', 80)]
        }

        self.dlsu_eateries_coord = {
            'A': (350,0),
            'B': (300,0),
            'C': (255,-45),
            'D': (60,-45),
            'E': (30,0),
            'F': (0,0),
            'G': (-60,0),
            'H': (-45,-45),
            'I': (-90,-0),
            'J1': (-130,0),
            'J2': (-160,-45),
            'K': (-160,0),
            'L': (-115,-45),
            'M': (-160,25),
            'N': (-130,25),
            'O': (45,75),
            'P': (130,25),
            'Q': (210,200),
            'R': (260,25),
            'S': (200,100),
            'T': (440,185),
            'U': (-215,-45)
        }
        
    def isExistingNode(self, node: str) -> bool:
        # Checks in list if node exists or not
        if node in self.node_list:
            return True
        return False

    def isClosed(self, node: str) -> bool:
        # Checks in list if node is closed or not
        if node in self.closed_nodes:
            return True
        return False
        
    def isPath(self, origin: str, destination: str) -> bool:
        # Checks in dictionary if destination is in origin
        for node, _ in self.dlsu_eateries[origin]:
            if node == destination:
                return True
        return False

    def addNode(self, code: str, name: str, coord: tuple, neighbors: list[tuple[str, int]]) -> bool:
        if self.isExistingNode(code):
            return False
        # 1) register the node
        self.node_list.append(code)
        self.node_names[code] = name
        self.dlsu_eateries_coord[code] = coord
        self.dlsu_eateries[code] = []

        # 2) bidirectional edges
        for nb, cost in neighbors:
            if not self.isExistingNode(nb):
                continue            
            self.dlsu_eateries[code].append((nb, cost))
            self.dlsu_eateries.setdefault(nb, []).append((code, cost))
            return True

    def closeNode(self, code: str) -> bool:
        if self.isExistingNode(code) and code not in self.closed_nodes:
            self.closed_nodes.append(code)
            return True
        return False

    def openNode(self, code: str) -> bool:
        if code in self.closed_nodes:
            self.closed_nodes.remove(code)
            return True
        return False

        

# =========================================================
#   ALGORITHMS
# =========================================================
       
class Algorithms:
    """
    Purpose:
        Provides two algorithms along with supporting functions for algorithms to work
    """
    def __init__(self, eateries: DLSUNodes):
        self.eateries = eateries

    def generateHeuristics(self, starting_node: str) -> set:
        starting_coord = self.eateries.dlsu_eateries_coord[starting_node]
        heuristics = {}
        for node in self.eateries.node_list:
            heuristics[node] = round(math.sqrt((self.eateries.dlsu_eateries_coord[node][0] - starting_coord[0])**2 + (self.eateries.dlsu_eateries_coord[node][1] - starting_coord[1])**2))
        return heuristics
    
    def uniformCostSearch(self, origin: str, destination: str) -> list:
        if origin == destination:
            return [origin], 0, [origin] # example: 0, ['A'], ['A']
        
        comparison_list = [] # this will be used to heapq to compare
        visited_nodes = [] # avoid having some paths to revisit node since revisit means someone with lower cost is already in the list
        list_of_paths = [0, origin, [origin]]  # total cost, current node, list of path
        heapq.heappush(comparison_list, list_of_paths) # heapq is better and optimized than doing it manually
        no_dest = True
        while no_dest:
            total_cost, current_node, current_pathing = heapq.heappop(comparison_list) # Get the path with smallest cost since priority

            if current_node == destination: # already found the pathing so return already
                return current_pathing, total_cost, visited_nodes

            # note if visited to save resources
            if current_node in visited_nodes:
                continue # disregard this pathing
            else:
                visited_nodes.append(current_node)
            
            # since not yet destination, visit the children nodes
            for child_node, child_cost in self.eateries.dlsu_eateries[current_node]:
                # update this node and add the children nodes to the comparison list
                duplicate_current_pathing = list(current_pathing) # duplicate pathing
                duplicate_current_pathing.append(child_node)
                new_item = [total_cost + child_cost, child_node, duplicate_current_pathing]
                heapq.heappush(comparison_list, new_item)

    def AStarSearch(self, origin: str, destination: str):
        open_set = []
        heapq.heappush(open_set, (0, origin))
        came_from = {}
        g_score = {node: float('inf') for node in self.eateries.dlsu_eateries}
        g_score[origin] = 0
        f_score = {node: float('inf') for node in self.eateries.dlsu_eateries}
        heuristic_graph = self.generateHeuristics(destination)
        f_score[origin] = heuristic_graph[origin]
        explored = []
        while open_set:
            current_f, current = heapq.heappop(open_set)
            explored.append(current)
            if current == destination: # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path, g_score[destination], explored
            for neighbor, cost in self.eateries.dlsu_eateries[current]:
                tentative_g = g_score[current] + cost
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic_graph[neighbor]
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        # return None, float('inf'), explored


# =========================================================
#   DISPLAY
# =========================================================
       
class Display:
    """
    Purpose:
        Provides display prints to avoid cluttering the main function
    """
    def __init__(self, eateries: DLSUNodes):
        self.eateries = eateries
        # ANSI color codes
        self.CYAN = '\033[96m'
        self.LIGHT_CYAN = "\033[1;36m"
        self.MAGENTA = '\033[95m'
        self.YELLOW = '\033[93m'
        self.GREEN = '\033[92m'
        self.RED = '\033[91m'
        self.BLUE = '\033[94m'
        self.PURPLE = "\033[0;35m"
        self.BOLD = '\033[1m'
        self.RESET = '\033[0m'
        

    def welcomeDisplay(self):
        print(self.BOLD + "======================================================================================" + self.RESET)
        print(self.LIGHT_CYAN + "                    _____ _____ _____ __    _ _______ _____ __   __ " + self.RESET)
        print(self.LIGHT_CYAN + "                   /  ___/  ___|_   _|  \\  | |__   __/  ___|\\ \\ / / " + self.RESET)
        print(self.LIGHT_CYAN + "                  |  |   \\____ \\ | | | | \\ | |  | |  \\____ \\ \\ V /  " + self.RESET)
        print(self.LIGHT_CYAN + "                  |  |___ ____> || |_| |\\ \\| |  | |   ____> | | |   " + self.RESET)
        print(self.LIGHT_CYAN + "                   \\_____|_____/_____|_| \\___|  |_|  |_____/  |_|   " + self.RESET)
        print(self.LIGHT_CYAN +"                  --------------------------------------------------" + self.RESET)
        print(self.YELLOW + "                                       GROUP 5                      " + self.RESET)
        print(self.YELLOW + "                               CHUA, HA, MISAGAL, TELOSA            " + self.RESET)
        print(self.BOLD + "======================================================================================\n" + self.RESET)

    def ASCIIKainanKalyewa(self):
        print(self.CYAN + r"""
   ,                                       ,            _                          
  /|   /       o                          /|   /       | |                         
   |__/   __,      _  _    __,   _  _      |__/   __,  | |        _           __,  
   | \   /  |  |  / |/ |  /  |  / |/ |     | \   /  |  |/  |   | |/  |  |  |_/  |  
   |  \_/\_/|_/|_/  |  |_/_/|_/   |  |_/   |  \_/\_/|_/|__/ \_/|/|__/ \/ \/  \_/|_/
                                                              /|                   
                                                              \|                   
        """ + self.RESET)

    def eateryChoices(self):
        print(self.YELLOW + "* * * * * * * * * * * * * * * * * * * * * * * * * * * * *" + self.RESET)      
        for letter, restaurant in self.eateries.node_names.items():
            color = self.RESET
            if letter in self.eateries.closed_nodes:
                color = self.RED
            print(self.YELLOW + f"[{letter}]" + color + f" {restaurant}" + self.RESET)
        print(self.RED + "\n[NOTE] Restaurants in RED means CLOSED" + self.RESET)
        print(self.YELLOW + "* * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n" + self.RESET)

    def displayResult(self, search_type: str, path: list, cost: int, expanded: list, t0: float, t1: float):
        print(self.MAGENTA + f"\n==================== {search_type} RESULT ====================" + self.RESET)
        print(self.BLUE + "Path:" + self.RESET)
        compact_path = []
        for i, node in enumerate(path):
            if i == 0:
                compact_path.append(self.GREEN + self.BOLD + f"[START: {node}]" + self.RESET)
            elif i == len(path) - 1:
                compact_path.append(self.RED + self.BOLD + f"[GOAL: {node}]" + self.RESET)
            else:
                compact_path.append(self.YELLOW + f"{node}" + self.RESET)
        print("".join([f"{n} ==> " if i < len(compact_path)-1 else n for i, n in enumerate(compact_path)]))
        print(self.GREEN + f"\nTotal Cost: {cost}" + self.RESET)
        print(self.BLUE + f"\nNodes Expanded: {len(expanded)}" + self.RESET)
        print(self.BLUE + "\nExpanded Nodes:" + self.RESET)
        print("  " + ", ".join(expanded))
        print(self.CYAN + f"\nSearch Time: {round((t1-t0)*1000, 2)} ms" + self.RESET)
        print(self.MAGENTA + "===============================================================\n" + self.RESET)


# =========================================================
#   DEMO / MAIN
# =========================================================

def main():
    nodes = DLSUNodes()
    algo = Algorithms(nodes)
    display = Display(nodes)

    os.system('cls' if os.name == 'nt' else 'clear') # Clear the console for a cleaner look
    display.welcomeDisplay()
    while True:
        display.ASCIIKainanKalyewa()
        print("Welcome to KAINAN KALYEWA! Kindly pick any of the following below:")
        print("[1] Route Finder")
        print("[2] Settings")
        print("[3] Exit")
        
        choice = input("Enter your choice [1-3]: ").strip()
        
        if choice == '1':
            print("\n\nAvailable DLSU Eateries: Choose their corresponding letters: ")
            display.eateryChoices()
            
            origin = " "
            while not nodes.isExistingNode(origin) or nodes.isClosed(origin):
                origin = input("[ORIGIN] Where are you right now? ").strip()
                if not nodes.isExistingNode(origin):
                    print("That location does not exist! Please try again.\n")
                elif nodes.isClosed(origin):
                    print("That location is currently CLOSED. Please pick another.\n")

            destination = " "
            while not nodes.isExistingNode(destination) or nodes.isClosed(destination):
                destination = input("[DEST] Where do you want to go? ").strip()
                if not nodes.isExistingNode(destination):
                    print("That destination does not exist! Please try again.\n")
                elif nodes.isClosed(destination):
                    print("That destination is currently CLOSED. Please pick another.\n")

            print("\nChoose a type of search algorithm:")
            invalid = True
            while invalid:
                print("[1] Blind Search")
                print("[2] Heuristic Search")
                
                choice = input("Enter your choice (1-2): ").strip()
                pass
                if choice == '1':
                    start_time = time.time()
                    path, cost, expanded = algo.uniformCostSearch(origin, destination)
                    end_time = time.time()
                    display.displayResult("Uniform Cost Search", path, cost, expanded, start_time, end_time)
                    invalid = False
                    input("Press Enter to continue...")
                elif choice == '2':
                    start_time = time.time()
                    path, cost, expanded = algo.AStarSearch(origin, destination)
                    end_time = time.time()
                    display.displayResult("A* Search", path, cost, expanded, start_time, end_time)
                    invalid = False
                    input("Press Enter to continue...")
                else:
                    print("Invalid option. Please try again.")
                print(" ")
                
        elif choice == '2':
            while True:
                print("\nSettings Menu")
                print("[1] Add New Establishment")
                print("[2] Close an Establishment")
                print("[3] Reopen an Establishment")
                print("[4] Back to Main Menu")

                s_choice = input("Enter your choice [1-4]: ").strip()

                # add nodes
                if s_choice == '1':
                    code = input(" • New node code (e.g., 'V'): ").strip()
                    if nodes.isExistingNode(code):
                        print("That code already exists.")
                        continue

                    name = input(" • Restaurant name: ").strip()
                    try:
                        x = int(input(" • X coordinate: "))
                        y = int(input(" • Y coordinate: "))
                    except ValueError:
                        print("Coordinates must be integers.")
                        continue

                    # gather neighbors
                    neighbors = []
                    print(" • Add neighbors:")
                    while True:
                        nb = input("    Neighbor code: ").strip()
                        if nb == '':
                            break
                        if not nodes.isExistingNode(nb):
                            print("      Unknown node – Please try again.")
                            continue
                        try:
                            cost = int(input(f"     Cost {code} ↔ {nb}: "))
                        except ValueError:
                            print("      Cost must be an integer.")
                            continue
                        neighbors.append((nb, cost))

                    if nodes.addNode(code, name, (x, y), neighbors):
                        print(f"    Added {name} [{code}] with {len(neighbors)} neighbor(s).")
                    else:
                        print("    Failed to add node.")

                # close node
                elif s_choice == '2':
                    target = input(" • Node code to close: ").strip()
                    if nodes.closeNode(target):
                        print(f"    {target} is now marked as CLOSED.")
                    else:
                        print("    Invalid code or already closed.")

                # open node
                elif s_choice == '3':
                    target = input(" • Node code to reopen: ").strip()
                    if nodes.openNode(target):
                        print(f"    {target} is now OPEN.")
                    else:
                        print("    Invalid code or already open.")

                elif s_choice == '4':
                    print("  Returning to main menu...\n")
                    break
                else:
                    print("    Invalid option – Please try again.")

        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")

        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
