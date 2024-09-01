# pip install pygame

from json import load
from multiprocessing import parent_process
from tkinter import filedialog
import pygame  # pip install pygame
import os
import tkinter as tk
from tkinter import *

from block import *
from button import *
from queue_class import *
from stack_class import *
from copy import deepcopy

FONT = pygame.font.Font('freesansbold.ttf', 32)
WINNING_NUMBERS = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
TEXT_POS = (45, 280)

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

# puzzle node class (a star), inherit from puzzle node class
class PuzzleNodeAStar(PuzzleNode):
    def __init__(self, numbers, action, parent, g=None):
        super().__init__(numbers, action, parent)
        self.g = g

# function to load the puzzle.in file (puzzle input)
def load_puzzle_input(puzzle_to_load):
    with open(puzzle_to_load, mode="r") as file:
        numbers = file.readlines()  # read the input file (return a list per line)

        # remove the \n and split by space
        for i in range(len(numbers)):
            numbers[i] = numbers[i].strip("\n")  # remove new line
            numbers[i] = numbers[i].split(" ")  # split by space

        # convert all numbers (string) to integer
        for i in range(len(numbers)):
            for j in range(len(numbers[i])):
                numbers[i][j] = int(numbers[i][j])
        
    return numbers

# function to check if the 2d array of integers are solvable
def is_solvable(numbers):
    num_1d = []
    inversions = 0

    # convert 2d numbers array to 1d array
    for i in range(len(numbers)):
        for j in range(len(numbers[i])):    
            num_1d.append(numbers[i][j])

    # loop through array num_1d[i] is the reference for comparison
    for i in range(len(num_1d)):
        if (num_1d[i] == 0):  # skip if zero
            continue
        
        # num_1d[j] represents the succeeding numbers to num_1d[i]
        for j in range(i+1, len(num_1d)): 
            if (num_1d[j] == 0):  # skip if zero
                continue

            # if current number is greater than succeeding numbers, append inversions
            if num_1d[i] > num_1d[j]:
                # print(f"{num_1d[i]} > {num_1d[j]}")
                inversions += 1

    # print(inversions)
    return inversions % 2 == 0

# function to initialize screen text below the puzzle
def init_screen_text():
    # check if puzzle is solvable
    if is_solvable(numbers):
        # screen text (if solvable)
        screen_text = FONT.render("Solvable!", True, (255, 255, 255))
    else:
        # screen text (if unsolvable)
        screen_text = FONT.render("Unsolvable!", True, (255, 255, 255))
    
    return screen_text

# function to draw screen text below the puzzle
def draw_screen_text(text, screen):
    screen.blit(text, TEXT_POS)

# search function to return row and column in the numbers 2d array
def search(numbers, x):
    for row in range(len(numbers)):
        for col in range(len(numbers[row])):
            if (x == numbers[row][col]):
                return [row, col]

# file dialog (for loading new puzzle)
def open_file():
    global numbers
    global initial_numbers
    global puzzle_to_load

    try:
        root.filename = filedialog.askopenfile(initialdir="./", title="Select Puzzle", filetypes=(("puzzle input file", "*.in"), ("all files", "*.*")))
        with open(f"{root.filename.name}", mode="r") as file:
            numbers = file.readlines()  # read the input file (return a list per line)

            # remove the \n and split by space
            for i in range(len(numbers)):
                numbers[i] = numbers[i].strip("\n")  # remove new line
                numbers[i] = numbers[i].split(" ")  # split by space

            # convert all numbers (string) to integer
            for i in range(len(numbers)):
                for j in range(len(numbers[i])):
                    numbers[i][j] = int(numbers[i][j])
        
        puzzle_to_load = f"{root.filename.name}"
        initial_numbers = deepcopy(numbers)
        return numbers
    except:
        print("Closed File Dialog")
        pass

