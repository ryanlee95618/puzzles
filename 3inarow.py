from puzzleClass import Puzzle, Cell

#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
browser.set_window_position(650, 0)
url = 'https://www.brainbashers.com/show3inarow.asp?date=0126&diff=2&size=18'
browser.get(url) 
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_id('puzzlediv'))
check_button = browser.find_element_by_xpath("//*[@id='puzzleContainer']/tbody/tr[2]/td/p[2]/a[6]")


def e():
	browser.quit()


class Threes_Puzzle(Puzzle):

	def __init__(self, array):

		#store cells and connect them to each other
		self.height = len(array)
		self.width = len(array[0])
		self.size = self.height
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

	def scan_row(self):

		for row in self.rows() + self.columns():
			number_of_blacks, number_of_whites, _ = self.count_colors(row)

			if number_of_blacks == self.size/2:
				for cell in row:
					if cell.state == None:
						cell.set_state("white")
			elif number_of_whites == self.size/2:
				for cell in row:
					if cell.state == None:
						cell.set_state("black")


			elif number_of_blacks == (self.size/2 - 1):
				for cell in row:
					if cell.state == None:
						for group_of_three in self.groups_of_three(row):
							if cell not in group_of_three:
								number_of_blacks, number_of_whites, number_of_blanks = self.count_colors(group_of_three)
								if number_of_whites + number_of_blanks == 3:
									cell.set_state("white")
						
			elif number_of_whites == (self.size/2 - 1):
				for cell in row:
					if cell.state == None:
						for group_of_three in self.groups_of_three(row):
							if cell not in group_of_three:
								number_of_blacks, number_of_whites, number_of_blanks = self.count_colors(group_of_three)
								if number_of_blacks + number_of_blanks == 3:
									cell.set_state("black")
	
	#return groups of 3 consectuive cells
	def groups_of_three(self, cell_list):
		output = []
		for index, cell in enumerate(cell_list[1:-1]):
			output.append([cell_list[index], cell, cell_list[index+2]])
		return output


	def count_colors(self, cell_list):
		n_of_white = 0
		n_of_black = 0
		n_of_blank = 0

		for cell in cell_list:
			if cell.state == "white":
				n_of_white += 1
			elif cell.state == "black":
				n_of_black += 1
			else:
				n_of_blank += 1
		return [n_of_black, n_of_white, n_of_blank]

	def scan(self):
		for row in self.rows() + self.columns():

			for group_of_three in self.groups_of_three(row):

				number_of_blacks, number_of_whites, number_of_blanks = self.count_colors(group_of_three)

				if number_of_whites == 2 and number_of_blanks == 1:
					[c for c in group_of_three if c.state == None][0].set_state("black")
				elif number_of_blacks == 2 and number_of_blanks == 1:
					[c for c in group_of_three if c.state == None][0].set_state("white")


class Number_Cell(Cell):
	def __init__(self, puzzle, html_cell, y, x):

		if html_cell.get_attribute('class').find('black')>-1:
			self.state = 'black'
		elif html_cell.get_attribute('class').find('white')>-1:
			self.state = 'white'
		else:
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

		if self.state != None:
			return

		self.state = state

	
		if state == "black":
			html_puzzle[self.y][self.x].click()
		else: #state == "white"
			html_puzzle[self.y][self.x].click()
			html_puzzle[self.y][self.x].click()


		# check_button.click()
		# if browser.find_element_by_id("showtext").find_element_by_tag_name("span").get_attribute("class") == "sred":
		# 	print "y:", self.y, "x:", self.x, "v:", state, inspect.stack()[1][3]
		# 	asdf

html_puzzle = [[html_cell for html_cell in html_row.find_elements_by_tag_name('td')[:-1]] for html_row in browser.find_element_by_id('puzzlediv').find_elements_by_tag_name('tr')[1:]]
puzzle = Threes_Puzzle(html_puzzle)


i = 1
while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i < 20:
	
	puzzle.scan()
	puzzle.scan_row()
	i+=1

if browser.find_element_by_id("showtext").text.find("Puzzle Solved") > -1:
	e()