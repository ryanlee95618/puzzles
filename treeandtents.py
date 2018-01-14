from puzzleClass import Puzzle, Cell
import inspect
#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()


def e():
	browser.quit()




#open 'root' webpage
browser.set_window_position(590, 0)
url = 'https://www.brainbashers.com/showtents.asp?date=0112&diff=Medium&size=20'
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_id('puzzlediv'))
check_button = browser.find_element_by_xpath("//*[@id='puzzleContainer']/tbody/tr/td/p[2]/a[6]")

def check(cell):
	check_button.click()
	if browser.find_element_by_id("showtext").find_element_by_tag_name("span").get_attribute("class") == "sred":
		asdf

print "Finished Loading Page"

class Trees_Puzzle(Puzzle):
	rows = []
	columns = []
	def __init__(self, array, row_hints, column_hints):

		#store cells and connect them to each other
		self.height = len(array)
		self.width = len(array[0])

		print "setting up puzzle"
		#initiate cells
		for y, row, in enumerate(array):
			for x, element in enumerate(row):
				cell_type = element.find_element_by_tag_name('img').get_attribute("src")[-8:-4]
				if cell_type == "blnk":
					self.cells.append(Grass_Cell(self, y, x))
				elif cell_type == "tree":
					self.cells.append(Tree_Cell(self, y, x))

		print "Initiating Cells Done"
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

		#initiate rows/columns
		for i in range(self.width):
			self.columns.append(Row(self, self.column(i), column_hints[i],i,"column"))
		for i in range(self.height):
			self.rows.append(Row(self, self.row(i), row_hints[i],i,"row"))

