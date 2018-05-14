from puzzleClass import Puzzle, Cell
import random, copy, time

#initiate selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

class Game(Puzzle):


	size = 4
	def __init__(self, values = None):

		self.run_browser = False
		self.browser = None
		self.height = self.size 
		self.width = self.size 
		self.history = []
		self.cells = []
		self.test = True if values else False

		for y in range(self.size):
			for x in range(self.size):
				self.cells.append(Cell(self, None, y, x))


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

		if values:
			for index, cell in enumerate(self.cells):
				cell.value = values[index]

	def update_history(self):
		self.history.append([cell.value for cell in self.cells])

	def get_score(self):
		return max([cell.value for cell in self.cells])

	def open_web_puzzle(self):
		self.browser = webdriver.Chrome()
		self.browser.set_window_position(686, 29)
		self.browser.set_window_size(677, 736)
		url = "https://gabrielecirulli.github.io/2048/"
		self.browser.get(url)
		self.browser.execute_script("return arguments[0].scrollIntoView();", self.browser.find_element_by_class_name('game-container'))

	def getTiles(self):
		self.grid = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]

		tiles = self.browser.find_element_by_class_name("tile-container").find_elements_by_xpath("*")

		for tile in tiles:
			tile_attributes = tile.get_attribute("class").split(" ")
			value = int(tile_attributes[1][5:])
			x,y = [int(coord) for coord in tile_attributes[2][14:].split("-")]

			self.coord(y-1,x-1).value = value

	def get_new_tile(self):
		tiles = self.browser.find_element_by_class_name("tile-container").find_elements_by_xpath("*")

		for tile in tiles:

			if tile.get_attribute("class")[-3:] == "new":
				tile_attributes = tile.get_attribute("class").split(" ")
				value = int(tile_attributes[1][5:])
				x,y = [int(coord) for coord in tile_attributes[2][14:].split("-")]

				return [[y,x], value]



	def new_game(self):
		self.history = []
		for cell in self.cells:
			cell.value = None

		if self.run_browser:
			self.open_web_puzzle()
			time.sleep(1)
			self.getTiles()

		else:
			self.add_2()
			self.add_2()
			self.update_history()

	def show_board(self):
		for row in self.rows():
			s = ""
			for number in [str(cell.value) if cell.value != None else " " for cell in row]:
				number += (4 - len(number))*" "
				s += number
			print s

	def add_2(self):
		if self.run_browser:
			try:
				[y,x], value = self.get_new_tile()

			except:
				time.sleep(.500)
				[y,x], value = self.get_new_tile()
			self.coord(y-1,x-1).value = value
		else:
			cell = random.choice([cell for cell in self.cells if cell.value == None])
			cell.value = 2 if random.random() < .9 else 4


	def game_over(self):
		for cell in self.cells:
			if cell.value == 2048:
				return True
		for cell in self.cells:
			if cell.value == None:
				return False
		for row in self.rows() + self.columns():
			for index, cell in enumerate(row[:-1]):
				if row[index].value == row[index + 1].value:
					return False
		return True

	def collapse_row(self, row, reverse):

		row = list(row)

		if reverse:
			row.reverse()

		row = [element for element in row if element != None]

		index = 1
		while index < len(row):
			if row[index] == row[index - 1]:
				row[index] *= 2
				row[index - 1] = None
				index+=1
			index +=1

		row = [element for element in row if element != None]

		padding_size = self.size - len(row)

		row = row + padding_size*[None]

		if reverse:
			row.reverse()

		return row

	def get_values(self, string):
		values = []
		for row in string.split("\n"):
			word = ""
			for index, character in enumerate(row):

				if (index + 1.0)/4 == round((index + 1.0)/4):
					number = word.strip()

					values.append(None if number == "" else int(number))
					word = ""
				else:
					word += character
		return values
	def undo(self, string = None):
		if string:
			values = self.get_values(string)
			for index, cell in enumerate(self.cells):
				cell.value = values[index]
			self.history = []
		else:
			old_values = self.history[-2]
			for index, cell in enumerate(self.cells):
				cell.value = old_values[index]
			self.history.pop()
		
		self.show_board()


	def shift(self, direction, Testing = False):
		previous_values = [cell.value for cell in self.cells]

		rows = self.columns() if direction == "up" or direction == "down" else self.rows()

		for row in rows:
			
			reverse = True if direction == "down" or direction == "right" else False
			new_row_values = self.collapse_row([cell.value for cell in row], reverse)
			for cell in row:
				cell.value = new_row_values.pop(0)

		if [cell.value for cell in self.cells] != previous_values:
			if not self.test:
				if self.run_browser:
					self.press_key(direction)
				self.add_2()
				# print direction
			self.update_history()
			
			# if not self.test:
			# 	# self.show_board()
			# 	# print [c.value for c in self.standard_path()]
			return True


		else:
			return False

	def press_key(self, direction):
		body = self.browser.find_element_by_tag_name("body")
		if direction == "up":
			body.send_keys("w")
		elif direction == "down":
			body.send_keys("s")
		elif direction == "right":
			body.send_keys("d")
		elif direction == "left":
			body.send_keys("a")


	def is_stable(self, row):
		return self.collapse_row(row, False) == row

	def is_full(self, row):
		return row.count(None) == 0





	def get_outcomes(self):
		current_values = [cell.value for cell in self.cells]
		outcomes = []
		for direction in ["left", "right", "down"]:
			game = Game(current_values)
			valid_move =game.shift(direction)
			path_sum = game.standard_path_sum()
			if valid_move:
				outcomes.append([direction, path_sum, game])
		return outcomes

	def maximize_standard_path_sum(self):
		outcomes = self.get_outcomes()

		sorted_outcomes = sorted(outcomes, key=lambda outcome: outcome[1])

		valid_move = False
		while not valid_move:
			if len(sorted_outcomes) == 0:
				self.shift("up")
				self.shift("down")
				break
			valid_move = self.shift(sorted_outcomes.pop()[0])

	def clear_end(self, path):
		outcomes = self.get_outcomes()

		sorted_outcomes = sorted(outcomes, key=lambda pair: pair[1])

		unblocked_outcomes = [outcome for outcome in sorted_outcomes if not self.is_blocked(outcome[2].standard_path())]

		valid_move = False
		outcome_to_try = sorted_outcomes + unblocked_outcomes
		while not valid_move:
			if len(outcome_to_try) == 0:
				self.shift("up")
				self.shift("down")
				break

			valid_move = self.shift(outcome_to_try.pop()[0])



	def is_blocked(self, path):
		#make sure there are not duplicates in path first
		for index, cell in enumerate(path[:-1]):
			next_cell = path[index + 1]
			if cell.value == next_cell.value:
				return False
		for cell in path[-1].neighbors():
			if cell.value == None:
				return False
		return True


	def automate_move(self):

		#if the path contains any duplicates. combine them.
		path = self.standard_path()

		for index, cell in enumerate(path[:-1]):
			next_cell = path[index + 1]
			if cell.value == next_cell.value:
				if cell.x == next_cell.x: #cells in same column
					self.shift("down")
				else: #same row

					# check to make sure startin cell is stable before
					#make sure all preceeding cells are stable
					if cell.right == next_cell:
						self.shift("left")
					elif cell.left == next_cell:
						bottom_row = [cell.value for cell in self.row(self.size - 1)]
						if self.is_stable(bottom_row):
							self.shift("right")
						else:
							self.shift("left")
				return

		# self.clear_end(path)
		if self.is_blocked(path):
			self.clear_end(path)
		else:
			self.maximize_standard_path_sum()



	def standard_path(self, y = size - 1 , x = 0):
		
		path = []
		current_cell = self.coord(y,x)
		path.append(current_cell)

		while True:

			options = [current_cell.up, current_cell.right, current_cell.left]

			cells = [cell for cell in options if cell and cell not in path and cell.value <= current_cell.value] 

			try:
				#can deviate from path is a cell of equal value is found
				if cells[0].value == current_cell.value:
					current_cell = cells[0]
					# print "ASDFASDFASDF"
				else:
					current_cell = cells[-1]
			except:
				break

			if current_cell.value == None:
				break
			else:
				path.append(current_cell)
		return path


	def standard_path_sum(self, y = size - 1, x = 0):
		return sum([cell.value if cell.value != None else 0 for cell in self.standard_path(y, x)])

	def q(self):
		self.browser.quit()

	def run(self):
		while True:
			self.automate_move()
			if self.game_over():
				break
		return self.get_score()
		





