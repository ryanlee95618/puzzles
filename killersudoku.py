import inspect
from puzzleClass import Puzzle, Cell
	
#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
browser.set_window_position(590, 0)
url = 'https://www.brainbashers.com/showkillersudoku.asp?date=0109&diff=1'
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_class_name('sudokutable'))
check_button = browser.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/p[2]/a[6]")

def e():
	browser.quit()



class Killer_Puzzle(Puzzle):

	groups = []
	
	def __init__(self, array):

		#store cells and connect them to each other
		self.height = len(array)
		self.width = len(array)
		for y, row, in enumerate(array):
			for x, element in enumerate(row):
				self.cells.append(Number_Cell(self, element.get_attribute("style")[18:36], y, x))


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
			html_cell = table_rows[cell.y][cell.x]
			if has_clue(html_cell):
				self.groups.append(Group(self, cell, get_clue(html_cell)))


	def columns(self):
		return [self.column(i) for i in range(self.width)]

	def rows(self):
		return [self.row(i) for i in range(self.height)]

	def square(self, y, x):
		output = []
		for y1 in range((y/3)*3, (y/3+1)*3):
			for x1 in range((x/3)*3, (x/3+1)*3):
				output.append(self.coord(y1, x1))
		return output

	def squares(self):
		output = []
		for y in range(0,9,3):
			for x in range(0,9,3):
				output.append(self.square(y,x))
		return output

class Group:

	type = "group"

	def __init__(self, puzzle, starting_cell, total):

		self.starting_cell = starting_cell
		self.color = starting_cell.color
		self.puzzle = puzzle
		self.total = total
		self.calculate_group_cells()


		for cell in self.cells:
			cell.set_value("".join([str(n) for n in sum_to2(self.total, len(self.cells))]))


	#return list of all cells with same value reachable from starting cell by traveling to adjacent cells of same value
	#keep track of neighboring cells encoutered.
	def calculate_group_cells(self):

		explored = [False for cell in self.puzzle.cells]
		exploration_list = [self.starting_cell]

		group = [self.starting_cell]
		explored[self.starting_cell.index()] = True

		while len(exploration_list) > 0:

			group_cell = exploration_list.pop()
			for adjacent_cell in group_cell.neighbors():

				if explored[adjacent_cell.index()]:
					continue

				if adjacent_cell.color == self.color:
					exploration_list.append(adjacent_cell)
					group.append(adjacent_cell)
					explored[adjacent_cell.index()] = True

				else:
					explored[adjacent_cell.index()] = True

		self.cells = group
		self.size = len(self.cells)

		for cell in self.cells:
			cell.group = self

	def check_pairs(self):
		if len(self.cells) == 2:
			for cell1, cell2 in [self.cells, self.cells[::-1]]:
				for v1 in cell1.value:
					valid = False
					for v2 in cell2.value:
						if int(v1) + int(v2) == self.total:
							valid = True
					if not valid:
						cell1.delete_value(v1)
	def one_unknown(self):
		unknown = []
		for cell in self.cells:
			if len(cell.value) > 1:
				unknown.append(cell)
		if len(unknown) == 1:
			partial = sum([int(cell.value) for cell in self.cells if cell!= unknown[0]])
			unknown[0].set_value(str(self.total - partial))



class Number_Cell(Cell):
	type = "number"
	def __init__(self, puzzle, color, y, x):

		self.value = None
		self.color = color
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None
		self.group = None

	#only applies to blank cells
	def set_value(self, value):
		html_cell = table_rows[self.y][self.x]
		html_cell.find_element_by_tag_name("input").clear()
		html_cell.find_element_by_tag_name("input").send_keys(str(value))

		self.value = value

	def delete_value(self, value):
		for character in value:
			if character in self.value:
				new_value = self.value.replace(character, "")
				self.value = new_value
				self.set_value(new_value)



		# check_button.click()
		# if browser.find_element_by_id("showtext").find_element_by_tag_name("span").get_attribute("class") == "sred":
		# 	print "y:", self.y, "x:", self.x, "v:", value, inspect.stack()[1][3]
		# 	asdf

	#if a cell has only one value left, delete that value from other cells in row and column
	def one_value(self):
		if len(self.value) == 1:
			for cell in self.row() + self.column():
				if cell != self:
					cell.delete_value(self.value)

