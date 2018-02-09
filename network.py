import inspect, copy
from puzzleClass import Puzzle, Cell
	
#initiate selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
browser = webdriver.Chrome()


#open webpage
browser.set_window_position(750, 0)
url = 'https://www.brainbashers.com/shownetwork.asp?date=0207&size=12&diff=WRAP'
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_id('puzzlediv'))
check_button = browser.find_element_by_xpath("//*[@id='puzzleContainer']/tbody/tr/td/p[2]/a[5]")

def e():
	browser.quit()

class Network_Puzzle(Puzzle):

	type = url.split("=")[-1]

	def __init__(self, array, puzzle = None):

		
		#make a test copy of the puzzle
		if puzzle:
			self.height = puzzle.height
			self.width = puzzle.width
			self.cells = [copy.deepcopy(cell) for cell in puzzle.cells]
			for cell in self.cells:
				cell.puzzle = self
			self.test = True

		#initiate cells
		else:
			self.height = len(array)
			self.width = len(array[0])
			self.test = False
			for y, row, in enumerate(array):
				for x, element in enumerate(row):
					self.cells.append(Number_Cell(self, element, y, x))

		self.connect_cells()

	def connect_cells(self):

		if self.type == "NOWRAP":
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

		elif self.type == "WRAP":
			for index, cell in enumerate(self.cells):
				y,x = self.to_coordinates(index)
				cell.up = self.cells[self.to_index((y - 1) % self.height, x)]
				cell.down = self.cells[self.to_index((y + 1) % self.height, x)]
				cell.right = self.cells[self.to_index(y, (x + 1) % self.width)]
				cell.left = self.cells[self.to_index(y, (x - 1) % self.width)]
	
	def check_starting_cases(self):
		if self.type == "NOWRAP":
			#border of puzzle cannot be connectioned
			for index, cell in enumerate(self.cells):
				y,x = self.to_coordinates(index)
				if y == 0:
					cell.connections[0] = False
				if y == self.height - 1:
					cell.connections[2] = False
				if x == self.width - 1:
					cell.connections[1] = False
				if x == 0:
					cell.connections[3] = False

		elif self.type == "WRAP":	
			for cell in self.cells:
				if not cell.locked:
					cell.starting_cases()

	def solve(self):

		self.check_starting_cases()			

		i = 0
		while sum([cell.locked for cell in self.cells]) != len(self.cells) and i<20: 	
			self.changes = False
			self.check_cells()
			if not self.changes:
				self.guess()
			i += 1

		if sum([cell.locked for cell in self.cells]) == len(self.cells):
			browser.quit()
		else:
			print "failed, ran tests ", i, " times"

	def check_cells(self):
		for cell in self.cells:
			if not cell.locked:
				cell.check_connections()
				cell.check_separate_network()
				cell.check_closed_loop()

	def find_contradiction(self):
		for cell in self.cells:
			if not cell.locked and cell.count_valid_orientations() == 0:
				return True
			for neighbor, direction in cell.neighbors_with_direction():
				if (cell.connections[direction] == True and neighbor.connections[neighbor.opposite(direction)] == False) or (cell.connections[direction] == False and neighbor.connections[neighbor.opposite(direction)] == True):
					return True
		else:			
			return False

	def guess(self):
		for cell in self.cells:

			if not cell.locked and cell.count_valid_orientations() == 2:

				print "guessing"
				for direction in range(4):
					if cell.matched():
						
						test_copy = Network_Puzzle(None, self)
						test_copy.coord(cell.y, cell.x).lock()
		
						if test_copy.find_contradiction():
							cell.rotate()
							while not cell.matched():
								cell.rotate()
							cell.lock()
							self.check_cells()
							break							
					cell.rotate()


