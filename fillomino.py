import inspect

from puzzleClass import Puzzle, Cell
	
#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
browser.set_window_position(590, 0)
url = 'https://www.brainbashers.com/showfillomino.asp?date=0105&size=16'
url = "https://www.brainbashers.com/showfillomino.asp?date=0112&size=16"
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_id('puzzlediv'))
check_button = browser.find_element_by_xpath("//*[@id='puzzleContainer']/tbody/tr/td[2]/p[2]/a[6]")

stop = True

def e():
	browser.quit()



class Fillomino_Puzzle(Puzzle):

	groups = []
	def __init__(self, array):

		#store cells and connect them to each other
		self.height = len(array)
		self.width = len(array[0])
		for y, row, in enumerate(array):
			for x, value in enumerate(row):
				self.cells.append(Number_Cell(self, value, y, x))

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

		self.calculate_groups()

	#set up groups
	def calculate_groups(self):
		for cell in self.cells:
			if cell.group == None:
				self.groups.append(Group(self, cell))
	
	def delete_group(self, group):
		del self.groups[self.groups.index(group)]

class Group:

	type = "group"

	def __init__(self, puzzle, starting_cell):

		self.starting_cell = starting_cell
		self.value = starting_cell.value
		self.puzzle = puzzle
		self.calculate_group_cells()


	#return list of all cells with same value reachable from starting cell by traveling to adjacent cells of same value
	#keep track of neighboring cells encoutered.
	def calculate_group_cells(self):

		explored = [False for cell in self.puzzle.cells]
		exploration_list = [self.starting_cell]
		neighbors = []

		group = [self.starting_cell]
		explored[self.starting_cell.index()] = True

		while len(exploration_list) > 0:

			group_cell = exploration_list.pop()

			for adjacent_cell in group_cell.neighbors():

				if explored[adjacent_cell.index()]:
					continue

				if adjacent_cell.value == self.value:
					exploration_list.append(adjacent_cell)
					group.append(adjacent_cell)
					explored[adjacent_cell.index()] = True

				else:
					neighbors.append(adjacent_cell)
					explored[adjacent_cell.index()] = True

		self.cells = group
		self.neighbors = neighbors
		self.size = len(self.cells)

		for cell in self.cells:
			cell.group = self

	def adjacent_groups(self):
		groups = []
		for neighbor in self.neighbors:
			if not neighbor.group in groups:
				groups.append(neighbor.group)
		return groups		

	#return list of groups of white spaces adjacent to group, no repeats 
	def adjacent_blank_groups(self):
		return [group for group in self.adjacent_groups() if group.value == None]

		# groups = []
		# for neighbor in self.neighbors:
		# 	if neighbor.value == None and not neighbor.group in groups:
		# 		groups.append(neighbor.group)
		# return groups


	#list of all blank cells that a group can expand into
	def expansion_space(self):
		#return [cell for group in [group.cells for group in self.adjacent_blank_groups()] for cell in group]
		explored = [False for cell in self.puzzle.cells]
		exploration_list = [self.starting_cell]
		#neighbors = []

		group = [self.starting_cell]
		explored[self.starting_cell.index()] = True

		while len(exploration_list) > 0:

			group_cell = exploration_list.pop()

			for adjacent_cell in group_cell.neighbors():

				if explored[adjacent_cell.index()]:
					continue

				if adjacent_cell.value == self.value or adjacent_cell.value == None:
					exploration_list.append(adjacent_cell)
					group.append(adjacent_cell)
					explored[adjacent_cell.index()] = True

				else:
					#neighbors.append(adjacent_cell)
					explored[adjacent_cell.index()] = True
		return group


	def too_large(self):
		if self.size + 1 == self.value:
			allowed = []
			for cell in self.neighbors:
				if cell.value == None:
					cell.set_value(self.value, True)

					if not cell.group.size > cell.value:
						allowed.append(cell)

					cell.set_value(None, True)
			if len(allowed) == 1:
				allowed[0].set_value(self.value, False, False)


	# def fill_expansion_space(self):
	# 	blank_cells = self.expansion_space()
	# 	if len(blank_cells) + self.size == self.value:
	# 		for cell in blank_cells:
	# 			cell.set_value(self.value)

	#if group size requirment not yet met and the group has only one neighboring blank cell
	#set blank cells value to groups value
	def one_blank_cell_to_expand_to(self, keep_going):
		if self.value != None and self.size < self.value:
			blank_neighbors = [cell for cell in self.neighbors if cell.value == None]
			if len(blank_neighbors) == 1:
				blank_neighbors[0].set_value(self.value, False, keep_going)
				return True		


	#if group of blank cells has only one neighbor whose hint has not been fufullied
	#set all blank cells to that neighbor's value
	def one_possible_value(self):
		if self.value == None:
			potential_values = [cell.value for cell in self.neighbors if cell.unfufilled()]
			if len(set(potential_values)) == 1:
				for cell in self.cells:
					cell.set_value(potential_values[0])



