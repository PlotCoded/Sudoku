# This script is the no animation sudoku solver: Much faster but goes straight to the point
import customtkinter as ctk, random, math

width,height = 600,600
window = ctk.CTk()
window.geometry(f"{width}x{height}")
window.title("Sudoku")

# Canvas 
canvas = ctk.CTkCanvas()
canvas.pack(expand=True,fill="both")

# Grid sides
grid_sides = 9

# Sudoku Grid
# Cells coords
coords = tuple((x,y) for x in range(grid_sides) for y in range(grid_sides))

# Grid lines
widthx,widthy = width/grid_sides,height/grid_sides
for x,y in coords:
	canvas.create_rectangle(x*widthx,y*widthy,widthx,widthy) # Creating the grid

# Storing the text for each coord
coords_text = {}

#----- Filling in the already filled cells: This is your input grid
string_grid = """000000080
800701040
040020030
374000900
000030000
005000321
010060050
050802006
080000000
"""

string_grid = string_grid.split("\n")
string_grid = [[int(b) for b in a if not b == "\n"] for a in string_grid]
fills = {} # Cells that are filled before the entire process starts running
grid_and_values = {} # Turning the text format of the grid into a dictionary format for easier usage

# Filling the filled cells with their values
for r in range(9):
	for c in range(9):
		value = string_grid[r][c]
		
		fills[(c,r)] = value

coords = tuple((x,y) for x in range(grid_sides) for y in range(grid_sides))
coords_text = {}

# Attributes for each cell
for c,v in fills.items():
	coords_text[c] = [(c[0]*widthx+(widthx/2),c[1]*widthy+(widthy/2)),v,"black"]

def createText():
	# Creating the text for each coord cell
	for x,y in coords:
		pos = coords_text[(x,y)][0]
		text = coords_text[(x,y)][1]
		color = coords_text[(x,y)][2]

		if text > 0:
			color = "blue"
		else:
			color = "black"

		text_id = canvas.create_text(
            pos,
            text=text,
            font=("Calibri",40),
            fill=color
        )

		coords_text[(x,y)] = [text_id]

createText()

def checkingValidity(cell):
	x,y,g = cell[0],cell[1],((cell[0])//3,(cell[1])//3)

	for c in range(9): # Columns
		if c == x: continue
		if fills[(c,y)] == fills[(x,y)]:
			return False
	
	for r in range(9): # Rows
		if r == y: continue
		if fills[(x,r)] == fills[(x,y)]:
			return False

	# Its grid
	for r in range(3*g[0],(3*g[0])+3):
		for c in range(3*g[1],(3*g[1])+3):
			if (x,y) == (r,c): continue
			if fills[(r,c)] == fills[(x,y)]:
				return False
	return True

# Getting each coords possible valid options/numbers
def gettingOptions(cell):
	x,y,g = cell[0],cell[1],((cell[0])//3,(cell[1])//3)

	options = set(n for n in range(1,10))

	for c in range(9): # Columns
		if fills[(c,y)] > 0 and fills[(c,y)] in options:
			options.remove(fills[(c,y)])
	
	for r in range(9): # Rows
		if fills[(x,r)] >  0 and fills[(x,r)] in options:
			options.remove(fills[(x,r)])

	# Its small grid stuff
	for r in range(3*g[0],3*g[0]+3):
		for c in range(3*g[1],3*g[1]+3):
			if fills[(r,c)] == 0 and fills[(x,y)] in options:
				options.remove(fills[(r,c)])

	return options

incompleted = [True]
completed_version = {}

def incomplete():
	if incompleted[0] == True:
		for r in range(9):
			for c in range(9):
				if fills[(r,c)]== 0:
					incompleted[0] = True
					return False
		else:
			incompleted[0] = False
			print("Done")
			for r in range(9):
				for c in range(9):
					completed_version[(r,c)] = fills[(r,c)]

			print(fills[(0,0)], fills[(1,0)], fills[(2,0)]) # Can you guess why I need the first 3 cells?

# This is my beast, the main Guy in all of this, G-King, the one, it is him
def dfs(node, stack):
	incomplete()

	if incompleted[0]:
		options = gettingOptions(node)

		# print(node,options)
		for n in options:
			window.update()
			window.after(0) # Real time viewing

			fills[node] = n

			# Recursion
			def f(node): # Going to the next node if only this node is valid
				if checkingValidity(node):
					next_node = node

					if node[0] <= 8 and node[1] <= 8:
						next_node = (node[0]+1,node[1])
						
						if node[0] >=  8:
							next_node = (0,node[1]+1)
					if node == (8,8): return True
				else:
					return False

				if fills[next_node] > 0:
					return f(next_node)
				return next_node

			next_node = f(node)
			if next_node:
				dfs(next_node,stack)

			window.update()
			window.after(0) # Real time viewing

			fills[node] = 0

def getStart():
	for r in range(9):
		for c in range(9):
			if fills[(c,r)] == 0:
				node = (c,r)
				return node

start = getStart()

dfs(start,[])

for c,v in completed_version.items():
	canvas.itemconfig(coords_text[c][0], text=v)
	canvas.itemconfig(coords_text[c][0], fill="green")

window.mainloop()