class Number_Cell(Cell):
	type = "number"
	def __init__(self, puzzle, hmtl_cell, y, x):

		gif_name = hmtl_cell.find_element_by_tag_name("img").get_attribute("src")[-5:-4]
		#4 types of cells: dead (end), line, turn, split

		if gif_name == "1":
			self.state = [False, True, False, False] #[up, right, down, left]
			self.type = "dead"
		elif gif_name == "2":
			self.state = [True, False, False, False]
			self.type = "dead"
		elif gif_name == "4":
			self.state = [False, False, False, True]
			self.type = "dead"
		elif gif_name == "8":
			self.state = [False, False, True, False]
			self.type = "dead"

		elif gif_name == "5":
			self.state = [False, True, False, True]
			self.type = "line"
		elif gif_name == "a":
			self.state = [True, False, True, False]
			self.type = "line"

		elif gif_name == "3":
			self.state = [True, True, False, False]
			self.type = "turn"
		elif gif_name == "9":
			self.state = [False, True, True, False]
			self.type = "turn"
		elif gif_name == "c":
			self.state = [False, False, True, True]
			self.type = "turn"
		elif gif_name == "6":
			self.state = [True, False, False, True]
			self.type = "turn"

		elif gif_name == "e":
			self.state = [True, False, True, True]
			self.type = "split"
		elif gif_name == "d":
			self.state = [False, True, True, True]
			self.type = "split"
		elif gif_name == "b":
			self.state = [True, True, True, False]
			self.type = "split"
		elif gif_name == "7":
			self.state = [True, True, False, True]
			self.type = "split"
		else:
			print gif_name, y, x, "UNEXPECTED GIF NAME"

		self.connections = [None, None, None, None]
		self.locked = False
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None


	def rotate(self, testing = False):
		if self.locked:
			print "tried to rotate locked cell", self.y, self.x
			return
		self.state = self.state[1:] + [self.state[0]]
		if not testing and not self.puzzle.test:
			html_puzzle[self.y][self.x].click()

	def opposite(self, direction):
		return (direction + 2) % 4

	def neighbors_with_direction(self):
		return [pair for pair in [[self.up, 0], [self.right, 1], [self.down, 2], [self.left, 3]] if pair[0]]

	def lock(self):

		if self.locked:
			print "tried to lock locked cell", self.y, self.x
			return

		self.locked = True
		self.connections = self.state
		self.update_neighbors_connections()

		if not self.puzzle.test:
			hover = ActionChains(browser).move_to_element(html_puzzle[self.y][self.x]).send_keys(" ")
			hover.perform()
			self.puzzle.changes = True

		for neighbor in self.neighbors():
			if not neighbor.locked:
				neighbor.check_connections()

	# def set_connection(self, direction, state)
	# 	self.connections[direction] = state
	# 	self.neighbors()[direction].state[self.opposite(direction)] = state

	def update_neighbors_connections(self):
		for neighbor, direction in self.neighbors_with_direction():
			if self.connections[direction] != None:
				neighbor.connections[self.opposite(direction)] = self.connections[direction]

	def check_separate_network(self):

		#necesaary # of connections minus # of known connections == 1
		if sum(self.state) - len([connection for connection in self.connections if connection == True]) == 1:

			#check that known connections lead to dead ends
			#if only unlocked cell in network is itself, then this is true
			if len([cell for cell in self.explore() if not cell.locked]) == 1:

				#none connections can't lead to a dead end 
				for neighbor, direction in self.neighbors_with_direction():
					if self.connections[direction] == None and neighbor.type == "dead":
						self.connections[direction] = False
						neighbor.connections[self.opposite(direction)] = False

	def check_closed_loop(self):

		for neighbor, direction in self.neighbors_with_direction():
			if not neighbor.locked:
				if neighbor in self.explore():

					if self.connections[direction] != True and neighbor.connections[self.opposite(direction)] != True:
						self.connections[direction] = False
						neighbor.connections[self.opposite(direction)] = False

		#special case
		if self.type == "split" and self.puzzle.type == "WRAP":
			for i in range(4):
				diagonal_neighbor = self.neighbors()[i].neighbors()[(i+1)%4]
				if diagonal_neighbor.connections[(i+2)%4] == True and diagonal_neighbor.connections[(i+3)%4] == True:
					self.connections[(i+2)%4] = True
					self.connections[(i+3)%4] = True
					self.update_neighbors_connections()



	def __connected_neighbors(self):
		return [neighbor for neighbor, direction in self.neighbors_with_direction() if self.connections[direction] == True] 

	#get all reachable cells traveling through known connections
	def explore(self):
		explored = [False for cell in self.puzzle.cells]
		exploration_list = [self]

		network = [self]
		explored[self.index()] = True

		while len(exploration_list) > 0:

			network_cell = exploration_list.pop()

			for connected_cell in network_cell.__connected_neighbors():

				if explored[connected_cell.index()]:
					continue

				exploration_list.append(connected_cell)
				network.append(connected_cell)
				explored[connected_cell.index()] = True
		return network


	def starting_cases(self):
		if not self.locked:
			if self.type == "line":
				neighbors = self.neighbors()
				for i in range(2):
					if neighbors[i].type == "dead" and neighbors[i+2].type == "dead":

						if self.state[i] == True:
							self.rotate()
						self.lock()
						break

				for i in range(4):
					if neighbors[i].type == "line" and neighbors[(i+2)%4].type == "dead":

						if neighbors[i].neighbors()[i].type == "dead":
							if self.state[i] == True:
								self.rotate()
							self.lock()
							break


	def count_valid_orientations(self):
		if self.locked:
			print "counted valid orientations of locked cell"
			return 1
		
		counter = 0
		valid_states = []

		if self.type == "line":
			for direction in range(2):
				if self.matched():
					counter += 1
					valid_states.append(self.state)
				self.rotate(True)

		else: #"split", "turn", "dead"
			for direction in range(4):
				if self.matched():
					counter += 1
					valid_states.append(self.state)
				self.rotate(True)

		#if connection is consistent throughout all valid states, set its value
		for direction in range(4):
			if sum([state[direction] == True for state in valid_states]) == len(valid_states):
				self.connections[direction] = True
			elif sum([state[direction] == False for state in valid_states]) == len(valid_states):
				self.connections[direction] = False
		return counter

	#current state matches up with connections of surrounding cells
	def matched(self):
		for direction in range(4):
			if self.connections[direction] != None:
				if self.connections[direction] != self.state[direction]:	
					return False
		return True

	def check_connections(self):
		if not self.locked and self.count_valid_orientations() == 1:
			while not self.matched():
				self.rotate()
			self.lock()
			self.update_neighbors_connections()



#get puzzle info from webpage
html_table = browser.find_element_by_id('puzzlediv')
html_puzzle = [html_row.find_elements_by_tag_name('td') for html_row in html_table.find_elements_by_tag_name('tr')]
p = Network_Puzzle(html_puzzle)

p.solve()