# BFS function
def BFSearch(numbers):
    frontier = Queue()  # candidate 2d array for expansion
    node_frontier = Queue()  # to track nodes

    initial_puzzle_node = PuzzleNode(numbers, None, None)  # will serve as initial puzzle node

    frontier.enqueue(initial_puzzle_node.numbers)  # store 2d arrays
    node_frontier.enqueue(initial_puzzle_node)  # store puzzle nodes
    
    explored = []  # explored 2d array
    iterations = 1  # number of iterations
    while (frontier.length() != 0):
        # extract the current puzzle array and node
        current_state = frontier.dequeue()
        current_node = node_frontier.dequeue()
        swapped_state = []  # initialize state that will store the swapped 2d array
        explored.append(current_state)
        # print(f"CURRENT: {current_state}")  # print the current state
        # if current iteration is the winning condition
        if (current_state == WINNING_NUMBERS):
            actions_list = []  # create an actions list
            while (current_node.parent != None):  # iterate through all of the actions taken
                actions_list.insert(0, current_node.action)  # insert to the first element (to avoid reversing the list)
                current_node = current_node.parent  # go to the parent (previous node)
            return actions_list
        else:
            iterations += 1
            print(f"ITERATIONS: {iterations}")
            # for actions in currentstate:
                # if result not in explored
                    # frontier.enqueue(result)

            zero_row_and_col = search(current_state, 0)
            z_row = zero_row_and_col[0]
            z_col = zero_row_and_col[1]

            # swap with top
            try:
                swapped_state = deepcopy(current_state)  # deepcopy to avoid list references
                if (z_row-1 == -1):
                    # print("top not possible")
                    pass
                else:
                    temp = swapped_state[z_row-1][z_col]
                    swapped_state[z_row-1][z_col] = swapped_state[z_row][z_col]
                    swapped_state[z_row][z_col] = temp
                    # print(f"TOP: {swapped_state}")
                    # append to queue
                    if ((not swapped_state in explored) or (not swapped_state in frontier)):
                        frontier.enqueue(swapped_state)
                        puzzle_node = PuzzleNode(numbers=swapped_state, action='U', parent=current_node)
                        node_frontier.enqueue(puzzle_node)
            except:
                # print("top error")
                pass

            # swap with right
            try:
                swapped_state = deepcopy(current_state)  # deepcopy to avoid list references
                if (z_col+1 == 3):
                    # print("right not possible")
                    pass
                else:
                    temp = swapped_state[z_row][z_col+1]
                    swapped_state[z_row][z_col+1] = swapped_state[z_row][z_col]
                    swapped_state[z_row][z_col] = temp
                    # print(f"RIGHT: {swapped_state}")
                    # append to queue
                    if ((not swapped_state in explored) or (not swapped_state in frontier)):
                        frontier.enqueue(swapped_state)
                        puzzle_node = PuzzleNode(numbers=swapped_state, action='R', parent=current_node)
                        node_frontier.enqueue(puzzle_node)
            except:
                # print("right error")
                pass

            # swap with bottom
            try:
                swapped_state = deepcopy(current_state)  # deepcopy to avoid list references

                if (z_row+1 == 3):
                    # print("bottom not possible")
                    pass
                else:
                    temp = swapped_state[z_row+1][z_col]
                    swapped_state[z_row+1][z_col] = swapped_state[z_row][z_col]
                    swapped_state[z_row][z_col] = temp
                    # print(f"BOTTOM: {swapped_state}")
                    # append to queue
                    if ((not swapped_state in explored) or (not swapped_state in frontier)):
                        frontier.enqueue(swapped_state)
                        puzzle_node = PuzzleNode(numbers=swapped_state, action='D', parent=current_node)
                        node_frontier.enqueue(puzzle_node)
            except:
                # print("bottom error")
                pass

            # swap with left
            try:
                swapped_state = deepcopy(current_state)  # deepcopy to avoid list references
                if (z_col-1 == -1):
                    # print("left not possible")
                    pass
                else:
                    temp = swapped_state[z_row][z_col-1]
                    swapped_state[z_row][z_col-1] = swapped_state[z_row][z_col]
                    swapped_state[z_row][z_col] = temp
                    # print(f"LEFT: {swapped_state}")
                    # append to queue
                    if ((not swapped_state in explored) or (not swapped_state in frontier)):
                        frontier.enqueue(swapped_state)
                        puzzle_node = PuzzleNode(numbers=swapped_state, action='L', parent=current_node)
                        node_frontier.enqueue(puzzle_node)
            except:
                # print("left error")
                pass

