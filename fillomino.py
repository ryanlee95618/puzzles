#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
url = 'https://www.brainbashers.com/showfillomino.asp?date=1214&size=8'
browser.get(url) 


#get puzzle info from webpage
html_table = browser.find_element_by_id('puzzlediv')
table_rows = [html_row.find_elements_by_tag_name('td') for html_row in html_table.find_elements_by_tag_name('tr')]
table_columns = [[row[x] for row in table_rows] for x in range(len(table_rows[1]))]
puzzle_size = len(table_rows)
number_selector = [html_row.find_element_by_tag_name('td') for html_row in browser.find_element_by_id("numberdiv").find_elements_by_tag_name("tr")]


def empty(cell):
	return cell.text == ""

def value(cell):
	return cell.text

#determine if a numbered cell can expand (its group size requirement has not yet been met)
def can_expand(cell):
	return cell.get_attribute("style") == "background-color: rgb(255, 255, 255);" and not empty(cell)



#return list of adjacent cell coordinates within puzzle boarder
def adjacent_coordinates(y, x):
	short_list = [[y, x + 1], [y, x - 1], [y + 1, x], [y - 1, x]]
	return [[y_prime, x_prime] for y_prime, x_prime in short_list if 0 <= x_prime <= (puzzle_size - 1) and 0 <= y_prime <= (puzzle_size - 1)]
	
#make a  test verison of puzzle to be modified for interconnectedness testing
def make_puzzle():
	return  [[html_cell.text for html_cell in  html_row.find_elements_by_tag_name('td')] for html_row in html_table.find_elements_by_tag_name('tr')]

def print_puzzle(puzzle):
	for row in puzzle:
		print " ".join(row)
	print "\n"

#change cell to specified value
def click(cell, n):
	number_selector[n].click()
	cell.click()

#calculate current group size of a cell
def group_size(y_start, x_start):
	puzzle = make_puzzle()
	number = puzzle[y_start][x_start]

	exploration_list = [[y_start, x_start]]
	size = 1
	while len(exploration_list) > 0:

		y,x = exploration_list.pop()
		puzzle[y][x] = 'explored'

		for coordinate in adjacent_coordinates(y,x):
			y_prime, x_prime = coordinate
			if puzzle[y_prime][x_prime] == number:
				exploration_list.append(coordinate)
				size += 1
	return size



#look for non-empty cells that are expandable. 'fill' all adjacent reachable cells of the same value
#keep track of number of adjacent blank cells encountered. if there is only one, change blank cell to value
def one_option(y_start,x_start):

	puzzle = make_puzzle()
	number = puzzle[y_start][x_start]
	exploration_list = [[y_start, x_start]]
	blank_cell_locations = []

	while len(exploration_list) > 0:

		y,x = exploration_list.pop()
		puzzle[y][x] = 'explored'

		for coordinate in adjacent_coordinates(y,x):
			y_prime, x_prime = coordinate
			if puzzle[y_prime][x_prime] == number:
				exploration_list.append(coordinate)
			elif puzzle[y_prime][x_prime] == "":
				puzzle[y_prime][x_prime] = "blank_found" 
				blank_cell_locations.append(coordinate)

	if len(blank_cell_locations) == 1:
		#change blank cell to number
		y_blank, x_blank = blank_cell_locations[0]
		click(table_rows[y_blank][x_blank], int(number))


for y, row in enumerate(table_rows):
	for x, cell in enumerate(row):
		if not empty(cell):
			if can_expand(cell):
				one_option(y, x)


#look for non-empty cells that are expandable. for each adjacent white cell 'fill' other reachable white cells.
#keep track of expandable adjacent cells. if there are none, fill every white cell encountered with the current cell value. 








