import inspect
from puzzleClass import Puzzle, Cell
	
#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
browser.set_window_position(750, 0)
browser.set_window_size(600, 735)
url = 'https://www.brainbashers.com/showslitherlink.asp?date=0114&diff=1&size=10'
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




	# 	for cell in self.cells:
	# 		if cell and cell.type == "hint":
	# 			y,x = cell.y, cell.x
	# 			#if cell.y % 2 == 0:
	# 				#connect cell left and right to number cells
	# 			self.connect(y, x, y, x-1)
	# 			self.connect(y, x, y, x+1)
	# 			#elif cell.x % 2 == 0:
	# 				#connect cell up and down to number cells
	# 			self.connect(y, x, y + 1, x)
	# 			self.connect(y, x, y - 1, x)


	# def connect(self, y1, x1, y2, x2):
	# 	cell_1 = self.cells[self.to_index(y1,x1)]
	# 	cell_2 = self.cells[self.to_index(y2,x2)]

	# 	if y1 == y2:
	# 		if x1 > x2:
	# 			cell_1.left = cell_2
	# 			cell_2.right = cell_1				
	# 		else:
	# 			cell_1.right = cell_2
	# 			cell_2.left = cell_1				
	# 	elif x1 == x2:
	# 		if y1 > y2:
	# 			cell_1.up = cell_2
	# 			cell_2.down = cell_1
	# 		else:
	# 			cell_1.down = cell_2
	# 			cell_2.up = cell_1


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

			# check_button.click()
			# if browser.find_element_by_id("showtext").find_element_by_tag_name("span").get_attribute("class") == "sred":
			# 	print "y:", self.y, "x:", self.x, "v:", state, inspect.stack()[1][3]
			# 	asdf


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


#get puzzle info from webpage
html_table = browser.find_element_by_id('slitherlinkdiv')
html_puzzle = [html_row.find_elements_by_tag_name('td') for html_row in html_table.find_elements_by_tag_name('tr')]
puzzle = Slither_Puzzle(html_puzzle)



#find diagonally adjacent 3's



#find adjacent 3's
for c in puzzle.cells:
	if c.type == 'hint' and c.value == "3":
		if c.up.up and c.up.up.value == "3":
			c.up.up.up.set_state(True)
			c.up.set_state(True)
			c.down.set_state(True)
			try:
				c.up.right.right.set_state(False)
				c.up.left.left.set_state(False)
			except:
				pass

		if c.right.right and c.right.right.value == "3":
			c.left.set_state(True)
			c.right.set_state(True)
			c.right.right.right.set_state(True)
			try:
				c.right.up.up.set_state(False)
				c.right.down.down.set_state(False)
			except:
				pass




for c in puzzle.cells:
	if c.type == 'hint' and c.value != "":
		c.check()
	if c.type == 'intersection':
		c.check()

# puzzle.coord(4,1).set_state(False)

# for n in puzzle.coord(2,2).neighbors()[-3:-1]:
# 	n.set_state(True)

# for n in puzzle.coord(3,3).neighbors()[1:2]:
# 	n.set_state(True)


# i = 0
# while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i<20:
# 	for c in puzzle.cells:
# 		pass
# 	i+=1
# print i