# DFS function          
def DFSearch(numbers):
    frontier = Stack()  # candidate 2d array for expansion
    node_frontier = Stack()  # to track nodes

    initial_puzzle_node = PuzzleNode(numbers, None, None)  # will serve as initial puzzle node

    frontier.push(initial_puzzle_node.numbers)  # store 2d arrays
    node_frontier.push(initial_puzzle_node)  # store puzzle nodes
    
    explored = []  # explored 2d array
    iterations = 1  # number of iterations
    while (frontier.length() != 0):
        # extract the current puzzle array and node
        current_state = frontier.pop()
        current_node = node_frontier.pop()
        swapped_state = []  # initialize state that will store the swapped 2d array
        explored.append(current_state)
        # print(f"CURRENT: {current_state}")  # print the current state

        # if current iteration is the winning condition
        if (current_state == WINNING_NUMBERS):
            actions_list = []  # create an actions list
            while (current_node.parent != None):  # iterate through all of the actions taken
                actions_list.insert(0, current_node.action)  # insert to the first element (to avoid reversing the list)
                current_node = current_node.parent  # go to the parent (previous node)
            return actions_list
        else:
            iterations += 1
            print(f"ITERATIONS: {iterations}")
            # for actions in currentstate:
                # if result not in explored
                    # frontier.push(result)

            zero_row_and_col = search(current_state, 0)
            z_row = zero_row_and_col[0]
            z_col = zero_row_and_col[1]

            # swap with top
            try:
                swapped_state = deepcopy(current_state)  # deepcopy to avoid list references
                if (z_row-1 == -1):
                    # print("top not possible")
                    pass
                else:
                    temp = swapped_state[z_row-1][z_col]
                    swapped_state[z_row-1][z_col] = swapped_state[z_row][z_col]
                    swapped_state[z_row][z_col] = temp
                    # print(f"TOP: {swapped_state}")
                    # append to stack
                    if ((not swapped_state in explored) or not (swapped_state in frontier)):
                        frontier.push(swapped_state)
                        puzzle_node = PuzzleNode(numbers=swapped_state, action='U', parent=current_node)
                        node_frontier.push(puzzle_node)
            except:
                # print("top error")
                pass

            # swap with right
            try:
                swapped_state = deepcopy(current_state)  # deepcopy to avoid list references
                if (z_col+1 == 3):
                    # print("right not possible")
                    pass
                else:
                    temp = swapped_state[z_row][z_col+1]
                    swapped_state[z_row][z_col+1] = swapped_state[z_row][z_col]
                    swapped_state[z_row][z_col] = temp
                    # print(f"RIGHT: {swapped_state}")
                    # append to stack
                    if ((not swapped_state in explored) or not (swapped_state in frontier)):
                        frontier.push(swapped_state)
                        puzzle_node = PuzzleNode(numbers=swapped_state, action='R', parent=current_node)
                        node_frontier.push(puzzle_node)
            except:
                # print("right error")
                pass

            # swap with bottom
            try:
                swapped_state = deepcopy(current_state)  # deepcopy to avoid list references

                if (z_row+1 == 3):
                    # print("bottom not possible")
                    pass
                else:
                    temp = swapped_state[z_row+1][z_col]
                    swapped_state[z_row+1][z_col] = swapped_state[z_row][z_col]
                    swapped_state[z_row][z_col] = temp
                    # print(f"BOTTOM: {swapped_state}")
                    # append to stack
                    if ((not swapped_state in explored) or not (swapped_state in frontier)):
                        frontier.push(swapped_state)
                        puzzle_node = PuzzleNode(numbers=swapped_state, action='D', parent=current_node)
                        node_frontier.push(puzzle_node)
            except:
                # print("bottom error")
                pass

            # swap with left
            try:
                swapped_state = deepcopy(current_state)  # deepcopy to avoid list references
                if (z_col-1 == -1):
                    # print("left not possible")
                    pass
                else:
                    temp = swapped_state[z_row][z_col-1]
                    swapped_state[z_row][z_col-1] = swapped_state[z_row][z_col]
                    swapped_state[z_row][z_col] = temp
                    # print(f"LEFT: {swapped_state}")
                    # append to stack
                    if ((not swapped_state in explored) or not (swapped_state in frontier)):
                        frontier.push(swapped_state)
                        puzzle_node = PuzzleNode(numbers=swapped_state, action='L', parent=current_node)
                        node_frontier.push(puzzle_node)
            except:
                # print("left error")
                pass