class Number_Cell(Cell):
	type = "number"
	def __init__(self, puzzle, value, y, x):
		try:
			self.value = int(value)
		except:
			self.value = None
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None
		self.group = None

	#only applies to blank cells
	def set_value(self, value, testing = False, keep_going = True):
		
		if not testing:
			#update html puzzle
			number_selector[value].click()
			html_puzzle[self.y][self.x].click()

			# check_button.click()
			# if browser.find_element_by_id("showtext").find_element_by_tag_name("span").get_attribute("class") == "sred" and stop:
			# 	print "y:", self.y, "x:", self.x, "v:", value, inspect.stack()[1][3]
			# 	asdf

		#update puzzle model
		self.value = value

		for neighbor in self.neighbors():
			try:
				group = neighbor.group
		
				for cell in group.cells:
					cell.group = None
				self.puzzle.delete_group(group)
				del group
			except:		
				pass	

		self.puzzle.calculate_groups()

		if not testing and stop and keep_going:
			for cell in self.group.neighbors+[self]:
				cell.group.one_possible_value()
				#cell.group.one_blank_cell_to_expand_to()
				cell.test_cut_off()

	#group size requirement has not yet been met
	def unfufilled(self):
		return self.group.size != self.value

	#if a blank cell has 2 neighbors with the same value, 
	#see if joining the 2 neighbors groups would violate group size requirment
	#if so see if eliminated that option from either of 2 neighbor's group expansions results in changes

	def too_large(self):
		if self.value != None:
			return None

		neighbors = [neighbor for neighbor in self.neighbors() if neighbor.value != None]

		for neighborX in neighbors:
			for neighborY in neighbors:
				if neighborX != neighborY and neighborX.value == neighborY.value:
					self.set_value(neighborX.value, True)

					if self.group.size > self.group.value:

						self.set_value(0, True)
						# for neighbor in neighborX.group.neighbors + neighborY.group.neighbors:
						# 	neighbor.test_cut_off(False)



						neighborX.group.one_blank_cell_to_expand_to(False)
						neighborY.group.one_blank_cell_to_expand_to(False)

		self.set_value(None, True)		


			



 	def test_cut_off(self, keep_going = True):

		#look at blank cell, temporary set value to "Test" get adjacent blank groups
		if self.value != None:
			return
		self.set_value(10, True)

		#get of small blank space groups
		blank_groups = [g for g in self.group.adjacent_blank_groups() if g.size < 8]

		for group in blank_groups:

			#find the all neighbors with unfufilled hints of the blank space group
			unfufilled_neighbors = [cell for cell in group.neighbors if cell != self and cell.unfufilled()]


			for unfufilled_neighbor in unfufilled_neighbors:
				if len(unfufilled_neighbor.group.expansion_space()) < unfufilled_neighbor.value:			
					self.set_value(unfufilled_neighbor.value, False, keep_going)
					return True

		
		for cell in self.neighbors():
			if cell.value != None and cell.unfufilled():
				if len(cell.group.expansion_space()) < cell.value:			
					self.set_value(cell.value, False, keep_going)
					return True

		else:
			self.set_value(None, True)
			return





#get puzzle info from webpage
html_table = browser.find_element_by_id('puzzlediv')
html_puzzle = [html_row.find_elements_by_tag_name('td') for html_row in html_table.find_elements_by_tag_name('tr')]
table_rows = [[html_cell.text for html_cell in html_row.find_elements_by_tag_name('td')] for html_row in html_table.find_elements_by_tag_name('tr')]
number_selector = [html_row.find_element_by_tag_name('td') for html_row in browser.find_element_by_id("numberdiv").find_elements_by_tag_name("tr")]
puzzle = Fillomino_Puzzle(table_rows)


i = 0
while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i<20:
	print i
	for cell in puzzle.cells:
		cell.test_cut_off()
		cell.too_large()
		cell.group.one_possible_value()
		cell.group.too_large()
	i+=1

print i
