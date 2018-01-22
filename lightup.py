import inspect
from puzzleClass import Puzzle, Cell
	
#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
browser.set_window_position(650, 0)
url = 'https://www.brainbashers.com/showlightup.asp?date=0120&diff=Hard&size=20'
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_id('puzzlediv'))
check_button = browser.find_element_by_xpath("//*[@id='puzzleContainer']/tbody/tr[3]/td/p[2]/a[6]")


def e():
	browser.quit()

class Light_Puzzle(Puzzle):

	groups = []
	def __init__(self, array):

		#store cells and connect them to each other
		self.height = len(array)
		self.width = len(array[0])
		for y, row, in enumerate(array):
			for x, element in enumerate(row):
				self.cells.append(Number_Cell(self, element, y, x))

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


class Number_Cell(Cell):
	def __init__(self, puzzle, html_cell, y, x):

		picture_name = html_cell.find_element_by_tag_name("img").get_attribute("src")[-9:-4]
		# whte  clueN clueB
		if picture_name.find("clue")>-1:
			self.type = "black"
			if picture_name[-1] == "B":
				self.value = None
			else:
				self.value = int(picture_name[-1])
				self.fufilled = False
		else:
			self.type = "white"
			self.lit = False
			self.bulb = None

		#self.value = value #blank light bulb, crossed out/lit up  black, black w/ number
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None
		self.group = None

	#only applies to blank cells
	def set_state(self, state):
		if self.type == "black":
			return

		if self.lit or self.bulb == True:
			return


		if state == "bulb" and self.is_blank():
			html_puzzle[self.y][self.x].click()
			self.bulb = True
			self.lit = True
			#fill all blanks cells in reach of current cell
			for cell in self.in_sight():
				cell.set_state("lit")

		elif state == "cross" and self.is_blank():
			html_puzzle[self.y][self.x].click()
			html_puzzle[self.y][self.x].click()
			self.bulb = False


		elif state == "lit":
			self.lit = True

		check_button.click()
		if browser.find_element_by_id("showtext").find_element_by_tag_name("span").get_attribute("class") == "sred":
			print "y:", self.y, "x:", self.x, "v:", state, inspect.stack()[1][3]
			asdf

	def in_sight(self, last_cell = False):

		cells = []
		last_cell_list = []
		current_cell = self
		while current_cell.up and not current_cell.up.type == "black":
			cells.append(current_cell.up) 
			current_cell = current_cell.up
		if current_cell.up:
			last_cell_list.append(current_cell.up)

		current_cell = self
		while current_cell.down and not current_cell.down.type == "black":
			cells.append(current_cell.down) 
			current_cell = current_cell.down
		if current_cell.down:
			last_cell_list.append(current_cell.down)

		current_cell = self
		while current_cell.right and not current_cell.right.type == "black":
			cells.append(current_cell.right) 
			current_cell = current_cell.right
		if current_cell.right:
			last_cell_list.append(current_cell.right)

		current_cell = self
		while current_cell.left and not current_cell.left.type == "black":
			cells.append(current_cell.left) 
			current_cell = current_cell.left
		if current_cell.left:
			last_cell_list.append(current_cell.left)

		return cells if not last_cell else last_cell_list

	def is_blank(self):
		return self.type == "white" and self.bulb == None and self.lit == False

	def check_hint(self):
		if self.type == "black" and self.value != None:

			if not self.fufilled:
				number_of_blanks = 0
				number_of_crosses = 0
				number_of_bulbs = 0

				for neighbor in self.neighbors():
					if neighbor.type == "white":
						if neighbor.bulb:
							number_of_bulbs += 1
						elif neighbor.lit or neighbor.bulb == False:
							number_of_crosses += 1
						else:
							number_of_blanks+= 1


				if number_of_blanks + number_of_bulbs == self.value:
					#fill in blank neighbors with bulbs
					for neighbor in self.neighbors():
						if neighbor.type == "white" and neighbor.bulb == None:
							neighbor.set_state("bulb")

				elif number_of_bulbs == self.value:
					self.fufilled = True
					#fill in blank neighbors with crosses
					for neighbor in self.neighbors():
						if neighbor.type == "white" and neighbor.bulb == None:
							neighbor.set_state("cross")

				elif number_of_blanks + number_of_bulbs == self.value + 1:

					if self.up:
						if self.right:
							if self.up.is_blank() and self.right.is_blank():
								self.up.right.set_state("cross")
						if self.left:
							if self.up.is_blank() and self.left.is_blank():
								self.up.left.set_state("cross")
					if self.down:
						if self.right:
							if self.down.is_blank() and self.right.is_blank():
								self.down.right.set_state("cross")
						if self.left:
							if self.down.is_blank() and self.left.is_blank():
								self.down.left.set_state("cross")

	def check_hint_advanced(self):
		if self.type == "black" and self.value == 3:
			if not self.fufilled:
				#find a 2 
				for cell in [cell for cell in self.neighbors() if cell.is_blank()]:
					last_cells = cell.in_sight(True)



	def check_unlit(self):
		if self.type == "white" and not self.lit:
			available_cells_insight = [cell for cell in self.in_sight() if cell.lit == False and cell.bulb == None]

			if self.bulb == False:
				if len(available_cells_insight) == 1:
					available_cells_insight[0].set_state("bulb")


				elif len(available_cells_insight) == 2:
					cell1, cell2 = available_cells_insight
					if cell1.y == cell2.y or cell1.x == cell2.x:
						return
					short_list = [puzzle.coord(cell2.y, cell1.x), puzzle.coord(cell1.y, cell2.x)]
					for cell in short_list:
						if cell != self and cell1 in cell.in_sight() and cell2 in cell.in_sight():
							cell.set_state("cross")

			elif self.bulb == None:
				if len(available_cells_insight) == 0:
					self.set_state("bulb")



#get puzzle info from webpage
html_table = browser.find_element_by_id('puzzlediv')
html_puzzle = [html_row.find_elements_by_tag_name('td') for html_row in html_table.find_elements_by_tag_name('tr')]
#table_rows = [[html_cell for html_cell in html_row.find_elements_by_tag_name('td')] for html_row in html_table.find_elements_by_tag_name('tr')]
puzzle = Light_Puzzle(html_puzzle)





i = 0
while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i<20:
	for c in puzzle.cells:
		c.check_hint()
		c.check_unlit()
	i+=1
print i