# ASearch function
def ASearch(numbers):
    # h(node) - returns the manhattan distance of a node
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

    # g(node) - returns the distance from root
    def distance_from_root(puzzle_node):
        distance = 0
        while (puzzle_node.parent != None):
            distance += 1
            puzzle_node = puzzle_node.parent

        return distance

    # returns h(node) + g(node)
    def f(puzzle_node):
        return manhattan_distance(puzzle_node) + distance_from_root(puzzle_node)

    # return the minimum and remove it from the open list
    def remove_min_f():
        fn_list = []
        for node in open_list:
            fn_list.append(f(node))
        minimum = min(fn_list)
        minimum_index = fn_list.index(minimum)
        
        removed = open_list.pop(minimum_index)
        return removed
    
    def is_in_open_list(swapped):
        swapped_in_open_list = False
        for i in range(len(open_list)):
            if (swapped == open_list[i].numbers):
                swapped_in_open_list = True
                break
    
        return swapped_in_open_list

    def is_in_closed_list(swapped):
        swapped_in_closed_list = False
        for i in range(len(open_list)):
            if (swapped == open_list[i].numbers):
                swapped_in_closed_list = True
                break
        
        return swapped_in_closed_list

    def cur_node_less_g(cur_node):
        # find a duplicate
        duplicate = None
        for node in open_list:
            if (cur_node.numbers == node.numbers):
                duplicate = node
                break
        
        # if there is a duplicate
        if (duplicate):
            if (cur_node.g < duplicate.g):
                return True
        
        return False

    initial_node = PuzzleNode(numbers=numbers, action=None, parent=None)
    open_list = [initial_node]
    closed_list = []
    iterations = 1
    while (len(open_list) != 0):
        # find best node and remove it from openList
        best_node = remove_min_f()
        closed_list.append(best_node)
        if (best_node.numbers == WINNING_NUMBERS):
            actions_list = []  # create an actions list
            while (best_node.parent != None):  # iterate through all of the actions taken
                actions_list.insert(0, best_node.action)  # insert to the first element (to avoid reversing the list)
                best_node = best_node.parent  # go to the parent (previous node)
            
            return actions_list

        zero_row_and_col = search(best_node.numbers, 0)
        z_row = zero_row_and_col[0]
        z_col = zero_row_and_col[1]
        iterations += 1
        print(f"ITERATIONS: {iterations}")

        # swap with top
        try:
            swapped_state = deepcopy(best_node.numbers)  # deepcopy to avoid list references
            if (z_row-1 == -1):
                # print("top not possible")
                pass
            else:
                temp = swapped_state[z_row-1][z_col]
                swapped_state[z_row-1][z_col] = swapped_state[z_row][z_col]
                swapped_state[z_row][z_col] = temp

                swapped_in_open_list = is_in_open_list(swapped_state)
                swapped_in_closed_list = is_in_closed_list(swapped_state)

                puzzle_node = PuzzleNodeAStar(numbers=swapped_state, action='U', parent=best_node)
                puzzle_node.g = distance_from_root(puzzle_node)

                if (not swapped_in_open_list or not swapped_in_closed_list) or (swapped_in_open_list and cur_node_less_g(puzzle_node)):
                    open_list.append(puzzle_node)

        except:
            # print("top error")
            pass

        # swap with right
        try:
            swapped_state = deepcopy(best_node.numbers)  # deepcopy to avoid list references
            if (z_col+1 == 3):
                # print("right not possible")
                pass
            else:
                temp = swapped_state[z_row][z_col+1]
                swapped_state[z_row][z_col+1] = swapped_state[z_row][z_col]
                swapped_state[z_row][z_col] = temp

                swapped_in_open_list = is_in_open_list(swapped_state)
                swapped_in_closed_list = is_in_closed_list(swapped_state)

                puzzle_node = PuzzleNodeAStar(numbers=swapped_state, action='R', parent=best_node)
                puzzle_node.g = distance_from_root(puzzle_node)

                if (not swapped_in_open_list or not swapped_in_closed_list) or (swapped_in_open_list and cur_node_less_g(puzzle_node)):
                    open_list.append(puzzle_node)

        except:
            # print("right error")
            pass

        # swap with bottom
        try:
            swapped_state = deepcopy(best_node.numbers)  # deepcopy to avoid list references

            if (z_row+1 == 3):
                # print("bottom not possible")
                pass
            else:
                temp = swapped_state[z_row+1][z_col]
                swapped_state[z_row+1][z_col] = swapped_state[z_row][z_col]
                swapped_state[z_row][z_col] = temp

                swapped_in_open_list = is_in_open_list(swapped_state)
                swapped_in_closed_list = is_in_closed_list(swapped_state)

                puzzle_node = PuzzleNodeAStar(numbers=swapped_state, action='D', parent=best_node)
                puzzle_node.g = distance_from_root(puzzle_node)

                if (not swapped_in_open_list or not swapped_in_closed_list) or (swapped_in_open_list and cur_node_less_g(puzzle_node)):
                    open_list.append(puzzle_node)


        except:
            # print("bottom error")
            pass

        # swap with left
        try:
            swapped_state = deepcopy(best_node.numbers)  # deepcopy to avoid list references
            if (z_col-1 == -1):
                # print("left not possible")
                pass
            else:
                temp = swapped_state[z_row][z_col-1]
                swapped_state[z_row][z_col-1] = swapped_state[z_row][z_col]
                swapped_state[z_row][z_col] = temp

                swapped_in_open_list = is_in_open_list(swapped_state)
                swapped_in_closed_list = is_in_closed_list(swapped_state)

                puzzle_node = PuzzleNodeAStar(numbers=swapped_state, action='L', parent=best_node)
                puzzle_node.g = distance_from_root(puzzle_node)

                if (not swapped_in_open_list or not swapped_in_closed_list) or (swapped_in_open_list and cur_node_less_g(puzzle_node)):
                    open_list.append(puzzle_node)

        except:
            # print("left error")
            pass
      
