import inspect
from puzzleClass import Puzzle, Cell
	
#initiate selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
browser = webdriver.Chrome()


#open 'root' webpage
browser.set_window_position(750, 0)
url = 'https://www.brainbashers.com/shownetwork.asp?date=0114&size=12&diff=NOWRAP'
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_id('puzzlediv'))
check_button = browser.find_element_by_xpath("//*[@id='puzzleContainer']/tbody/tr/td/p[2]/a[5]")

def e():
	browser.quit()


class Network_Puzzle(Puzzle):

	def __init__(self, array):

		self.height = len(array)
		self.width = len(array[0])

		#initiate cells
		for y, row, in enumerate(array):
			for x, element in enumerate(row):
				self.cells.append(Number_Cell(self, element, y, x))


		if url.split("=")[-1] == "NOWRAP":

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

			#no wrap, so boarder of puzzle cannot be connections
			for index, cell in enumerate(self.cells):
				y,x = self.to_coordinates(index)
				if y == 0:
					cell.known_connections[0] = False
				if y == self.height - 1:
					cell.known_connections[2] = False
				if x == self.width - 1:
					cell.known_connections[1] = False
				if x == 0:
					cell.known_connections[3] = False


		elif url.split("=")[-1] == "WRAP":

			#connect cells
			for index, cell in enumerate(self.cells):
				y,x = self.to_coordinates(index)
				cell.up = self.cells[self.to_index((y - 1) % self.height, x)]
				cell.down = self.cells[self.to_index((y + 1) % self.height, x)]
				cell.right = self.cells[self.to_index(y, (x + 1) % self.width)]
				cell.left = self.cells[self.to_index(y, (x - 1) % self.width)]