integers = [1,2,3,4,5,6,7,8,9]
def sum_to2(total, N, integer_list = integers):

	if N == 0:
		return used(integer_list) if total == 0 else False

	else:
		output = []
		for n in integer_list:
			copy = list(integer_list)
			del copy[copy.index(n)]
			answer = sum_to2(total - n, N - 1, copy)
			if answer:
				output+=answer
	output.sort()
	return list(set(output))

#return list of numbers that have been deleted given a list of numbers
def used(array):
	copy = list(integers)
	for n in array:
		del copy[copy.index(n)]
	return copy



#search all rows/columns for subgroups of sizes 2 through 4 inclusive.
# a subgroup is a set of N cells with a total of N combined possible values
def search_for_subgroups():
	for number_cells in puzzle.rows() + puzzle.columns() + puzzle.squares():
		for N in range(2,5):
			short_list = [cell for cell in number_cells if len(cell.value) <= N]
			groups = combination(short_list, N)
			for group in groups:
				all_possible_values = set(list("".join([cell.value for cell in group])))
				if len(all_possible_values) == N:
					for cell in number_cells:
						if cell not in group:
							cell.delete_value("".join(list(all_possible_values)))

		#if there is only 1 possible location for a number in a row, column or square, set that cells value to that number.
		for n in integers:
			cells_with_n = [cell for cell in number_cells if str(n) in cell.value]
			if len(cells_with_n) == 1:
				if len(cells_with_n[0].value) > 1:
					cells_with_n[0].set_value(str(n))
					cells_with_n[0].one_value()




def combination(list, N):
	output = []
	if N == 1:
		for element in list:
			output.append([element])
	else:
		for index, element in enumerate(list[:-N+1]):
			for l in combination(list[index+1:],N-1):
				output.append([element] + l)
	return output

#if a numbers location is limited to a single row or column within a square, delete that number from other squares in same row/column
def row_elim():
	for square_cells in puzzle.squares():
		for n in integers:
			cells_with_n = [cell for cell in square_cells if str(n) in cell.value]
			number_cells_with_n = len(cells_with_n)
			if 1<number_cells_with_n <= 3:
				#all cells in same row
				if len([cell_n.y == cells_with_n[0].y for cell_n in cells_with_n]) == number_cells_with_n:
					for row_cell in puzzle.row(cells_with_n[0].y):
						if row_cell not in square_cells:
							row_cell.delete_value(str(n))
				#same column
				elif len([cell_n.x == cells_with_n[0].x for cell_n in cells_with_n]) == number_cells_with_n:
					for column_cell in puzzle.column(cells_with_n[0].x):
						if column_cell not in square_cells:
							column_cell.delete_value(str(n))


def color(cell):
	return cell.get_attribute("style")[18:36]
def value(cell):
	return cell.find_element_by_tag_name("input").get_attribute("value")
def has_clue(cell):
	return cell.get_attribute("style")[74:78] == 'clue'
def get_clue(cell):
	return int(cell.get_attribute("style")[80:-7])
def write(cell, str):
	cell.click()
	cell.find_element_by_tag_name("input").send_keys(str)














#get puzzle info from webpage
html_table = browser.find_element_by_class_name('sudokutable')
table_rows = [html_row.find_elements_by_tag_name('td')[1:10] for html_row in html_table.find_elements_by_tag_name('tr')[1:10]]
puzzle = Killer_Puzzle(table_rows)



i = 0
while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i<20:
	search_for_subgroups()

	for g in puzzle.groups:
		g.check_pairs()
		g.one_unknown()

	for c in puzzle.cells:
		c.one_value()
	i+=1
print i