# initialize pygame
pygame.init()

# initialize screen
root = tk.Tk()
root.geometry("")
# embed = tk.Frame(root, width = 100, height = 100) #creates embed frame for pygame window
# embed.grid(columnspan = (600), rowspan = 500) # Adds grid
# embed.pack(side = LEFT) #packs window to the left
# os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
# os.environ['SDL_VIDEODRIVER'] = 'windib'
screen = pygame.display.set_mode((300, 500), pygame.RESIZABLE)  # (width, height)
pygame.display.init()
pygame.display.update()
root.update()

# title and icon
pygame.display.set_caption("8-Puzzle Solver")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

# change puzzle file button
file_button = tk.Button(root, text="Choose Puzzle", command=open_file)
file_button.pack()

# numbers array
puzzle_to_load = "puzzle.in"
numbers = load_puzzle_input(puzzle_to_load)
initial_numbers = deepcopy(numbers)
puzzle_is_solvable = is_solvable(initial_numbers)
screen_text = init_screen_text()  # draw in the loop
solution = []  # will contain the solution
solution_index = 0  # used to help in iterating the solution

# button click (bfs)
def click_bfs():
    global numbers
    global solution
    numbers = load_puzzle_input(puzzle_to_load)
    solution = BFSearch(initial_numbers)
    with open("puzzle.out", mode="w") as file:
        sol_str = ""
        for move in solution:
            file.write(f"{move} ")
            sol_str += f"{move} "
    print(solution)
    print(F"PATH: {len(solution)}")

    solution_label = Label(root, text=sol_str, wraplength=250, justify=CENTER)
    solution_label.pack()

