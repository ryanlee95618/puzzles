from puzzleClass import Puzzle, Cell
from selenium import webdriver
browser = webdriver.Chrome()


#open 'root' webpage
browser.set_window_position(320, 0)
url = 'https://www.brainbashers.com/showslant.asp?date=0111&size=15x12'
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_id('slanttable'))

class Slant_Puzzle(Puzzle):

	def __init__(self, array):
		self.height = len(array)
		self.width = len(array[0])
		for y, row, in enumerate(array):
			for x, value in enumerate(row):
				if (y + x) % 2 == 0: #store blank hmtl tabel cells as None

					if y % 2 == 0: #lines alternate between being hint cells and slant cells
						self.cells.append(Hint_Cell(self, value.find_element_by_tag_name("img").get_attribute("src")[39], y, x))
					else:
						self.cells.append(Slant_Cell(self, y, x))
				else:
					self.cells.append(None)

		#set up pointers between each slant cell and 4 surrounding hint cells
		for cell in self.cells:
			if cell and cell.type == "slant":
				y,x = cell.y, cell.x
				self.connect(y,x,y+1,x+1)
				self.connect(y,x,y-1,x-1)
				self.connect(y,x,y+1,x-1)
				self.connect(y,x,y-1,x+1)


	def connect(self, y1, x1, y2, x2):
		cell_1 = self.cells[self.to_index(y1,x1)]
		cell_2 = self.cells[self.to_index(y2,x2)]
		if y1>y2:
			if x1>x2:
				#set y1,y2 up to y2, x2
				cell_1.up = cell_2
				cell_2.down = cell_1
			else:
				cell_1.right = cell_2
				cell_2.left = cell_1
		else:
			if x1>x2:
				cell_1.left = cell_2
				cell_2.right = cell_1
			else:
				cell_1.down = cell_2
				cell_2.up = cell_1

		cell_2.number_of_blanks+=1

class Hint_Cell(Cell):
	type = "hint"
	def __init__(self, puzzle, value, y, x):
		self.value = value
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None
		self.number_of_connections = 0
		self.number_of_nonconnections = 0
		self.number_of_blanks = 0

	def check_connections(self):

		if self.value != "_" and self.number_of_blanks > 0:
			if self.number_of_connections == int(self.value):
				self.set_remaining_blanks("unconnected")
			elif self.number_of_blanks + self.number_of_connections == int(self.value):
				self.set_remaining_blanks("connected")
		else:
			if self.number_of_nonconnections == 3:
				self.set_remaining_blanks("connected")

	def set_remaining_blanks(self, connection_type):
		for slant_cell in self.neighbors():
			if slant_cell.state == "blank":

				connected_direction = "left" if slant_cell.y - slant_cell.x == self.y - self.x else "right"
				unconncected_direction = "right" if connected_direction == "left" else "left"
				slant_cell.set_state(connected_direction if connection_type == "connected" else unconncected_direction)

				for hint_cell in slant_cell.neighbors():
					if hint_cell != self:
						hint_cell.check_connections()

	def connect_slant(self, slant_cell):
		if slant_cell.y - slant_cell.x == self.y - self.x:
			slant_cell.set_state("left")
		else:
			slant_cell.set_state("right")

		for hint_cell in slant_cell.neighbors():
			hint_cell.check_connections()

class Slant_Cell(Cell):
	type = "slant"
	def __init__(self, puzzle, y, x):
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.state = "blank"
		self.up = None
		self.down = None
		self.right = None
		self.left = None

	def set_state(self, direction):
		self.state = direction
		for hint_cell in self.neighbors():
			hint_cell.number_of_blanks -= 1

		if direction == "right":
			rows[self.y][self.x].click()
			rows[self.y][self.x].click()

			self.right.number_of_connections+=1
			self.left.number_of_connections+=1
			self.up.number_of_nonconnections+=1
			self.down.number_of_nonconnections+=1

		elif direction == "left":
			rows[self.y][self.x].click()

			self.up.number_of_connections+=1
			self.down.number_of_connections+=1
			self.right.number_of_nonconnections+=1
			self.left.number_of_nonconnections+=1


#rotate puzzle by 45 degrees

#get puzzle info from webpage
html_table = browser.find_element_by_id('slanttable').find_element_by_tag_name("table")
rows = [html_row.find_elements_by_tag_name('td') for html_row in html_table.find_elements_by_tag_name('tr')]
puzzle = Slant_Puzzle(rows)



for cell in puzzle.cells:
	if cell and cell.type == "hint":
		cell.check_connections()

# if 2 hint cells with value 3 are adjacent (side to side or up and down), the the 2 slant cells that are not shared between them are connected
def neibhoring_threes():
	for cell in puzzle.cells:
		if cell and cell.type == "hint" and cell.value == "3":
			#look to the right
			hint_cell_right = puzzle.cells[puzzle.to_index(cell.y, cell.x + 2)]	
			if hint_cell_right.value == "3":
				print cell.y, cell.x

				for slant_cell in hint_cell_right.neighbors():
					if not slant_cell in cell.neighbors():
						hint_cell_right.connect_slant(slant_cell)
				for slant_cell in cell.neighbors():
					if not slant_cell in hint_cell_right.neighbors():
						cell.connect_slant(slant_cell)


			#look down
			hint_cell_down = puzzle.cells[puzzle.to_index(cell.y+2, cell.x)]
			if hint_cell_down.value == "3":
				pass


def neighboring_hint_cells(hint_cell):
	output = []
	if hint_cell.up:
		if hint_cell.up.state == "left":
			output.append(hint_cell.up.up)
	if hint_cell.down:
		if hint_cell.down.state == "left":
			output.append(hint_cell.down.down)

	if hint_cell.right:
		if hint_cell.right.state == "right":
			output.append(hint_cell.right.right)
	if hint_cell.left:
		if hint_cell.left.state == "right":
			output.append(hint_cell.left.left)
	return output


def are_connected(h1, h2):
	explored = [False for cell in puzzle.cells]

	need_to_explore = [h1]

	while len(need_to_explore) > 0:
		hint_cell = need_to_explore.pop()

		explored[hint_cell.index()] = True

		for hint_neighbor in neighboring_hint_cells(hint_cell):

			if hint_neighbor == h2:
				return True

			if not explored[hint_neighbor.index()]:
				need_to_explore.append(hint_neighbor)


def find_closed_loop():
	for cell in puzzle.cells:
		if cell and cell.type == "slant" and cell.state == "blank":

			if are_connected(cell.up, cell.down):
				cell.set_state("right")

				for hint_cell in cell.neighbors():
					hint_cell.check_connections()

			elif are_connected(cell.right, cell.left):
				cell.set_state("left")
				for hint_cell in cell.neighbors():
					hint_cell.check_connections()

print "no closed loops"

i = 0
while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i<10:
	find_closed_loop()
	i+=1



def exit():
	browser.quit()