#look for non-empty cells that are expandable. calculate the maximum number cells a the current cell could expand into. If the maximum plus the number of cells in the group size is equal to the value, then fill all white cells encountered.
def max_space(y_start,x_start):


	#find all whites space that is adjacent to the group of the start cell. 	
	puzzle = make_puzzle()
	number = puzzle[y_start][x_start]

	exploration_list = [[y_start, x_start]]
	adjacent_blank_cells = []
	while len(exploration_list) > 0:

		y,x = exploration_list.pop()
		puzzle[y][x] = 'explored'

		for coordinate in adjacent_coordinates(y,x):
			y_prime, x_prime = coordinate
			if puzzle[y_prime][x_prime] == number:
				exploration_list.append(coordinate)

			elif puzzle[y_prime][x_prime] ==  '':
				adjacent_blank_cells.append(coordinate)



	#'fill' the list of white space to find the most cells the current group could fill.	
	puzzle = make_puzzle()

	white_cell_list = list(adjacent_blank_cells)
	while len(adjacent_blank_cells) > 0:

		y,x = adjacent_blank_cells.pop()
		if puzzle[y][x] == 'explored':
			continue

		puzzle[y][x] = 'explored'

		for coordinate in adjacent_coordinates(y,x):
			y_prime, x_prime = coordinate
			if puzzle[y_prime][x_prime] ==  '':
				adjacent_blank_cells.append(coordinate)

				if not coordinate in white_cell_list:
					white_cell_list.append(coordinate)

	print white_cell_list
	if len(white_cell_list) + group_size(y_start, x_start) == int(number):

		for y,x in white_cell_list:
			click(table_rows[y][x], int(number))



for y, row in enumerate(table_rows):
	for x, cell in enumerate(row):
		if not empty(cell):
			if can_expand(cell):
				max_space(y, x)



	#keep track of which cells have been explored
	#explored = [ [0]*puzzle_size for _ in xrange(puzzle_size)]








asdf











def change_state(y, x, cell_color):

	cell = table_rows[y][x]
 
	#make sure cell value has not already been changed
	if color(cell) != "grey":
		return None

	#when changing state of a cell to white, change all other cells in the same column and row with the same value to black
	if cell_color == "white":
		cell.click()

		#check cells in same row
		for cell_index, cell2 in enumerate(table_rows[y]):
			if value(cell2) == value(cell):
				change_state(y, cell_index, "black")
		
		#check cells in same column
		for cell_index, cell2 in enumerate(table_columns[x]):
			if value(cell2) == value(cell):
				change_state(cell_index, x, "black")

	#when changing a cell to black, change 4 adjacent cells to white.
	elif cell_color == "black":
		cell.click()
		cell.click()

		for coordinate in adjacent_coordinates(y,x):
			y_prime, x_prime = coordinate
			change_state(y_prime, x_prime, "white")

#single whites cells cannot be enclosed by black cells
for y, row in enumerate(table_rows):
	for x, cell in enumerate(row):
		if color(cell) != "white":
			continue
		
		#keep track of how many grey neighbors the current cell has
		grey_neighbor_coordinates = []
		white_neighbor_coordinates = []
		for coordinate in adjacent_coordinates(y,x):
			y_prime, x_prime = coordinate

			if color(table_rows[y_prime][x_prime]) == "grey":
				grey_neighbor_coordinates.append([y_prime, x_prime])
			if color(table_rows[y_prime][x_prime]) == "white":
				white_neighbor_coordinates.append([y_prime,x_prime])

		#if there is one grey neighbor and no white neighbors, the only way for the current cell to be connected to the rest of the puzzle is through the one grey neighbor, so change that neighbor to white.
		if len(grey_neighbor_coordinates) == 1 and len(white_neighbor_coordinates) == 0:
			y_alpha, x_alpha = grey_neighbor_coordinates[0]
			change_state(y_alpha, x_alpha, "white")




#start at a white cell, and fill every other white cell that is reachable. keep track of number of neihboring grey cells encountered. if there is only one encountered, then that is the only way for the reachable white cells to be connected to the rest of the puzzle, so change grey cell to white.
def explore(y_start, x_start, puzzle):

	exploration_list = [[y_start, x_start]]
	grey_cell_locations = []

	while len(exploration_list) > 0: #and len(grey_cell_locations) < 2:

		y,x = exploration_list.pop()
		puzzle[y][x] = 'explored'

		for coordinate in adjacent_coordinates(y,x):
			y_prime, x_prime = coordinate
			if puzzle[y_prime][x_prime] == "white":
				exploration_list.append(coordinate)
			elif puzzle[y_prime][x_prime] == "grey":
				puzzle[y_prime][x_prime] = "grey_found" 
				grey_cell_locations.append(coordinate)

	if len(grey_cell_locations) == 1:
		#change grey cell to white
		y_grey, x_grey = grey_cell_locations[0]
		change_state(y_grey, x_grey, "white")
		print_puzzle(puzzle)