# button click (dfs)
def click_dfs():
    global numbers
    global solution
    numbers = load_puzzle_input(puzzle_to_load)
    solution = DFSearch(initial_numbers)
    with open("puzzle.out", mode="w") as file:
        sol_str = ""
        for move in solution:
            file.write(f"{move} ")
            sol_str += f"{move} "
    print(solution)
    print(F"PATH: {len(solution)}")
    
    solution_label = Label(root, text=sol_str, wraplength=250, justify=CENTER)
    solution_label.pack()

# button click (a star)
def click_astar():
    global numbers
    global solution
    numbers = load_puzzle_input(puzzle_to_load)
    solution = ASearch(initial_numbers)
    with open("puzzle.out", mode="w") as file:
        sol_str = ""
        for move in solution:
            file.write(f"{move} ")
            sol_str += f"{move} "
    print(solution)
    print(F"PATH: {len(solution)}")

    solution_label = Label(root, text=sol_str, wraplength=250, justify=CENTER)
    solution_label.pack()

# button click/placeholder (next)
def click_next():
    pass

# initialize buttons
bfs_button = Button(45, 330, "BFS", click_bfs)
dfs_button = Button(45, 380, "DFS", click_dfs)
astar_button = Button(45, 430, "A*", click_astar)
next_button = Button(150, 330, "Next", click_next)

# set up the blocks
def setup_blocks():
    global numbers

    # set up blocks
    blocks_list = []
    initial_x = 40
    initial_y = 40
    for i in range(3):
        for j in range(3):
            block = Block(initial_x, initial_y, numbers[i][j])
            if (block.value == 0):
                zero_block = block  # set the zero block
            blocks_list.append(block)
            initial_x += 80  # go to next item
        initial_x = 40  # reset value of x
        initial_y += 80  # go to next row
    
    return [blocks_list, zero_block]

one_clicked = False  # one of the buttons is clicked

