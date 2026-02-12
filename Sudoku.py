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
	# text_id = canvas.create_text(
    #         (x*widthx+(widthx/2),y*widthy+(widthy/2)),
    #         text=random.randint(0,9),
    #         font=("Calibri",40),
    #         fill="black"
    #     )
	coords_text[(x,y)] = [(x*widthx+(widthx/2),y*widthy+(widthy/2)),random.randint(0,9),"black"]

#----- Filling in the already filled cells
string_grid = """030050040
008010500
460000012
070502080
000603000
040109030
250000098
001020600
080060020"""

string_grid = string_grid.split("\n")
filled = {}

# Filling the filled cells with their values
def fill_coords(cell_vals):
	for c,v in cell_vals.items():
		coords_text[c][1] = v

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

		coords_text[(x,y)] = [pos,text,color,text_id]
		# canvas.create_text(pos,text=text,font=("Calibri",40),fill=color)

createText()

def checkingValidity(cell):
	x,y,g = cell[0],cell[1],((cell[0])//3,(cell[1])//3)

	for c in range(9): # Columns
		if c == x: continue
		if coords_text[(c,y)][1] == coords_text[(x,y)][1]:
			# print(coords_text[(c,y)][1],coords_text[(x,y)][1],"column")
			return False
	
	for r in range(9): # Rows
		if r == y: continue
		if coords_text[(x,r)][1] == coords_text[(x,y)][1]:
			# print(coords_text[(x,r)][1],coords_text[(x,y)][1],"row")
			return False

	# Its grid
	for r in range(3*g[0],(3*g[0])+3):
		for c in range(3*g[1],(3*g[1])+3):
			if (x,y) == (r,c): continue
			if coords_text[(r,c)][1] == coords_text[(x,y)][1]:
				# print(coords_text[(r,c)][1],coords_text[(x,y)][1],x,y,r,c,"both")
				return False
	return True

# Getting each coords possible valid options/numbers
def gettingOptions(cell):
	x,y,g = cell[0],cell[1],((cell[0])//3,(cell[1])//3)

	options = set(n for n in range(1,10))

	for c in range(9): # Columns
		if coords_text[(c,y)][1] > 0 and coords_text[(c,y)][1] in options:
			options.remove(coords_text[(c,y)][1])
	
	for r in range(9): # Rows
		if coords_text[(x,r)][1] >  0 and coords_text[(x,r)][1] in options:
			options.remove(coords_text[(x,r)][1])

	# Its grid
	for r in range(3*g[0],3*g[0]+3):
		for c in range(3*g[1],3*g[1]+3):
			if coords_text[(r,c)][1] == 0 and coords_text[(r,c)][1] in options:
				options.remove(coords_text[(r,c)][1])

	return options

# Getting the options in each cell
coords_options = {}

for r in range(0,9):
	for c in range(0,9):
		if filled[(r,c)] == 0:
			coords_options[(r,c)] = gettingOptions((r,c)) #print
		else:
			coords_options[(r,c)] = {}

def incomplete():
	for r in range(9):
		for c in range(9):
			if coords_text[(r,c)][1] == 0:
				return True
	else:
		return False
# This is my beast, the main Guy in all of this, G-King, the one, it is him
def dfs(node, stack):
	for r in range(9):
		if not coords_text[(r,8)][1] > 0:
			break
	else:
		return [coords_text[(0,0)][1],coords_text[(1,0)][1], coords_text[(2,0)][1]]

	child_nodes = coords_options[node]

	for n in child_nodes:
		coords_text[node][1] = n

		pos = coords_text[node][0]
		text = coords_text[node][1]
		color = "red"

		window.update()
		window.after(0) # Real time viewing

		canvas.itemconfig(coords_text[node][3], text=n)
		canvas.itemconfig(coords_text[node][3], fill="red")

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
				# print(coords_text[(0,0)][1],coords_text[(1,0)][1], coords_text[(2,0)][1])
				# print(next_node,"hsohconsodc")
			else:
				return False
			if filled[next_node] > 0:
				return f(next_node)
			return (next_node)

		next_node = f(node)
		if next_node:
			try:
				dfs(next_node,stack)
			except:
				print("Done")
				return False
	else:
		coords_text[node][1] = 0

		pos = coords_text[node][0]
		text = coords_text[node][1]
		color = "black"

		window.update()
		window.after(0) # Real time viewing

		canvas.itemconfig(coords_text[node][3], text=0)
		canvas.itemconfig(coords_text[node][3], fill=color)

print(dfs((0,0),[]))
# print(coords_options)

# # Creating binding and functionality
# # Getting the cell you are on when you click on a cell
# def click(event):
# 	canvas.focus_set()
# 	x,y = event.x,event.y
# 	x,y = math.floor(x/widthx),math.floor(y/widthy)

# 	if (x,y) not in coords: return None
# 	# Changing the text color to info the user it had been clicked
# 	pos = coords_text[(x,y)][0]
# 	text = coords_text[(x,y)][1]
# 	color = "green"
	
# 	print("click")

# 	canvas.create_text(pos,text=text,font=("Calibri",40),fill=color)

# # Changing the color when you unclick it
# def unclick(event):
# 	x,y = event.x,event.y
# 	x,y = math.floor(x/widthx),math.floor(y/widthy)

# 	if (x,y) not in coords: return None

# 	# Changing the text color to info the user it had been clicked
# 	pos = coords_text[(x,y)][0]
# 	text = coords_text[(x,y)][1]
# 	if text > 0:
# 		color = "blue"
# 	else:
# 		color = "black"

# 	print("unclick")
# 	canvas.create_text(pos,text=text,font=("Calibri",40),fill=color)

# canvas.bind("<KeyPress-Left>",click)
# canvas.bind("<ButtonRelease>",unclick)

window.mainloop()