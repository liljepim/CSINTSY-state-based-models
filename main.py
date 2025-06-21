import math
import heapq

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
            "F": "EGI Taft (24 Chicken)",
            "G": "Castro Street (Dixie's)",
            "H": "Agno Food Court",
            "I": "One Archer's",
            "J1": "Kitchen Hall",
            "J2": "La Casita",
            "K": "Green Mall",
            "L": "Green Court",
            "M": "Sherwood",
            "N": "Jollibee",
            "O": "Dagonoy Street (Tinuhog ni Benny)",
            "P": "Burgundy (Zark's)",
            "Q": "Estrada Street (El Poco)",
            "R": "D'Student's Place (Domino's)",
            "S": "Leon Guinto Street (Kanto Freestyle)",
            "T": "P.Ocampo Street (Samgyup Salamat)",
            "U": "Fidel A. Reyes Street (The Barn)"
        }

        self.closed_nodes = {}
        self.dlsu_eateries = {
            'A':  [('B', 1),  ('T', 10)],
            'B':  [('A', 1),  ('C', 4),   ('E', 20)],
            'C':  [('B', 4),  ('D', 15),  ('R', 7)],
            'D':  [('C', 15), ('E', 7)],
            'E':  [('B', 20), ('D', 7),   ('F', 1), ('O', 7)],
            'F':  [('E', 1),  ('G', 3),   ('O', 9)],
            'G':  [('F', 3),  ('H', 7),   ('I', 2)],
            'H':  [('G', 7),  ('L', 3)],
            'I':  [('G', 2),  ('J1', 6),  ('L', 5), ('N', 9)],
            'J1': [('I', 6),  ('K', 6)],
            'J2': [('L', 3),  ('K', 10)],
            'K':  [('J1', 6), ('J2', 10), ('M', 8), ('U', 10)],
            'L':  [('H', 3),  ('I', 5),   ('J2', 3)],
            'M':  [('K', 8),  ('N', 3)],
            'N':  [('I', 9),  ('M', 3)],
            'O':  [('E', 7),  ('F', 9),   ('P', 4), ('S', 6)],
            'P':  [('O', 4),  ('Q', 2),   ('S', 2)],
            'Q':  [('P', 2),  ('R', 5),   ('S', 4)],
            'R':  [('C', 7),  ('Q', 5),   ('T', 12)],
            'S':  [('O', 6),  ('P', 2),   ('Q', 4)],
            'T':  [('A', 10), ('R', 12)],
            'U':  [('K', 10)]
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

    def add_node(self, code: str, name: str, coord: tuple, neighbors: list[tuple[str, int]]) -> bool:
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

    def close_node(self, code: str) -> bool:
        if self.isExistingNode(code) and code not in self.closed_nodes:
            self.closed_nodes[code] = True
            return True
        return False

    def open_node(self, code: str) -> bool:
        if code in self.closed_nodes:
            self.closed_nodes.pop(code)
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

    def generate_heuristics(self, starting_node: str) -> set:
        starting_coord = self.eateries.dlsu_eateries_coord[starting_node]
        heuristics = {}
        for node in self.eateries.node_list:
            heuristics[node] = round(math.sqrt((self.eateries.dlsu_eateries_coord[node][0] - starting_coord[0])**2 + (self.eateries.dlsu_eateries_coord[node][1] - starting_coord[1])**2))
        return heuristics
    
    def uniformCostSearch(self, origin: str, destination: str) -> list:
        if origin == destination:
            return [0, [origin]] # example: 0, ['A']
        
        comparison_list = [] # this will be used to heapq to compare
        visited_nodes = [] # avoid having some paths to revisit node since revisit means someone with lower cost is already in the list
        list_of_paths = [0, origin, [origin]]  # total cost, current node, list of path --> after some crashout, i realize na nagiging alphabetical yung ordering so nagbabase pala siya sa first element
        heapq.heappush(comparison_list, list_of_paths) # heapq finds the element with the smallest number from the list --> better and optimized than doing it manually
        no_dest = True
        while no_dest:
            total_cost, current_node, current_pathing = heapq.heappop(comparison_list) # Get the path with smallest cost since priority

            if current_node == destination: # already found the pathing so return already (no need to continue since this is the smallest cost out of all in the queue)
                return [total_cost, current_pathing] # you can refer sa if origin == destination kung ano itsure ng result

            # note if visited to save resources
            if current_node in visited_nodes:
                continue # disregard this pathing
            else:
                visited_nodes.append(current_node)
            
            # since not yet destination, visit the children nodes
            for child_node, child_cost in self.eateries.dlsu_eateries[current_node]:
                # update this node and add the children nodes to the comparison list
                duplicate_current_pathing = list(current_pathing) # it is possible to have more than one child so have an extra copy para hindi masira yung current pathing
                duplicate_current_pathing.append(child_node)
                new_item = [total_cost + child_cost, child_node, duplicate_current_pathing]
                heapq.heappush(comparison_list, new_item)


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

    def welcomeDisplay(self):
        print("==================================================")
        print("  _____ _____ _____ __    _ _______ _____ __   __ ")
        print(" /  ___/  ___|_   _|  \\  | |__   __/  ___|\\ \\ / / ")
        print("|  |   \\____ \\ | | | | \\ | |  | |  \\____ \\ \\ V /  ")
        print("|  |___ ____> || |_| |\\ \\| |  | |   ____> | | |   ")
        print(" \\_____|_____/_____|_| \\___|  |_|  |_____/  |_|   ")
        print("--------------------------------------------------")
        print("                     GROUP 5                      ")
        print("             CHUA, HA, MISAGAL, TELOSA            ")
        print("==================================================\n")
        
        
        #  _____ _____ _____ __    _ _______ _____ __   __
        # /  ___/  ___|_   _|  \  | |__   __/  ___|\ \ / /
        #|  |   \____ \ | | | | \ | |  | |  \____ \ \ V /
        #|  |___ ____> || |_| |\ \| |  | |   ____> | | |
        # \_____|_____/_____|_| \___|  |_|  |_____/  |_|
        

    def eateryChoices(self):
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")      
        for letter, restaurant in self.eateries.node_names.items():
            symbol = " "
            if letter in self.eateries.closed_nodes:
                symbol = "++"
            print(f"[{letter}] {restaurant} {symbol}")
        print("\n[NOTE] ++ at the end of the restaurant name means CLOSED")
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")

# =========================================================
#   DEMO / MAIN
# =========================================================

def main():
    nodes = DLSUNodes()
    algo = Algorithms(nodes)
    display = Display(nodes)

    display.welcomeDisplay()
    print("Welcome to ___! Kindly pick any of the following below:")
    while True:
        print("[1] Where to? (BASTA GANYAN IDK HOW TO WORD IT)")
        print("[2] Settings")
        print("[3] Exit")
        
        choice = input("Enter your choice [1-3]: ").strip()
        
        if choice == '1':
            print("\n\nHere are the selection of DLSU eateries! Choose their corresponding letters: ")
            display.eateryChoices()
            
            origin = " "
            while not nodes.isExistingNode(origin) or nodes.isClosed(origin):
                origin = input("[ORIGIN] Where are you right now? ").strip()
                if not nodes.isExistingNode(origin):
                    print("This character does not exist! Please try again.\n")

            destination = " "
            while not nodes.isExistingNode(destination) or nodes.isClosed(destination):
                destination = input("[DEST] Where do you want to go? ").strip()
                if not nodes.isExistingNode(destination):
                    print("This character does not exist! Please try again.\n")

            print("\nChoose a type of algorithm:")
            invalid = True
            while invalid:
                print("[1] Blind Search")
                print("[2] Heuristic Search")
                
                choice = input("Enter your choice (1-2): ").strip()
                pass
                if choice == '1':
                    print(algo.uniformCostSearch(origin, destination)) #sample run for uniformCostSearch WILL FIX SOON
                    invalid = False
                elif choice == '2':
                    # Heuristic Search Here
                    invalid = False
                else:
                    print("Invalid option. Please try again.")
                print(" ")
                
        elif choice == '2':
            # Settings
            pass
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == '__main__':
    main()
