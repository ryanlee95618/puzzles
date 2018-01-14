#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()
from puzzleClass import Puzzle, Cell

#open 'root' webpage
browser.set_window_position(320, 0)
url = 'https://www.brainbashers.com/showhitori.asp?date=1228&size=9&diff=2'
browser.get(url) 
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_id('puzzlediv'))

class Hitory_Puzzle(Puzzle):
	def __init__(self, array):

		self.height = len(array)
		self.width = len(array[0])
		for y, row, in enumerate(array):
			for x, value in enumerate(row):
				self.cells.append(Hitori_Cell(self, value.text, y, x))

		for index, cell in enumerate(self.cells):

			y,x = self.to_coordinates(index)
			if not y == 0:
				cell.up = self.cells[self.to_index(y - 1, x)]
			if not y == self.height - 1:
				cell.down = self.cells[self.to_index(y + 1, x)]
			if not x == self.width - 1:
				cell.right = self.cells[self.to_index(y, x + 1)]
			if not x == 0:
				cell.left = self.cells[self.to_index(y, x - 1)]

class Hitori_Cell(Cell):
	
	def __init__(self, puzzle, value, y, x):
	    self.value = value
	    self.puzzle = puzzle
	    self.y = y
	    self.x = x
	    self.state = "grey"
	    self.up = None
	    self.down = None
	    self.right = None
	    self.left = None

	def set_state(self, color):
		if self.state != "grey":
			return None
		if color == "white":
			html_puzzle[self.y][self.x].click()
			self.state = "white"
			for cell in self.column():
				if cell.value == self.value:
					cell.set_state("black")
			for cell in self.row():
				if cell.value == self.value:
					cell.set_state("black")
		elif color == "black":
			html_puzzle[self.y][self.x].click()
			html_puzzle[self.y][self.x].click()
			self.state = "black"
			for cell in self.neighbors():
				cell.set_state("white")			





#get puzzle info from webpage
html_puzzle = [html_row.find_elements_by_tag_name('td') for html_row in browser.find_element_by_id('puzzlediv').find_elements_by_tag_name('tr')]
puzzle = Hitory_Puzzle(html_puzzle)
	
#a cell between 2 cells with same value must be white
for cell in puzzle.cells:
	if cell.right and cell.left:
		if cell.right.value == cell.left.value:
			cell.set_state("white")
	if cell.up and cell.down:
		if cell.up.value == cell.down.value:
			cell.set_state("white")



#if there 3 numbers in the same row, and 2 of them are adjacent, the 3rd must be black
#find for 2 adjacent numbers, search for a 3rd and set it to black 
for cell in puzzle.cells:
	if cell.right and cell.right.value == cell.value:
		for row_cell in cell.row():
			if row_cell != cell and row_cell != cell.right:
				if row_cell.value == cell.value:
					row_cell.set_state("black")
	if cell.down and cell.down.value == cell.value:
		for column_cell in cell.column():
			if column_cell != cell and column_cell != cell.down:
				if column_cell.value == cell.value:
					column_cell.set_state("black")


print "TESTING CONNECTEDNESS"
#Any White square can be reached from any other (i.e. they are connected).

changes_made = True

while changes_made:
	changes_made = False

	for cell in puzzle.cells:
		if cell.state != "white":
			continue

		#count number of grey and white neighbors,
		grey_neighbors = []
		white_neighbors = []

		for neighbor in cell.neighbors():
			if neighbor.state == "grey":
				grey_neighbors.append(neighbor)
			elif neighbor.state == "white":
				white_neighbors.append(neighbor)

		#with 1 grey and 0 white neighbors, the only way for cell to be connected to rest of puzzle is thought the grey neightbor
		if len(grey_neighbors) == 1 and len(white_neighbors) == 0:
			grey_neighbors.pop().set_state("white")
			changes_made = True


print "3"
#find all grey neighbors the can be reached by traveling over white cells
#if there is only one grey neightbor it must be white to ensure connectedness
def test_connectedness(cell):

	#keep track of which cells have been explored
	explored = [False]*(puzzle.width*puzzle.height)

	to_explore = [cell]
	grey_neighbors = []

	while len(to_explore) > 0:

		cell = to_explore.pop()
		explored[cell.index()] = True

		for neighbor in cell.neighbors():

			if not explored[neighbor.index()]:

				if neighbor.state == "white":
					to_explore.append(neighbor)
				elif neighbor.state == "grey":
					if not neighbor in grey_neighbors: #why is this necessary?!
						grey_neighbors.append(neighbor)

	if len(grey_neighbors) == 1:
		grey_neighbors.pop().set_state("white")


while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1:
	for cell in puzzle.cells:
		if cell.state == "grey":
			for neighbor in cell.neighbors():
				if neighbor.state == "white":
					test_connectedness(neighbor)



browser.close()