runs = 10
total_score = 0.0
for i in range(runs):
	print i
	g = Game()
	g.new_game()
	score = g.run()
	total_score += score

print total_score/runs



	# def top_non_empty_row_at_risk(self):
	# 	for row in self.rows():
	# 		row_values = [cell.value for cell in row]
	# 		if row_values.count(None) < 4:
	# 			if row_values.count(None) == 1:
	# 				return True	
	# 			else:
	# 				return False	
	# 	return False
	# def one_option(self):

	# 	if self.shift("down", True) == False and self.shift("left", True) == False:
	# 		self.shift("right")

	# 	elif self.shift("down", True) == False and self.shift("right", True) == False:
	# 		self.shift("left")

	# 	elif self.shift("right", True) == False and self.shift("left", True) == False:
	# 		self.shift("down")
	# def path(self, y, x):

	# 	# only deviate from "standard path" if next cell is larger than current cell not if this a blank??!?! YES
	# 	#can deviate from path is a cell of equal value is found
	# 	path = []
	# 	current_cell = self.coord(y,x)
	# 	path.append(current_cell)

	# 	while True:

	# 		options = [current_cell.up, current_cell.right, current_cell.left]

	# 		cells = [cell for cell in options if cell and cell not in path and cell.value != None and cell.value <= current_cell.value]

	# 		try:
	# 			current_cell = sorted(cells, key=lambda cell: cell.value)[-1]
	# 			path.append(current_cell)
	# 		except:
	# 			break

	# 	return path
	# def automate(self):
		
	# 	for i in range(100):
	# 		if self.game_over():
	# 			break
	# 		previous_values = [cell.value for cell in self.cells]

	# 		self.shift("left")
	# 		self.shift("down")
	# 		self.shift("down")
	# 		self.shift("down")
			

	# 		if [cell.value for cell in self.cells] == previous_values:
	# 			self.shift("right")


	# 			if self.coord(3,0) != None:
	# 				self.shift("down")
	# def b(self):
	# 	#
	# 	outcomes = [self.shift("down", True),
	# 					self.shift("right", True),
	# 					self.shift("left", True),
	# 					self.shift("up", True),
	# 					]

	# 	valid_outcomes = [outcome for outcome in outcomes if outcome]
	# def a(self):

	# 	#if bottom row in not stable, don't press right
	# 	bottom_row = [cell.value for cell in self.row(self.size - 1)]
	# 	if not self.is_stable(bottom_row):

	# 		#if full press left,
	# 		if self.is_full(bottom_row):
	# 			if self.shift("down"):
	# 				return
	# 			if self.shift("left"):
	# 				return
	# 			if self.shift("right"):
	# 				return
	# 			if self.shift("up"):
	# 				return


	# 		else: #	if there is a blank space press down until filled or until down is invalid move.
	# 			if self.coord(self.size - 1,0).value == None and bottom_row.count(None) != 4:
	# 				self.shift("left")
	# 			else:
	# 				if self.shift("down"):
	# 					return
	# 				if self.shift("left"):
	# 					return
	# 				if self.shift("right"):
	# 					return
	# 				if self.shift("up"):
	# 					return

	# 	else:

	# 		#if bottom row is stable
	# 		#if right most value in 3rd row is greater then right most value of bottom row, try to 

	# 		# print "BOTTOM ROW STABLE"
	# 		if self.coord(2,3).value > self.coord(3,3).value:
	# 			self.shift("left")
	# 			self.shift("down")
	# 			self.shift("right")
	# 		else:
	# 			if self.shift("down"):
	# 				return
	# 			if self.shift("right"):
	# 				return
	# 			if self.shift("left"):
	# 				return
	# 			if self.shift("up"):
	# 				return



#rules:
#don't press up ever, avoid scenario in which up is only option
#if bottom row in not stable, don't press right
#	if full press left,
#	if there is a blank space press down until filled or until down is invalid move.



#generate path until a cell is in a unstable row.
#try to stablize row..



# 1:make moves that increase value of last cell
# 2:make moves than move cells of equal or lesser value compared to last cell adjacent to last cell
# 3:make moves that move cells of equal or lesser value compared to last cell to same row/column of last cell

#how to keep track of cells when they move?? 

# a = """            2   
#         4   2   
# 2       16  8   
#     256 16  4   """
# g.undo(a)













