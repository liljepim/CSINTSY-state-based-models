import math

node_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J1', 'J2', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
dlsu_eateries = {
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

dlsu_eateries_coord = {
    'A':(350,0),
    'B':(300,0),
    'C':(255,-45),
    'D':(60,-45),
    'E':(30,0),
    'F':(0,0),
    'G':(-60,0),
    'H':(-45,-45),
    'I':(-90,-0),
    'J1':(-130,0),
    'J2':(-160,-45),
    'K':(-160,0),
    'L':(-115,-45),
    'M':(-160,25),
    'N':(-130,25),
    'O':(45,75),
    'P':(130,25),
    'Q':(210,200),
    'R':(260,25),
    'S':(200,100),
    'T':(440,185),
    'U':(-215,-45)
}

def generate_heuristics(starting_node):
    starting_coord = dlsu_eateries_coord[starting_node]
    heuristics = {}
    for node in node_list:
        heuristics[node] = round(math.sqrt((dlsu_eateries_coord[node][0] - starting_coord[0])**2 + (dlsu_eateries_coord[node][1] - starting_coord[1])**2))
    return heuristics

#print(generate_heuristics('F'))

def main():
    
    while True:
        print("---INTRO BANNER HERE---")
        print("[1] Blind Search")
        print("[2] Heuristic Search")
        print("[3] Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            # Blind Search Here
            pass
        elif choice == '2':
            # Heuristic Search Here
            pass
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")
            
if __name__ == '__main__':
    main()