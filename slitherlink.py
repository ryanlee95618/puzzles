import inspect
from puzzleClass import Puzzle, Cell
	
#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
browser.set_window_position(750, 0)
browser.set_window_size(600, 735)
url = 'https://www.brainbashers.com/showslitherlink.asp?date=0115&diff=1&size=15'
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_id('puzzleContainer'))
check_button = browser.find_element_by_xpath("//*[@id='puzzleContainer']/tbody/tr/td/p[4]/a[6]")


def e():
	browser.quit()

class Slither_Puzzle(Puzzle):

	def __init__(self, array):

		#initiate and store cells
		self.height = len(array)
		self.width = len(array[0])
		for y, row, in enumerate(array):
			for x, element in enumerate(row):
				if y % 2 == 1:
					if x % 2 == 1:
						#its a number cell
						self.cells.append(Hint_Cell(self, element, y, x))
					else:
						#relation type cell
						self.cells.append(Link(self, element, y, x))
				else:
					if x % 2 == 1:
						#relation type cell
						self.cells.append(Link(self, element, y, x))
					else:
						#None
						self.cells.append(Intersection(self,element, y, x))

		#connect cells
		for index, cell in enumerate(self.cells):

			y,x = self.to_coordinates(index)
			if not y == 0:
				cell.up = self.cells[self.to_index(y-1, x)]
			if not y == self.height - 1:
				cell.down = self.cells[self.to_index(y + 1, x)]
			if not x == self.width - 1:
				cell.right = self.cells[self.to_index(y, x + 1)]
			if not x == 0:
				cell.left = self.cells[self.to_index(y, x - 1)]

class Link(Cell):
	type = "link"
	def __init__(self, puzzle, html_cell, y, x):
		
		self.state = None
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None

	#only applies to blank cells
	def set_state(self, state):

		if self.state == None:
			self.state = state
			if state:
				html_puzzle[self.y][self.x].click()
			else:
				html_puzzle[self.y][self.x].click()
				html_puzzle[self.y][self.x].click()

			for n in self.neighbors():
				if not n.done:
					n.check()

			# check_button.click()
			# if browser.find_element_by_id("showtext").find_element_by_tag_name("span").get_attribute("class") == "sred":
			# 	print "y:", self.y, "x:", self.x, "v:", state, inspect.stack()[1][3]
			# 	asdf
	def check_closed_loop(self):
		intersection1, intersection2 = [n for n in self.neighbors() if n.type == "intersection"]
		if intersection1 in intersection2.explore():
			self.set_state(False)

class Intersection(Cell):
	type = "intersection"
	

	def __init__(self, puzzle, html_cell, y, x):
		self.done = False
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None

	def check(self):
		n_of_Trues, n_of_Falses, n_of_Nones = self.tally()
		if n_of_Trues == 2:
			for link in self.neighbors():
				if link.state == None:
					link.set_state(False)
			self.done = True
		if n_of_Falses == len(self.neighbors()) - 1:
			for link in self.neighbors():
				if link.state == None:
					link.set_state(False)
			self.done = True

		if n_of_Trues == 1 and n_of_Nones == 1:
			for link in self.neighbors():
				if link.state == None:
					link.set_state(True)
			self.done = True

	def tally(self):
		n_of_Trues = 0
		n_of_Falses = 0
		n_of_Nones = 0
		for link in self.neighbors():
			if link.state == True:
				n_of_Trues += 1
			elif link.state == False:
				n_of_Falses += 1
			else:
				n_of_Nones += 1
		return [n_of_Trues, n_of_Falses, n_of_Nones]

	def connected_neighbors(self):
		output = []
		if self.up and self.up.state == True:
			output.append(self.up.up)
		if self.right and self.right.state == True:
			output.append(self.right.right)
		if self.down and self.down.state == True:
			output.append(self.down.down)
		if self.left and self.left.state == True:
			output.append(self.left.left)
		return output


	def explore(self):
		explored = [False for cell in self.puzzle.cells]
		exploration_list = [self]

		network = [self]
		explored[self.index()] = True

		while len(exploration_list) > 0:

			network_cell = exploration_list.pop()

			for connected_cell in network_cell.connected_neighbors():

				if explored[connected_cell.index()]:
					continue

				exploration_list.append(connected_cell)
				network.append(connected_cell)
				explored[connected_cell.index()] = True

		return network






class Hint_Cell(Cell):
	type = 'hint'
	def __init__(self, puzzle, html_cell, y, x):

		self.done = False
		self.value = html_cell.text
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None

	def number_of(self, state):
		len([link for link in self.neighbors() if link == state])

	def tally(self):
		n_of_Trues = 0
		n_of_Falses = 0
		n_of_Nones = 0
		for link in self.neighbors():
			if link.state == True:
				n_of_Trues += 1
			elif link.state == False:
				n_of_Falses += 1
			else:
				n_of_Nones += 1
		return [n_of_Trues, n_of_Falses, n_of_Nones]

	def check(self):
		if self.value == "":
			return

		n_of_Trues, n_of_Falses, n_of_Nones = self.tally()

		if n_of_Trues + n_of_Nones == int(self.value):
			for link in self.neighbors():
				if link.state == None:
					link.set_state(True)
			self.done = True
		if n_of_Trues == int(self.value):
			for link in self.neighbors():
				if link.state == None:
					link.set_state(False)
			self.done = True

		if n_of_Falses == 4 - int(self.value):
			for link in self.neighbors():
				if link.state == None:
					link.set_state(True)

	def threes(self):
		if self.value == "3":
			pass


#get puzzle info from webpage
html_table = browser.find_element_by_id('slitherlinkdiv')
html_puzzle = [html_row.find_elements_by_tag_name('td') for html_row in html_table.find_elements_by_tag_name('tr')]
puzzle = Slither_Puzzle(html_puzzle)



#check if making a corner would elminiate too many possibilities


#find diagonally adjacent 3's
coords = []
for c in puzzle.cells:
	if c.type == 'hint' and c.value == "3":
		coords.append([c.y,c.x])

for index, coord1 in enumerate(coords[:-1]):
	y1,x1 = coord1
	for y2,x2 in coords[index+1:]:
		if abs(y2-y1) == 2 and abs(x2-x1) == 2:
			cell1 = puzzle.coord(y1,x1)
			cell2 = puzzle.coord(y2,x2)
			if y1 > y2:
				cell1.down.set_state(True)
				cell2.up.set_state(True)
			else:
				cell2.down.set_state(True)
				cell1.up.set_state(True)

			if x1 > x2:
				cell1.right.set_state(True)
				cell2.left.set_state(True)
			else:
				cell2.right.set_state(True)
				cell1.left.set_state(True)



#find adjacent 3's
for c in puzzle.cells:
	if c.type == 'hint' and c.value == "3":
		if c.up.up and c.up.up.value == "3":
			c.up.up.up.set_state(True)
			c.up.set_state(True)
			c.down.set_state(True)
			try:
				c.up.right.right.set_state(False)
			except:
				pass
			try:
				c.up.left.left.set_state(False)
			except:
				pass

		if c.right.right and c.right.right.value == "3":
			c.left.set_state(True)
			c.right.set_state(True)
			c.right.right.right.set_state(True)
			try:
				c.right.up.up.set_state(False)
			except:
				pass
			try:
				c.right.down.down.set_state(False)
			except:
				pass





i = 0
while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i<10:
	for c in puzzle.cells:
		if c.type == 'hint' and c.value != "" and not c.done:

			c.check()
		if c.type == 'intersection' and not c.done:
			c.check()
		if c.type == "link":
			c.check_closed_loop()
	i+=1
print i
