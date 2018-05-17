from puzzleClass import Puzzle, Cell
import random, copy, time
from selenium import webdriver

class Game(Puzzle):

	size = 4
	def __init__(self, values = None):

		self.keep_going = True  #play beyond 2048
		self.run_browser = False
		if self.run_browser:
			self.size = 4

		self.button_dismissed = False
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


	# def print_errors(self):
	# 	for values in self.history:
	# 		if values.index(max(values)) != 12:
	# 			for index, cell in enumerate(self.cells):
	# 				cell.value = values[index]
	# 			self.show_board()

	def print_all_history(self):
		for values in self.history:
			for index, cell in enumerate(self.cells):
				cell.value = values[index]
			self.show_board()
			print [c.value for c in self.standard_path()]

	def get_score(self):
		return max([cell.value for cell in self.cells])

	def largest_cell(self):
		max_value = 0
		max_cell = None
		for cell in self.cells:
			if cell.value and cell.value > max_value:
				max_value = cell.value
				max_cell = cell
		return max_cell


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
				number += (5 - len(number))*" "
				s += number
			print s

	def add_2(self):
		if self.run_browser:
			try:
				[y,x], value = self.get_new_tile()

			except:
				time.sleep(.200)
				[y,x], value = self.get_new_tile()
			self.coord(y-1,x-1).value = value
		else:
			cell = random.choice([cell for cell in self.cells if cell.value == None])
			cell.value = 2 if random.random() < .9 else 4


	def game_over(self):
		for cell in self.cells:

			if cell.value == 2048:
				if self.keep_going:
					if self.run_browser:
						if not self.button_dismissed:
							time.sleep(1.5)
							self.browser.find_element_by_class_name("keep-playing-button").click()
							self.button_dismissed = True
				else:
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
				
				word += character
				if (index + 1.0)/5 == round((index + 1.0)/5):
					number = word.strip()

					values.append(None if number == "" else int(number))
					word = ""

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


				
				
				# self.show_board()
				# print self.at_risk()

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





	def get_outcomes(self, non_standard = False):
		current_values = [cell.value for cell in self.cells]
		outcomes = []
		for direction in ["left", "right", "down"]:
			game = Game(current_values)
			valid_move = game.shift(direction)
			if non_standard:
				path_sum = self.path_sum(game.path())
			else:
				path_sum = self.path_sum(game.standard_path())
			if valid_move:
				outcomes.append([direction, path_sum, game])
		return outcomes


#3 directions sorted by standard path sum

#end of path my be blocked/ unblocked


#if all outcomes are blockec, use non-standard path.


#avoid displacment of largest tile:
	#avoid pressing up
		#If up is pressed, press down after
	#avoid pressing right if bottom row is unstable
		#if right is pressed, immediatley press left afterwards



	def maximize(self, path):
		outcomes = self.get_outcomes()

		sorted_outcomes = sorted(outcomes, key=lambda pair: pair[1])

		sorted_outcomes = [outcome for outcome in sorted_outcomes if not outcome[2].at_risk()]

		unblocked_outcomes = [outcome for outcome in sorted_outcomes if not self.is_blocked(outcome[2].standard_path()) and self.path_sum(outcome[2].standard_path()) != 0 and not outcome[2].at_risk()]

		outcome_to_try = sorted_outcomes + unblocked_outcomes



		if len(unblocked_outcomes) == 0:
			outcomes = self.get_outcomes(True)
			sorted_outcomes = sorted(outcomes, key=lambda pair: pair[1])
			outcome_to_try = sorted_outcomes
			#[outcome for outcome in sorted_outcomes if not outcome[2].at_risk()]


			
		if len(outcome_to_try) == 0:
			self.shift("up")
			self.shift("down")
		else:
			self.shift(outcome_to_try.pop()[0])


		#if number of pices not in path is greater than number of pieces in path and number of blank spaces < 4


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
		#[direction, path_sum, game])
		 #["left", "right", "down"]
		outcomes = self.get_outcomes()

		#if the path contains any duplicates. combine them.
		path = self.standard_path()

		for index, cell in enumerate(path[:-1]):
			next_cell = path[index + 1]
			if cell.value == next_cell.value:
				if cell.x == next_cell.x: #cells in same column

					if not outcomes[-1][2].at_risk():
						self.shift("down")
					else:
						break
				else: #same row

					# check to make sure startin cell is stable before
					#make sure all preceeding cells are stable
					if cell.right == next_cell:
						if not outcomes[0][2].at_risk():
							self.shift("left")
						else:
							break

					elif cell.left == next_cell:
						bottom_row = [cell.value for cell in self.row(self.size - 1)]
						if self.is_stable(bottom_row):
							if outcomes[1][0] == "right":
								if not outcomes[1][2].at_risk():
									self.shift("right")
								else:
									break
							elif outcomes[0][0] == "right":
								if not outcomes[0][2].at_risk():
									self.shift("right")
								else:
									break
						else:
							if not outcomes[0][2].at_risk():
								self.shift("left")
							else:
								break
				return

		self.maximize(path) 

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
				else:
					current_cell = cells[-1]
			except:
				break

			if current_cell.value == None:
				break
			else:
				path.append(current_cell)

		return path


	def path(self, y = size - 1 , x = 0):

		# only deviate from "standard path" if next cell is larger than current cell not if this a blank??!?! YES
		#can deviate from path is a cell of equal value is found
		path = []
		current_cell = self.coord(y,x)
		path.append(current_cell)

		while True:

			options = [current_cell.up, current_cell.right, current_cell.left]

			cells = [cell for cell in options if cell and cell not in path and cell.value != None and cell.value <= current_cell.value]

			try:
				current_cell = sorted(cells, key=lambda cell: cell.value)[-1]
				path.append(current_cell)
			except:
				break

		return path


	def path_sum(self, path):
		return sum([cell.value if cell.value != None else 0 for cell in path])


	def standard_path_sum(self, y = size - 1, x = 0):
		return sum([cell.value if cell.value != None else 0 for cell in self.standard_path(y, x)])

	def q(self):
		self.browser.quit()

	def run(self):
		while True:
			self.automate_move()
			# self.maximize(self.standard_path())
			if self.game_over():	
				break
		return self.get_score()




	def at_risk(self):


		#bottom row(s) are full and stable (cant be compressed sideways)
		rows = self.rows()
		rows.reverse()
		unstable_row_found = False
		for row in rows:
			values = [c.value for c in row]

			if not unstable_row_found:
				if not self.collapse_row(values, False) == self.collapse_row(values, True):
					unstable_row_found = True

					for index, cell in enumerate(row[:-1]):
						if cell.value == row[index+1].value:
							return False

					#partially filled row with 3 cells and 1 blank cell.
					if not values.count(None) == 1:
						return False
					else:
					#blank cell is NOT adjacent to both a 2 and a 4
						blank_cell = [cell for cell in row if cell.value == None][0]
						two_found = False
						four_found = False
						for cell in blank_cell.neighbors():
							if cell.value == 2:
								two_found = True
							elif cell.value == 4:
								four_found = True

						if two_found and four_found:
							return False	
					
			else:
				#rest of the rows are empty
				if not sum([value == None for value in values]) == len(values):
					return False

		#no cells can be compressed vertically down
		for column in self.columns():
			values = [c.value for c in column]
			if self.collapse_row(values, True) != values:
				return False

		if not unstable_row_found:
			return False
		else:
			return True

		
		





