from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
url = 'https://www.brainbashers.com/showabcpath.asp?date=1226'
browser.get(url) 


#get puzzle info from webpage
html_table = [html_row.find_elements_by_tag_name('td') for html_row in browser.find_element_by_class_name('futoshikitable').find_elements_by_tag_name('tr')]
puzzle_rows_with_hints = [[row[0]] + row[1:-1:2] + [row[-1]] for row in [html_table[0]] + html_table[1::2]]
puzzle_rows = [row[1:-1] for row in puzzle_rows_with_hints[1:-1]]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"


#don't need this??	
def clue_type(cell):
	#8 kinds of arrows / ints
	#up 		1
	#up-right 	2
	#right  	3
	#down-right	4
	#down 		5
	#down-left	6
	#left 		7
	#up-left	8
	return cell.find_element_by_tag_name("img").get_attribute("src")[-6]






def clue_letter(cell):
	return cell.find_element_by_tag_name("img").get_attribute("src")[-5]

def get_letters(cell):
	return cell.find_element_by_tag_name("input").get_attribute("value")

def has_letter(cell, letter):
	return letter in get_letters(cell)

def add_letter(letter, cell):
	input = cell.find_element_by_tag_name("input")
	input.click()
	input.send_keys(letter)


def remove_letter(letter, cell):
	letters = get_letters(cell)
	index = letters.index(letter)
	input = cell.find_element_by_tag_name("input")
	input.clear()
	add_letter(letters[:index]+letters[index+1:], cell)

def adjacent_coordinates(y, x):
	short_list = [[y, x+1], [y, x-1], [y-1, x], [y+1, x], [y+1,x+1], [y-1,x-1], [y+1,x-1], [y-1,x+1]]
	return [[y_prime, x_prime] for y_prime, x_prime in short_list if 0 <= x_prime <= (5 - 1) and 0 <= y_prime <= (5 - 1)]



def previous_letter(letter):
	return alphabet[alphabet.index(letter)-1]

def	next_letter(letter):
	return alphabet[alphabet.index(letter)+1]


def add_letter_if_previous_adjacent(letter, cell, row_index, cell_index):
	for y_adjacent, x_adjacent in adjacent_coordinates(row_index, cell_index):
		adjacent_cell = puzzle_rows[y_adjacent][x_adjacent] 
		if has_letter(adjacent_cell, previous_letter(letter)):
			add_letter(letter, cell)
			break

def right_arrow(y, letter):
	for row_index, row in enumerate(puzzle_rows):
		for cell_index, cell in enumerate(row):
			if row_index == y:
				add_letter_if_previous_adjacent(letter, cell, row_index, cell_index)

def up_arrow(x, letter):
	for row_index, row in enumerate(puzzle_rows):
		for cell_index, cell in enumerate(row):
			if cell_index == x:
				add_letter_if_previous_adjacent(letter, cell, row_index, cell_index)

def up_right_arrow(letter):
	for row_index, row in enumerate(puzzle_rows):
		for cell_index, cell in enumerate(row):
			if row_index + cell_index == 4:
				add_letter_if_previous_adjacent(letter, cell, row_index, cell_index)
				
def up_left_arrow(letter):
	for row_index, row in enumerate(puzzle_rows):
		for cell_index, cell in enumerate(row):
			if row_index == cell_index:
				add_letter_if_previous_adjacent(letter, cell, row_index, cell_index)



#store hints and their coordinates
hint_coordinates = {}
for row_index, row in enumerate(puzzle_rows_with_hints):
	for cell_index, cell in enumerate(row):
		try:
			hint_coordinates[clue_letter(cell)] = [row_index, cell_index]	
		except Exception as e:
			pass


def run():

	# iterate through letters of the alphabet.
	for letter in alphabet[1:]:
		y, x = hint_coordinates[letter]

		#
		if y == x:
			up_left_arrow(letter)
		elif y + x == 6:
			up_right_arrow(letter)
		elif y == 0 or y == 6:
			up_arrow(x-1, letter)
		elif x == 0 or x == 6:
			right_arrow(y-1, letter)


run()






# if a letter only exists in one place in the whole puzzle. set it location to that letter, delete all other instances of that letter

for row_index, row in enumerate(puzzle_rows):
	for cell_index, cell in enumerate(row):
		letters = get_letters(cell)
		if len(letters) == 1:
			for row_index2, row2 in enumerate(puzzle_rows):
				#nned to fix indexes
				for cell_index2, cell2 in enumerate(row):
					if [row_index, cell_index] != [row_index2, cell_index2]:

						if has_letter(cell2, letters):
							remove_letter(letters, cell2)




# 	for each letter, find the hint location on the border of teh puzzle. for each hint locadtion there are 5 potental possible locations for the letter

# add the letter to each of those locations if it is adjacent to the prior letter.
	
# check previous letter to see if it is still adjacent to current letter??

# if any locations or eliminated, check the priovious letter to see if any of its locations can be eliminated
# 		if so, check the previous, previous element, continue checking if changes are made

# if any cell contains only one letter, delete all other instances of that letter.
# 	when deletions are made, check prior and following letters possiblilties to see if they are still adjacent to deleted letter. 






