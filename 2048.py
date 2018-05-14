from puzzleClass import Puzzle, Cell

#initiate selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
browser = webdriver.Chrome()

def e():
	browser.quit()


#open webpage
browser.set_window_position(686, 29)
browser.set_window_size(677, 736)
url = "https://gabrielecirulli.github.io/2048/"
browser.get(url)
browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_class_name('game-container'))



a = browser.find_element_by_class_name("tile-container").find_elements_by_class_name("grid-cell")

grid = None


body = browser.find_element_by_tag_name("body")
def up():
	body.send_keys("w")
def down():
	body.send_keys("s")
def right():
	body.send_keys("d")
def left():
	body.send_keys("a")



# def getTiles():
# 	global grid
# 	grid = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]

# 	tiles = browser.find_element_by_class_name("tile-container").find_elements_by_xpath("*")

# 	for tile in tiles:
# 		tile_attributes = tile.get_attribute("class").split(" ")
# 		value = int(tile_attributes[1][5:])
# 		x,y = [int(coord) for coord in tile_attributes[2][14:].split("-")]

# 		grid[y-1][x-1] = value




# for x in range(10):
# 	for i in range(20):
# 		left()
# 		down()
# 		down()
# 		down()
# 		down()


# 	right()

# 	getTiles()
# 	if grid[3][0] == None:
# 		down()
# 	else:
# 		left()

# 	down()
# 	down()
# 	down()


#goal: increase the largest tile on the board
#avoid pressing up at all costs
#




# "tile tile-2 tile-position-1-3 tile-new"
# "tile tile-2 tile-position-2-3"
# "tile tile-4 tile-position-4-3 tile-merged"







class Game(Puzzle):

	def __init__(self):

		self.height = 4
		self.width = 4
		self.grid = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]


		for y, row, in enumerate(array):
			for x, element in enumerate(row):
				self.cells.append(Cell(self, element, y, x))

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





	def get_new_tile(self):
		tiles = browser.find_element_by_class_name("tile-container").find_elements_by_xpath("*")

		for tile in tiles:

			if tile.get_attribute("class")[-3:] == "new":
				tile_attributes = tile.get_attribute("class").split(" ")
				value = int(tile_attributes[1][5:])
				x,y = [int(coord) for coord in tile_attributes[2][14:].split("-")]





	def getTiles(self):
		self.grid = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]

		tiles = browser.find_element_by_class_name("tile-container").find_elements_by_xpath("*")

		for tile in tiles:
			tile_attributes = tile.get_attribute("class").split(" ")
			value = int(tile_attributes[1][5:])
			x,y = [int(coord) for coord in tile_attributes[2][14:].split("-")]

			self.grid[y-1][x-1] = value