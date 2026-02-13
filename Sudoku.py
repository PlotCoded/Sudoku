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

# For the last sides: Because without this, the last edges aren't finished
# canvas.create_line((x+1)*widthx, 0, width,height)

# Storing the text for each coord
coords_text = {}

#Attributes for each cell
for x,y in coords:
	coords_text[(x,y)] = [(x*widthx+(widthx/2),y*widthy+(widthy/2)),0,"black"]

#----- Filling in the already filled cells
string_grid = """200170603
050000100
000006079
000040700
000801000
009050000
310400000
005000060
906037002"""

string_grid = string_grid.split("\n")
filled = {} # Cells that are filled before the entire process starts running

# Filling the filled cells with their values
def fill_coords(_):
	for c,v in _.items():
		coords_text[c][1] = v # Updating the text in each cell

# Same here
for r in range(len(string_grid)):
	for c in range(len(string_grid)):
		filled[(c,r)] = int(string_grid[r][c])

# Running that function
fill_coords(filled) #----

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
		# canvas.create_text(pos,text=text,font=("Calibri",40),fill=color)

createText()

def checkingValidity(cell):
	x,y,g = cell[0],cell[1],((cell[0])//3,(cell[1])//3)

	for c in range(9): # Columns
		if c == x: continue
		if canvas.itemcget(coords_text[(c,y)][0],"text") == canvas.itemcget(coords_text[(x,y)][0],"text"):
			return False
	
	for r in range(9): # Rows
		if r == y: continue
		if canvas.itemcget(coords_text[(x,r)][0],"text") == canvas.itemcget(coords_text[(x,y)][0],"text"):
			return False

	# Its grid
	for r in range(3*g[0],(3*g[0])+3):
		for c in range(3*g[1],(3*g[1])+3):
			if (x,y) == (r,c): continue
			if canvas.itemcget(coords_text[(r,c)][0],"text") == canvas.itemcget(coords_text[(x,y)][0],"text"):
				return False
	return True

# Getting each coords possible valid options/numbers
def gettingOptions(cell):
	x,y,g = cell[0],cell[1],((cell[0])//3,(cell[1])//3)

	options = set(n for n in range(1,10))

	for c in range(9): # Columns
		if int(canvas.itemcget(coords_text[(c,y)][0],"text")) > 0 and int(canvas.itemcget(coords_text[(c,y)][0],"text")) in options:
			options.remove(int(canvas.itemcget(coords_text[(c,y)][0],"text")))
	
	for r in range(9): # Rows
		if int(canvas.itemcget(coords_text[(x,r)][0],"text")) >  0 and int(canvas.itemcget(coords_text[(x,r)][0],"text")) in options:
			options.remove(int(canvas.itemcget(coords_text[(x,r)][0],"text")))

	# Its grid
	for r in range(3*g[0],3*g[0]+3):
		for c in range(3*g[1],3*g[1]+3):
			if int(canvas.itemcget(coords_text[(r,c)][0],"text")) == 0 and int(canvas.itemcget(coords_text[(r,c)][0],"text")) in options:
				options.remove(int(canvas.itemcget(coords_text[(r,c)][0],"text")))

	return options

# Getting the options in each cell
coords_options = {}

for r in range(0,9):
	for c in range(0,9):
		if filled[(r,c)] == 0:
			coords_options[(r,c)] = gettingOptions((r,c))
		else:
			coords_options[(r,c)] = {}

incompleted = [True]
completed_version = {}

def incomplete():
	global completed_version
	if incompleted[0] == True:
		for r in range(9):
			for c in range(9):
				if int(canvas.itemcget(coords_text[(r,c)][0],"text")) == 0:
					incompleted[0] = True
					return False
		else:
			incompleted[0] = False
			print("Done")
			for r in range(9):
				for c in range(9):
					completed_version[(r,c)] = int(canvas.itemcget(coords_text[(r,c)][0],"text"))

			print(int(canvas.itemcget(coords_text[(0,0)][0],"text")), int(canvas.itemcget(coords_text[(1,0)][0],"text")), int(canvas.itemcget(coords_text[(2,0)][0],"text")))

# This is my beast, the main Guy in all of this, G-King, the one, it is him
def dfs(node, stack):
	incomplete()

	if incompleted[0]:
		child_nodes = gettingOptions(node)

		for n in child_nodes:
			window.update()
			window.after(0) # Real time viewing

			canvas.itemconfig(coords_text[node][0], text=n)
			canvas.itemconfig(coords_text[node][0], fill="red")

			# Recursion
			def f(node): # Going to the next node if only this node is valid
				global next_node
				if checkingValidity(node):
					next_node = node

					if node[0] <= 8 and node[1] <= 8:
						next_node = (node[0]+1,node[1])
						
						if node[0] >=  8:
							next_node = (0,node[1]+1)

					if node == (8,8): return True
				else:
					return False
				if filled[next_node] > 0:
					return f(next_node)
				return (next_node)

			next_node = f(node)
			if next_node:
				dfs(next_node,stack)

			window.update()
			window.after(0) # Real time viewing

			canvas.itemconfig(coords_text[node][0], text=0)
			canvas.itemconfig(coords_text[node][0], fill="black")

def getStart():
	for r in range(9):
		for c in range(9):
			if canvas.itemcget(coords_text[(c,r)][0],"text") == "0":
				node = (c,r)
				return node

start = getStart()
print(start)
(dfs(start,[]))

for node,val in completed_version.items():
	canvas.itemconfig(coords_text[node][0], text=val)
	canvas.itemconfig(coords_text[node][0], fill="green")

window.mainloop()