class Row():
	def __init__(self, puzzle, cells, hint, y, type):
		self.puzzle = puzzle
		self.cells = cells
		self.index = y
		self.hint = hint
		self.type = type

		if self.type == "row":
			for cell in self.cells:
				cell.row = self
		else:
			for cell in self.cells:
				cell.column = self

	#counts number of cells in a given row or column with a specified state, only use for tent or blanks
	def number_of(self, state):
		return sum([cell.state == state for cell in self.cells if cell.type == "grass"])

	#fill rest of blank cells in a row or column with the specified state
	def fill_in_with(self, state):
		for cell in self.cells:
			if cell.type == "grass" and cell.state == None:
				cell.set_state(state)

	def checkrow(self):
		
		if self.number_of("tent") == self.hint:
			self.fill_in_with("grass")
		
		if self.number_of(None) + self.number_of("tent") == self.hint:
			self.fill_in_with("tent")

		if self.max_tents() + self.number_of("tent") == self.hint:
			for cell_list in self.consecutive_blanks():
				if len(cell_list) % 2 == 1:
					for index, cell in enumerate(cell_list):
						if index%2 == 0:
							cell_list[0].set_state("tent")

				if len(cell_list) >= 2:
					for cell in cell_list:
						for neighbor in cell.neighbors():
							if neighbor not in self.cells and neighbor.type == "grass":
								neighbor.set_state("grass")

				

		if self.max_tents() + self.number_of("tent") == self.hint + 1:

			#look for 2 single blanks space 1 apart. 
			consecutive_blanks = self.consecutive_blanks()
			for index, cell_list in enumerate(consecutive_blanks):
				if index < len(consecutive_blanks) - 1 and len(cell_list) == 1 and len(consecutive_blanks[index+1]) == 1:
					blank1 = cell_list[0]
					blank2 = consecutive_blanks[index+1][0]

					y,x = blank1.y, blank1.x
					if blank2.x == blank1.x + 2:
						middle_cell = self.puzzle.coord(y,x+1)
						if middle_cell.up and middle_cell.up.type == "grass":
							middle_cell.up.set_state("grass")
						if middle_cell.down and middle_cell.down.type == "grass":
							middle_cell.down.set_state("grass")
					elif blank2.y == blank1.y + 2:
						middle_cell = self.puzzle.coord(y+1,x)
						if middle_cell.right and middle_cell.right.type == "grass":
							middle_cell.right.set_state("grass")
						if middle_cell.left and middle_cell.left.type == "grass":
							middle_cell.left.set_state("grass")


			#3 in a row blank
			for cell_list in consecutive_blanks:
				if len(cell_list) == 3:
					for neighbor in cell_list[1].neighbors():
						if neighbor not in self.cells and neighbor.type == "grass":
							neighbor.set_state("grass")


			#search for 2 blank cells that each have one adjacent available tree that are one in the same
			consecutive_blanks = self.consecutive_blanks()
			last_blank_and_tree = []


			for blanks_list in consecutive_blanks:
				if len(blanks_list) == 1:
					avaiable_trees = blanks_list[0].get_avaiable_trees()
					if len(avaiable_trees) == 1:
						if avaiable_trees[0] in last_blank_and_tree:
							blanks = [blanks_list[0], last_blank_and_tree[0]]
							for b in blanks:
								del consecutive_blanks[consecutive_blanks.index([b])]
							for cell_list in consecutive_blanks:
								if len(cell_list) % 2 == 1:
									for index, cell in enumerate(cell_list):
										if index%2 == 0:
											cell_list[0].set_state("tent")
							break	
						else:
							last_blank_and_tree = [blanks_list[0], avaiable_trees[0]]

		if self.max_tents() + self.number_of("tent") == self.hint + 2:

			count = 0
			consecutive_blanks = self.consecutive_blanks()
			last_blank_and_tree = []
			to_delete = []
			for blanks_list in consecutive_blanks:
				if len(blanks_list) == 1:
					avaiable_trees = blanks_list[0].get_avaiable_trees()
					if len(avaiable_trees) == 1:
						if avaiable_trees[0] in last_blank_and_tree:
							blanks = [blanks_list[0], last_blank_and_tree[0]]
							for b in blanks:
								to_delete.append(b)
							count+=1
							last_blank_and_tree = []
						else:
							last_blank_and_tree = [blanks_list[0], avaiable_trees[0]]
			if count == 2:
				for b in to_delete:
					del consecutive_blanks[consecutive_blanks.index([b])]
				for cell_list in consecutive_blanks:
					if len(cell_list) % 2 == 1:
						for index, cell in enumerate(cell_list):
							if index%2 == 0:
								cell_list[0].set_state("tent")







			# for cell in self.cells:
			# 	if cell.state == None:
			# 		avaiable_trees = cell.get_avaiable_trees()
			# 		if len(avaiable_trees) == 1:
			# 			if avaiable_trees[0] in last_blank_and_tree:

			# 				blanks = [cell, last_blank_and_tree[0]]
			# 				# print "found", blanks[0].y, blanks[0].x
			# 				# print [a.state for a in self.cells]
			# 				for blank_cell in blanks:
			# 					for consecutive_blank_cell_list in consecutive_blanks:

			# 						if blank_cell in consecutive_blank_cell_list:
			# 							if len(consecutive_blank_cell_list) == 1:
			# 								del consecutive_blanks[consecutive_blanks.index(consecutive_blank_cell_list)] 
			# 							else:
			# 								return
			# 				for cell_list in consecutive_blanks:
			# 					if len(cell_list) == 1:
			# 						# print cell_list[0].y, cell_list[0].x
			# 						cell_list[0].set_state("tent", False)	
			# 				break									
			# 			else:
			# 				last_blank_and_tree = [cell, avaiable_trees[0]]




	def consecutive_blanks(self):
		blanks = None
		output = []
		for index, cell in enumerate(self.cells):
			if index < len(self.cells)-1 and cell.state == None and self.cells[index+1].state == None:		
				if blanks:
					blanks.append(cell)
				else:
					blanks = [cell, self.cells[index+1]]
			else:

				if blanks:
					output.append(blanks)
				elif cell.state == None:
					output.append([cell])
				blanks = None 
		return output

	#max number of tents that can fit in all the blank cells of a row without adjacent tents
	def max_tents(self):
		return sum([(len(cell_list)+1)/2 for cell_list in self.consecutive_blanks()])