class Number_Cell(Cell):
	type = "number"
	def __init__(self, puzzle, hmtl_cell, y, x):

		gif_name = hmtl_cell.find_element_by_tag_name("img").get_attribute("src")[-5:-4]
		#4 types of cells: dead (end), line, turn, split

		#dead: 1 connection, 3 non-connection
			#right 	1
			#up		2
			#left	4
			#down	8
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

		#line: 2 opposing connections, 2 opposing non-connections
			#right/left 	5
			#up/down		a
		elif gif_name == "5":
			self.state = [False, True, False, True]
			self.type = "line"
		elif gif_name == "a":
			self.state = [True, False, True, False]
			self.type = "line"

		#turn: 2 adjacent connections, 2 adjacent non-connections
			#ur 	3
			#rd		9
			#dl		c
			#lu		6
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

		#split. 1 non-conncection, 3 connections
			#right 	e
			#up		d
			#left	b
			#down	7
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

		self.known_connections = [None, None, None, None]
		self.locked = False
		self.puzzle = puzzle
		self.y = y
		self.x = x
		self.up = None
		self.down = None
		self.right = None
		self.left = None

	#only applies to unlocked cells
	def rotate(self):
		self.state = self.state[1:] + [self.state[0]]
		html_puzzle[self.y][self.x].click()

	def opposite_direction(self, index):
		return (index + 2) % 4

	def neighbors_with_index(self):
		return [pair for pair in [[self.up, 0], [self.right, 1], [self.down, 2], [self.left, 3]] if pair[0]]

	def lock(self):
		if self.locked:
			return
		self.locked = True
		self.known_connections = self.state
		self.update_known_connections()
		hover = ActionChains(browser).move_to_element(html_puzzle[self.y][self.x]).send_keys(" ")
		hover.perform()

		# check_button.click()
		# if browser.find_element_by_id("showtext").find_element_by_tag_name("span").get_attribute("class") == "sred":
		# 	print "y:", self.y, "x:", self.x, inspect.stack()[1][3]
		# 	asdf

		for neighbor in self.neighbors():
			if not neighbor.locked:
				neighbor.check_connections()

	def update_known_connections(self):
		for neighbor, direction_index in self.neighbors_with_index():
			if self.known_connections[direction_index] != None:
				neighbor.known_connections[self.opposite_direction(direction_index)] = self.known_connections[direction_index]


	def check_separate_network(self):

		#necesaary # of connections minus # of known connections == 1
		if sum(self.state) - len([c for c in self.known_connections if c == True]) == 1:

			#check that known connections lead to dead ends
			#if only unlocked cell in network is itself, then this is true
			if len([cell for cell in self.explore() if not cell.locked]) == 1:

				#none connections can't lead to a dead end 
				for neighbor, direction_index in self.neighbors_with_index():
					if self.known_connections[direction_index] == None and neighbor.type == "dead":
						self.known_connections[direction_index] = False
						neighbor.known_connections[self.opposite_direction(direction_index)] = False

	def check_closed_loop(self):

		for neighbor, direction_index in self.neighbors_with_index():
			if not neighbor.locked:
				if neighbor in self.explore():

					if self.known_connections[direction_index] != True and neighbor.known_connections[self.opposite_direction(direction_index)] != True:
						self.known_connections[direction_index] = False
						neighbor.known_connections[self.opposite_direction(direction_index)] = False
	




	def connected_neighbors(self):
		return [neighbor for neighbor, index in self.neighbors_with_index() if self.known_connections[index] == True] 

	#get all reachable cells in network
	def explore(self):
		explored = [False for cell in self.puzzle.cells]
		exploration_list = [self]

		network = [self]
		explored[self.index()] = True

		while len(exploration_list) > 0:

			network_cell = exploration_list.pop()

			for connected_cell in network_cell.connected_neighbors():

				if explored[connected_cell.index()]:
					continue

				exploration_list.append(connected_cell)
				network.append(connected_cell)
				explored[connected_cell.index()] = True
		return network

	#check 
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



	def check_connections(self):

		if not self.locked:

			#orientation of a line cell can be determined if any connection or non-connection is known
			if self.type == "line":
				for i in range(4):
					if self.known_connections[i] != None:
						if not self.known_connections[i] == self.state[i]:
							self.rotate()
						self.lock()
						break

			#orientation of a split cell can be determined if location of 1 non-connection is known or if those of 3 connections are known
			elif self.type == "split":
				if len([connect for connect in self.known_connections if connect == True]) == 3:
					for i in range(4):
						if self.known_connections[i] != True:
							while self.state[i] != False:
								self.rotate()
							self.lock()
							break

				else:
					for i in range(4):
						if self.known_connections[i] == False:
							while self.state[i] != False:
								self.rotate()
							self.lock()
							break

			#similarly, orientation of a deadend cell can be determined if location of 1 connection is known or if those of 3 non-connections are known
			elif self.type == "dead":
				if len([connect for connect in self.known_connections if connect == False]) == 3:
					for i in range(4):
						if self.known_connections[i] != False:
							while self.state[i] != True:
								self.rotate()
							self.lock()
							break

				else:
					for i in range(4):
						if self.known_connections[i] == True:
							while self.state[i] != True:
								self.rotate()
							self.lock()
							break

			elif self.type == "turn":

				#orientation is determined if 2 connections are known, or 2 non-connections
				if len([connect for connect in self.known_connections if connect == False]) == 2:
					#rotate until correct, lock
					count = 0
					while count != 2:
						self.rotate()
						count = 0
						for i in range(4):
							if self.known_connections[i] == False and self.state[i] == False:
								count += 1
					self.lock()

				elif len([connect for connect in self.known_connections if connect == True]) == 2:
					#rotate until correct, lock
					count = 0
					while count != 2:
						self.rotate()
						count = 0
						for i in range(4):
							if self.known_connections[i] == True and self.state[i] == True:
								count += 1
					self.lock()
					

				#the location of a connection or non-connection is known, the opposing side must be of the opposite state
				elif len([connect for connect in self.known_connections if connect == True]) == 1:
					#change opposite side to non connection
					for i in range(4):
						if self.known_connections[i] == True:
							self.known_connections[(i+2)%4] = False

					self.update_known_connections()

				elif len([connect for connect in self.known_connections if connect == False]) == 1:
					#change opposite side to connection
					for i in range(4):
						if self.known_connections[i] == False:
							self.known_connections[(i+2)%4] = True
					self.update_known_connections()


#get puzzle info from webpage
html_table = browser.find_element_by_id('puzzlediv')
html_puzzle = [html_row.find_elements_by_tag_name('td') for html_row in html_table.find_elements_by_tag_name('tr')]
puzzle = Network_Puzzle(html_puzzle)


i = 0
while browser.find_element_by_id("showtext").text.find("Puzzle Solved") == -1 and i<20:
	for c in puzzle.cells:
		if not c.locked:

			if url.split("=")[-1] == "WRAP":
				c.starting_cases()
	
			c.check_connections()
			c.check_separate_network()
			c.check_closed_loop()
	i+=1
print i

if browser.find_element_by_id("showtext").text.find("Puzzle Solved") > -1:
	e()