running = True
gameover = False
while running:
    # load the blocks
    blocks_and_zero = setup_blocks()
    blocks = blocks_and_zero[0]
    zero_block = blocks_and_zero[1]

    # screen color (background)
    screen.fill(color=(0,0,100))

    # set up event listeners
    for event in pygame.event.get():
        # close button
        if event.type == pygame.QUIT:
            running = False

        if (not gameover):
            # detect mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if (not one_clicked):
                    # for bfs button
                    if (bfs_button.check_click(event.pos)):
                        one_clicked = True

                if (not one_clicked):
                    # for dfs button
                    if (dfs_button.check_click(event.pos)):
                        one_clicked = True

                if (not one_clicked):
                    # for astar button
                    if (astar_button.check_click(event.pos)):
                        one_clicked = True
                
                # one button is clicked (check solution)
                if (one_clicked):
                    
                    try:
                        file_button.pack_forget()
                    except:
                        pass

                    if (next_button.check_click(event.pos)):
                        try:
                            # test if there are solutions
                            current_action = solution[solution_index]       
                        except:
                            print("NO MORE SOLUTIONS!") 

                        zero_row_and_col = search(numbers, 0)    # search for the zero block's current row and column
                        z_row = zero_row_and_col[0]
                        z_col = zero_row_and_col[1]

                        try:
                            if (solution[solution_index] == 'U'):  # swap up
                                for block in blocks:
                                    if (block.value == numbers[z_row-1][z_col] and z_row-1 != -1):
                                        zero_row_and_col = search(numbers, 0)    # search for the zero block's current row and column
                                        z_row = zero_row_and_col[0]
                                        z_col = zero_row_and_col[1]

                                        print("GO UP")
                                        row_and_col = search(numbers, block.value)    # search for its row and column
                                        row = row_and_col[0]
                                        col = row_and_col[1]
                                        print(f"BEFORE: {numbers}")
                                        temp = numbers[row][col]
                                        numbers[row][col] = numbers[z_row][z_col]
                                        numbers[z_row][z_col] = temp
                                        print(f"AFTER: {numbers}")
                                        zero_block.swap(block)  # swap the blocks
                        except:
                            print("ERROR UP")
                            pass
                              
                        try:
                            if (solution[solution_index] == 'R'):  # swap right
                                for block in blocks:
                                    if (block.value == numbers[z_row][z_col+1] and z_col+1 != 3):
                                        zero_row_and_col = search(numbers, 0)    # search for the zero block's current row and column
                                        z_row = zero_row_and_col[0]
                                        z_col = zero_row_and_col[1]

                                        print("GO RIGHT")
                                        row_and_col = search(numbers, block.value)    # search for its row and column
                                        row = row_and_col[0]    
                                        col = row_and_col[1]
                                        print(f"BEFORE: {numbers}")
                                        temp = numbers[row][col]
                                        numbers[row][col] = numbers[z_row][z_col]
                                        numbers[z_row][z_col] = temp
                                        print(f"AFTER: {numbers}")
                                        zero_block.swap(block)  # swap the blocks
                        except:
                            print("ERROR RIGHT")
                            pass

                        try:
                            if (solution[solution_index] == 'L'):  # swap left
                                for block in blocks:
                                    if (block.value == numbers[z_row][z_col-1] and z_col-1 != -1):
                                        zero_row_and_col = search(numbers, 0)    # search for the zero block's current row and column
                                        z_row = zero_row_and_col[0]
                                        z_col = zero_row_and_col[1]

                                        print("GO LEFT")
                                        row_and_col = search(numbers, block.value)    # search for its row and column
                                        row = row_and_col[0]    
                                        col = row_and_col[1]
                                        print(f"BEFORE: {numbers}")
                                        temp = numbers[row][col]
                                        numbers[row][col] = numbers[z_row][z_col]
                                        numbers[z_row][z_col] = temp
                                        print(f"AFTER: {numbers}")
                                        zero_block.swap(block)  # swap the blocks
                        except:
                            print("ERROR LEFT")
                            pass

                        try:
                            if (solution[solution_index] == 'D'):  # swap down
                                for block in blocks:
                                    if (block.value == numbers[z_row+1][z_col] and z_row+1 != 3):
                                        zero_row_and_col = search(numbers, 0)    # search for the zero block's current row and column
                                        z_row = zero_row_and_col[0]
                                        z_col = zero_row_and_col[1]

                                        print("GO DOWN")
                                        row_and_col = search(numbers, block.value)    # search for its row and column
                                        row = row_and_col[0]    
                                        col = row_and_col[1]
                                        print(f"BEFORE: {numbers}")
                                        temp = numbers[row][col]
                                        numbers[row][col] = numbers[z_row][z_col]
                                        numbers[z_row][z_col] = temp
                                        print(f"AFTER: {numbers}")
                                        zero_block.swap(block)  # swap the blocks    
                        except:
                            print("ERROR LEFT")
                            pass

                        # initialize the path text in gameover
                        if (solution_index == len(solution)-1):
                            PATH_FONT = pygame.font.Font('freesansbold.ttf', 24)
                            path_text = PATH_FONT.render(f"Path Cost: {len(solution)}", True, (255, 255, 255))

                        solution_index += 1
                        print(f"SOLUTION INDEX: {solution_index}")
                        print(numbers)

                # for block (solution not yet clicked/free play)
                if (not one_clicked):
                    for block in blocks:
                        if (block.check_click(event.pos)):  # event.pos is a tuple of mouse click coordinates
                            # check if adjecent to 0
                            number = block.value

                            row_and_col = search(numbers, number)    # search for its row and column
                            row = row_and_col[0]    
                            col = row_and_col[1]

                            zero_row_and_col = search(numbers, 0)    # search for the zero block's current row and column
                            z_row = zero_row_and_col[0]
                            z_col = zero_row_and_col[1]

                            # swap the clicked block and zero block if they are adjacent
                            try:
                                if (numbers[row+1][col]==0):  # below
                                    # print("BELOW")
                                    # print(f"{row_and_col}, ZERO: {zero_row_and_col}")
                                    block.swap(zero_block)
                                    temp = numbers[z_row][z_col]
                                    numbers[z_row][z_col] = numbers[row][col]
                                    numbers[row][col] = temp
                            except:
                                # print("1")
                                pass

                            try:
                                if (numbers[row][col+1]==0):  # right
                                    # print("RIGHT")
                                    # print(f"{row_and_col}, ZERO: {zero_row_and_col}")
                                    block.swap(zero_block)
                                    temp = numbers[z_row][z_col]
                                    numbers[z_row][z_col] = numbers[row][col]
                                    numbers[row][col] = temp
                            except:
                                # print("2")
                                pass
                                
                            try:
                                if (numbers[row-1][col]==0 and not row-1 == -1):  # above (check negative index)
                                    # print("ABOVE")
                                    # print(f"{row_and_col}, ZERO: {zero_row_and_col}")
                                    block.swap(zero_block)
                                    temp = numbers[z_row][z_col]
                                    numbers[z_row][z_col] = numbers[row][col]
                                    numbers[row][col] = temp
                            except:
                                # print("3")
                                pass
                                
                            try:
                                if (numbers[row][col-1]==0 and not col-1 == -1):  # left (check negative index)
                                    # print("LEFT")
                                    # print(f"{row_and_col}, ZERO: {zero_row_and_col}")
                                    block.swap(zero_block)
                                    temp = numbers[z_row][z_col]
                                    numbers[z_row][z_col] = numbers[row][col]
                                    numbers[row][col] = temp
                            except:
                                # print("4")
                                pass
                            
                            # print(numbers)

    # draw the blocks
    for block in blocks:
        block.draw(screen)

    # draw solution buttons
    if (puzzle_is_solvable and not one_clicked and not gameover):
        bfs_button.draw(screen)
        dfs_button.draw(screen)
        astar_button.draw(screen)

    # show solution if one button is clicked
    if (one_clicked and not gameover):
        # SOLUTION_FONT = pygame.font.Font('freesansbold.ttf', 12)
        # solution_text = SOLUTION_FONT.render(f"{solution}", True, (255, 255, 255))
        # screen.blit(solution_text, (20, 20))
        
        next_button.draw(screen)

    # draw screen text (solvable or not)
    if (not gameover):
        draw_screen_text(screen_text, screen)

    # check if game is over
    if (numbers == WINNING_NUMBERS):
        gameover = True
        screen.blit(FONT.render("Gameover!", True, (255, 255, 255)), TEXT_POS)

        # draw the number of path length (only if a solution is clicked)
        try:
            screen.blit(path_text, (45, 330))
        except:
            pass

    # update screen every loop
    pygame.display.update()
    root.update()  # for tkinter