class Tree_Cell(Cell):
	type = "tree"
	def __init__(self, puzzle, y, x):
		self.tent = None
		self.state = "tree"
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None
		self.group = None

	def tally_neighbors(self):
		blank_cells = []
		avaiable_tent_cells = []
		for cell in self.neighbors():
			if cell.type == "grass":
				if cell.state == None:
					blank_cells.append(cell)
				elif cell.state == "tent" and not cell.tree:
					avaiable_tent_cells.append(cell)	
		return [blank_cells, avaiable_tent_cells]	

	def check(self):

		if self.tent:
			return

		blank_cells, avaiable_tent_cells = self.tally_neighbors()

		if len(blank_cells) == 1 and len(avaiable_tent_cells) == 0:
			blank_cells[0].set_state("tent")
			blank_cells[0].connect_to_tree(self)

		if len(blank_cells) == 0 and len(avaiable_tent_cells) == 1:
			avaiable_tent_cells[0].connect_to_tree(self)


		#if a tree has no adjacent tents and only 2 adjacent blanks cells (which are diagonally adjacent to each other)
		#the cells that shares sides with both ajacent blank cells must be grass
		if len(blank_cells) == 2 and len(avaiable_tent_cells) == 0:
			blank_1 = blank_cells[0]
			blank_2 = blank_cells[1]
			if blank_1.x != blank_2.x and blank_1.y != blank_2.y:

				for shared_sides_cell in [puzzle.coord(blank_1.y,blank_2.x), puzzle.coord(blank_2.y,blank_1.x)]:
					if self != shared_sides_cell and shared_sides_cell.type == "grass" and shared_sides_cell.state == None:
						shared_sides_cell.set_state("grass")




class Grass_Cell(Cell):
	type = "grass"
	def __init__(self, puzzle, y, x):

		self.state = None
		self.tree = None
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None
		self.group = None

	def surrounding_8(self):
		y,x = self.y, self.x
		surrounding_cell_coordinates = [[y, x+1], [y, x-1], [y+1, x], [y-1, x], [y+1, x+1], [y+1, x-1], [y-1, x+1], [y-1, x-1]]
		return [self.puzzle.coord(y_prime, x_prime) for y_prime, x_prime in surrounding_cell_coordinates if -1 < x_prime < self.puzzle.width and -1 < y_prime < self.puzzle.height]


	def set_state(self, state, keep_going = True):
		html_cell = table[self.y][self.x]

		if self.state != None:
			return

		if state == 'tent':
			html_cell.click()
			html_cell.click()

			self.state = "tent"

			#fill in surrounding 8 cells with grass if they are blank
			for cell in self.surrounding_8():
				if cell.type == "grass" and cell.state == None:
					cell.set_state("grass", False)
		else: #state == 'grass'
			html_cell.click()
			self.state = "grass"

		if keep_going:
			self.row.checkrow()
			self.column.checkrow()

			for neighbor in self.neighbors():
				neighbor.check()



	def connect_to_tree(self, tree):
		self.tree = tree
		tree.tent = self

	def get_avaiable_trees(self):
		avaiable_trees = []
		for cell in self.neighbors():
			if cell.type == "tree":
				if not cell.tent:
					avaiable_trees.append(cell)
		return avaiable_trees

	def check(self):

		avaiable_trees = self.get_avaiable_trees()

		if self.state == None and len(avaiable_trees) == 0:
			self.set_state("grass")

		elif self.state == "tent" and not self.tree and len(avaiable_trees) == 1:
			self.connect_to_tree(avaiable_trees[0])

			for cell in avaiable_trees[0].neighbors():
				cell.check()




#store html table elements in python 2D-array
html_table = browser.find_element_by_id('puzzlediv')
table = [[html_cell for html_cell in html_row.find_elements_by_tag_name('td')[1:]] for html_row in html_table.find_elements_by_tag_name('tr')[1:]]
column_hints = [int(element.text) for element in html_table.find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1:]]
row_hints = [int(row.find_element_by_tag_name('td').text) for row in html_table.find_elements_by_tag_name('tr')[1:]]

puzzle = Trees_Puzzle(table, row_hints, column_hints)
print "Done Importing Data"

def run():
	i = 1
	while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i < 20:
		print i
		for cell in puzzle.cells:
			cell.check()

		for cell_list in puzzle.rows + puzzle.columns:
			cell_list.checkrow()
		i+=1



run()

check_button.click()
if browser.find_element_by_id("showtext").find_element_by_tag_name("span").get_attribute("class") == "sred":
	asdf

if browser.find_element_by_id("showtext").text.find("Puzzle Solved") != -1:
	pass
	#e()
#create list for each row of the number of consecutive blank squares in a row. most number of tents that 
#can be placed in N consectutive blank cells is N/2 (rounded up) so (N+1)/2








