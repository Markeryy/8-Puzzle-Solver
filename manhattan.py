
WINNING_NUMBERS = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
numbers = [[1,2,3], [4,0,6], [7,5,8]]

# puzzle node class (bfs and dfs)
class PuzzleNode():
    def __init__(self, numbers, action, parent):
        self.numbers = numbers
        self.index_of_empty = search(numbers, 0)  # search for row and col of 0
        self.action = action
        self.parent = parent

    def search(self, numbers, x):
        for row in range(len(numbers)):
            for col in range(len(numbers[row])):
                if (x == numbers[row][col]):
                    return [row, col]

# puzzle node class (a star)
class PuzzleNodeAStar(PuzzleNode):
    # inherit from PuzzleNode
    def __init__(self, numbers, action, parent, g, h, f):
        super().__init__(numbers, action, parent)
        self.g = g 
        self.h = h
        self.f = f 

# search function to return row and column in the numbers 2d array
def search(numbers, x):
    for row in range(len(numbers)):
        for col in range(len(numbers[row])):
            if (x == numbers[row][col]):
                return [row, col]

node1 = PuzzleNode(numbers=numbers, action=None, parent=None)

node2 = PuzzleNode(numbers=[[1,0,3], [4,2,6], [7,5,8]], action='U', parent=node1)
node3 = PuzzleNode(numbers=[[1,2,3], [4,6,0], [7,5,8]], action='R', parent=node1)
node4 = PuzzleNode(numbers=[[1,2,3], [4,5,6], [7,0,8]], action='D', parent=node1)
node5 = PuzzleNode(numbers=[[1,2,3], [0,4,6], [7,5,8]], action='L', parent=node1)

def manhattan_distance(puzzle_node):
    num_list = puzzle_node.numbers
    distance = 0
    for row in range(len(num_list)):
        for col in range(len(num_list[row])):
            if num_list[row][col] == 0:
                continue
            
            if num_list[row][col] <= 3:
                correct_row = 0
            elif num_list[row][col] <= 6:
                correct_row = 1
            elif num_list[row][col] <= 8:
                correct_row = 2

            if num_list[row][col] == 1 or num_list[row][col] == 4 or num_list[row][col] == 7:
                correct_col = 0
            elif num_list[row][col] == 2 or num_list[row][col] == 5 or num_list[row][col] == 8:
                correct_col = 1
            elif num_list[row][col] == 3 or num_list[row][col] == 6:
                correct_col = 2

            distance += abs(correct_row - row) + abs(correct_col - col)

    return distance

def distance_from_root(puzzle_node):
    distance = 0
    while (puzzle_node.parent != None):
        distance += 1
        puzzle_node = puzzle_node.parent

    return distance

def f(puzzle_node):
    return manhattan_distance(puzzle_node) + distance_from_root(puzzle_node)

open_list = [node2, node3, node4, node5]
closed_list = []
# while (len(open_list) != 0):
# find best node and remove it from openList
def remove_min_f():
    fn_list = []
    for node in open_list:
        fn_list.append(f(node))
    minimum = min(fn_list)
    minimum_index = fn_list.index(minimum)
    
    removed = open_list.pop(minimum_index)
    return removed
best_node = remove_min_f()
closed_list.append(best_node)
if (best_node.numbers == WINNING_NUMBERS):
    # TODO: track it down
    pass



