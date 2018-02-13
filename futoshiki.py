from puzzleClass import Puzzle, Cell
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
browser.set_window_position(700, 0)
url = 'https://www.brainbashers.com/showfutoshiki.asp?date=0209&size=9&diff=1'
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_class_name('futoshikitable'))

def e():
	browser.quit()


class Futoshiki_Puzzle(Puzzle):

	def __init__(self, array):
		self.height = len(array)
		self.width = len(array[0])
		for y, row, in enumerate(array):
			for x, element in enumerate(row):
				if y % 2 == 0:
					if x % 2 == 0:
						#its a number cell
						self.cells.append(Number_Cell(self, element.find_element_by_tag_name("input").get_attribute("value"), y, x))
					else:
						#relation type cell
						self.cells.append(Relation_Type(self, element.find_element_by_tag_name("img").get_attribute("src")[-6], y, x))
				else:
					if x % 2 == 0:
						#relation type cell
						self.cells.append(Relation_Type(self, element.find_element_by_tag_name("img").get_attribute("src")[-6], y, x))
					else:
						#None
						self.cells.append(None)



		for cell in self.cells:
			if cell and cell.type == "relation":
				y,x = cell.y, cell.x
				if cell.y % 2 == 0:
					#connect cell left and right to number cells
					self.connect(y, x, y, x-1)
					self.connect(y, x, y, x+1)
				elif cell.x % 2 == 0:
					#connect cell up and down to number cells
					self.connect(y, x, y + 1, x)
					self.connect(y, x, y - 1, x)

		for cell in self.cells:
			if cell and cell.type == "relation":
				cell.make_comparison_pointers()


	def connect(self, y1, x1, y2, x2):
		cell_1 = self.cells[self.to_index(y1,x1)]
		cell_2 = self.cells[self.to_index(y2,x2)]

		if y1 == y2:
			if x1 > x2:
				cell_1.left = cell_2
				cell_2.right = cell_1				
			else:
				cell_1.right = cell_2
				cell_2.left = cell_1				
		elif x1 == x2:
			if y1 > y2:
				cell_1.up = cell_2
				cell_2.down = cell_1
			else:
				cell_1.down = cell_2
				cell_2.up = cell_1

	def columns(self):
		return [self.column(i) for i in range(self.width)]

	def rows(self):
		return [self.row(i) for i in range(self.height)]


class Number_Cell(Cell):
	type = "number"
	def __init__(self, puzzle, value, y, x):

		self.value = value
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None

	def add_value(self, str):
		self.value += str
		# rows[self.y][self.x].find_element_by_tag_name("input").send_keys(str)

		browser.execute_script("return arguments[0].setRangeText(`${arguments[1]}`);", rows[self.y][self.x].find_element_by_tag_name("input"), str)

	def set_value(self, str):
		self.value = str

		rows[self.y][self.x].find_element_by_tag_name("input").clear()


		browser.execute_script("return arguments[0].setRangeText(`${arguments[1]}`);", rows[self.y][self.x].find_element_by_tag_name("input"), str)


		# rows[self.y][self.x].find_element_by_tag_name("input").send_keys(str)

	def delete_value(self, str):
		for character in str:

			if character in self.value:
				new_value = self.value.replace(character, "")
				self.value = new_value
				self.set_value(new_value)

			# if len(self.value) == 1:
			# 	self.update_neighbors()
			# 	self.one_value()

	def get_lowest_value(self):
		return self.value[0]
	def get_highest_value(self):
		return self.value[-1]

	# def update_neighbors(self):
	# 	for relation in self.neighbors():
	# 		relation.check_condition()

	#if a cell has only one value left, delete that value from other cells in row and column
	def one_value(self):
		if len(self.value) == 1:
			for cell in self.row() + self.column():
				if cell.type == "number" and cell != self:
					cell.delete_value(self.value)


class Relation_Type(Cell):

	#uneqR1 left is greater than right
	
	#uneqU1 bottom greater than top

	#uneqL1 right is greater than left
	#uneqD1 top greater than bottom

	# uneqH1
	# uneqV1 no relation

	type = "relation"
	def __init__(self, puzzle, relation, y, x):
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None
		self.value = relation

		
	def make_comparison_pointers(self):
		relation = self.value
		if relation == 'H' or relation == 'V':
			self.relation = False
		else:
			self.relation = True
 			if relation == 'D' or relation == 'L':
				self.greater, self.lesser = self.neighbors()
 			elif relation == 'R' or relation == 'U':
				self.lesser, self.greater = self.neighbors()


	#lowerst value of greater cell must be greater than lowest value of lesser 
	def check_comparision(self):
		changes_made = True
		while changes_made:
			changes_made = False
			if self.greater.get_lowest_value() <= self.lesser.get_lowest_value():
				self.greater.delete_value(self.greater.get_lowest_value())
				changes_made = True

		#highest value of lesser cell must be less than highest value of higher cell
			if self.lesser.get_highest_value() >= self.greater.get_highest_value():
				self.lesser.delete_value(self.lesser.get_highest_value())
				changes_made = True

#if there is only one possible cell location for a number in a row, cell value of that location to tthat number
def one_number_per_row():
	for cell_list in puzzle.rows()[::2] + puzzle.columns()[::2]:
		number_cells = [cell for cell in cell_list if cell and cell.type == "number"]
		counter = [0]*((puzzle.height+1)/2+1)
		for cell in number_cells:
			for char in cell.value:
				counter[int(char)] += 1
		for n, count in enumerate(counter):
			if count == 1:
				for cell in number_cells:
					if str(n) in cell.value and len(cell.value) > 1:
						cell.set_value(str(n))


#search all rows/columns for subgroups of sizes 2 through 4 inclusive.
# a subgroup is a set of N cells with a total of N combined possible values
def search_for_subgroups():
	for cell_list in puzzle.rows()[::2] + puzzle.columns()[::2]:
		number_cells = [cell for cell in cell_list if cell and cell.type == "number" and len(cell.value) > 1]
		for N in range(2,5):
			short_list = [cell for cell in number_cells if len(cell.value) <= N]
			groups = combination(short_list, N)
			for group in groups:
				all_possible_values = set(list("".join([cell.value for cell in group])))
				if len(all_possible_values) == N:
					for cell in number_cells:
						if cell not in group:
							cell.delete_value("".join(list(all_possible_values)))

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



html_table = browser.find_element_by_class_name('futoshikitable')
rows = [html_row.find_elements_by_tag_name('td') for html_row in html_table.find_elements_by_tag_name('tr')]
puzzle = Futoshiki_Puzzle(rows[:-1])



# str = 1111
# browser.execute_script("return arguments[0].setRangeText(`${arguments[1]}`);", rows[0][0].find_element_by_tag_name("input"), str)



# add all numbers to every cell
for cell in puzzle.cells:
	if cell and cell.type == "number":
		if len(cell.value) != 1:
			cell.add_value( "".join([str(n) for n in range(1, (puzzle.width+1)/2 +1)]))



for cell in puzzle.cells:
	if cell and cell.type == "number":
		cell.one_value()


for cell in puzzle.cells:
	if cell and cell.type == "relation" and cell.relation:
		cell.check_comparision()






i = 1
while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i < 10:
	print i
	for cell in puzzle.cells:
		if cell:
			if cell.type == "number":
				cell.one_value()
			elif cell.type == "relation" and cell.relation:
				cell.check_comparision()

			
			one_number_per_row()



			#cell.update_neighbors()
			
			search_for_subgroups()
	i+=1
	