def run_game(runs = 100):

	scores = []
	for i in range(runs):
		print i
		g = Game()
		g.new_game()
		score = g.run()
		scores.append(score)

	return scores

def win_rate():
	data = run_game()
	print "Win Rate: " + str(len([score for score in data if score >= 2048])/(len(data)+1.0 - 1.0))
	print "Average Score: " + str(sum(data)/len(data))


	d = {}
	for score in data:
		if score in d.keys():
			d[score] += 1
		else:
			d[score] = 1
	print d


def run_until_loss():
	for i in range(100):
		g = Game()
		g.new_game()
		score = g.run()
		if score<=512:
			g.print_all_history()
			break
# run_until_loss()
win_rate()
# g = Game()
# g.new_game()
# g.run()
# g.show_board()


#if a 'tumor' grows too large, larger than 64, then don't use standard path


# win_rate()
# Win Rate: 0.37
# Average Score: 1402
# {2048: 29, 512: 23, 4096: 8, 1024: 34, 256: 6}


# Win Rate: 0.53
# Average Score: 1719
# {1024: 30, 512: 15, 4096: 12, 128: 1, 256: 1, 2048: 41}


# Win Rate: 0.54
# Average Score: 1990
# {2048: 32, 4096: 21, 1024: 33, 8192: 1, 128: 1, 256: 3, 512: 9}


# Win Rate: 0.53
# Average Score: 2035
# {4096: 22, 2048: 30, 8192: 1, 256: 1, 512: 7, 1024: 39}


#goal get average score over 2048!!!
#improve time effeciency!!


#whyy?!
"""
2   4   2       
4   2   8       
8   16  64  4   
1024512     2   
[1024, 512]
2   4   2       
4   2   8   2   
8   16  64  4   
1024512 2   
"""


# 2   2           
# 4   8   2       
# 2   16  8       
# 4096204810248   



# g = Game()
# g.new_game()

# a = """2              2    
#      4    8    2    
# 2    16   32   8    
# 512  256  128  64   """

# g.undo(a)


'''
2              2    
     4    8    2    
2    16   32   8    
512  256  128  64   
[512, 256, 128, 64, 8, 2, 2]
                    
2    4    8    4    
4    16   32   8    
512  256  128  64   
[512, 256, 128, 64, 8, 4]

'''

'''
4         4         
4    8              
4    16   64   128  
4096 2048 512  256  
[4096, 2048, 512, 256, 128, 64, 16, 4, 4, 4]
                    
4    8    4    2    
8    16   64   128  
4096 2048 512  256 
'''

#when merging adjacent duplicate-valued-cells in path, make sure the move will not put puzzle at risk of being forced to press up!!!!!




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








