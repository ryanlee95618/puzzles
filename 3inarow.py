#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
url = 'https://www.brainbashers.com/show3inarow.asp?date=1207&diff=1&size=10'
browser.get(url) 

table = [[html_cell for html_cell in html_row.find_elements_by_tag_name('td')[:-1]] for html_row in browser.find_element_by_id('puzzlediv').find_elements_by_tag_name('tr')[1:]]


def isWhite(cell):
	return cell.get_attribute('class').find('white')>-1
def isBlack(cell):
	return cell.get_attribute('class').find('black')>-1


#check if two cells are same color
def are_the_same_color(a,b):

	if isBlack(a) and isBlack(b):
		return 'black'
	elif isWhite(a) and isWhite(b):
		return 'white'
	else:
		return None
	

def click_value(string,x,y):
	if string == 'white':
		print 'CLICK'
		table[y][x].click()
	elif string == 'black':
		print 'CLICK'
		table[y][x].click()
		table[y][x].click()
	else:
		pass


puzzle_height = len(table)
puzzle_width = len(table[1])

#iterate over every cell and check 2 cells above, below, right, and left to see if they are repeated.
def scan():
	for x in range(puzzle_width):
		for y in range(puzzle_height):
			if table[y][x].get_attribute('class').find('grey')>-1:
				
				#check for repeats above
				if y >= 2:
					same_value = are_the_same_color(table[y-1][x], table[y-2][x])
					click_value(same_value,x,y)

				#check for repeats below
				if y <= puzzle_height-3:
					same_value = are_the_same_color(table[y+1][x], table[y+2][x])
					click_value(same_value,x,y)			
					
				#check for repeats right
				if x <= puzzle_width-3:
					same_value = are_the_same_color(table[y][x+1], table[y][x+2])
					click_value(same_value,x,y)

				#check for repeats left
				if x >= 2:
					same_value = are_the_same_color(table[y][x-1], table[y][x-2])
					click_value(same_value,x,y)










def click_cell(string, cell):
	if cell.get_attribute('class').find('grey')>-1:
		if string == 'white':
			cell.click()
			print 'CLICK'
		elif string == 'black':
			cell.click()
			cell.click()
			print 'CLICK'
		else:
			pass


#look at every group of 3 cells, if 2 are the same, if in the 3rd (if it is grey) with the opposite color
def scan2():
	puzzle_height = len(table)
	puzzle_width = len(table[1])

	for x in range(puzzle_width):
		for y in range(puzzle_height):

			if x < puzzle_width - 2:
			#3 cells to the right (including current cell)
				A,B,C = [table[y][x],table[y][x+1],table[y][x+2]]
				#print A.get_attribute('class'), B.get_attribute('class'), C.get_attribute('class')
				click_cell(are_the_same_color(A,B),C)
				click_cell(are_the_same_color(B,C),A)
				click_cell(are_the_same_color(A,C),B)
			if y < puzzle_height - 2:
			#3 cells below (including current cell)
				A,B,C = [table[y][x],table[y+1][x],table[y+2][x]]
				click_cell(are_the_same_color(A,B),C)
				click_cell(are_the_same_color(B,C),A)
				click_cell(are_the_same_color(A,C),B)






#check for row/columns with only one remaining color to fill
def almost_full():
	#scan rows
	for x in range(puzzle_height):
		row = table[x]
		white_count = sum([isWhite(cell) for cell in row])
		black_count = sum([isBlack(cell) for cell in row])

		if white_count == puzzle_width/2:
			for cell in row:
				click_cell('white', cell)
		elif black_count == puzzle_width/2:
			for cell in row:
				click_cell('black', cell)

	#scan columns
	for y in range(puzzle_width):
		column = [row[y] for row in table]
		white_count = sum([isWhite(cell) for cell in column])
		black_count = sum([isBlack(cell) for cell in column])

		if white_count == puzzle_height/2:
			for cell in column:
				click_cell('white', cell)
		elif black_count == puzzle_height/2:
			for cell in column:
				click_cell('black', cell)

#when a change is made to a cell, check all groups of 3 that contain the cell.
def check_cell(cell):
	pass
	




for i in range(10):
	scan2()
	almost_full()
	print i
	try:
		browser.find_element_by_class_name('sgreen')
		print "DONE!!!!!!!"
		break
	except:
		pass



# for row in table:
# 	previous_cell = " "
# 	repeat_found = False
# 	for cell in row:
# 		if repeat_found:
# 			pass
# 		if cell.get_attribute('class').find(previous_cell) > -1:
# 			pass
# 		previous_cell = cell.get_attribute('class')




# =[[u'inarowgrey', u'inarowfixedblack', u'inarowgrey', u'inarowgrey', u'inarowgrey', u'inarowgrey'], [u'inarowgrey', u'inarowfixedblack', u'inarowgrey', u'inarowgrey', u'inarowfixedblack', u'inarowgrey'], [u'inarowgrey', u'inarowgrey', u'inarowgrey', u'inarowfixedwhite', u'inarowgrey', u'inarowgrey'], [u'inarowgrey', u'inarowfixedblack', u'inarowfixedblack', u'inarowgrey', u'inarowfixedblack', u'inarowgrey'], [u'inarowgrey', u'inarowgrey', u'inarowgrey', u'inarowgrey', u'inarowgrey', u'inarowgrey'], [u'inarowgrey', u'inarowgrey', u'inarowgrey', u'inarowfixedwhite', u'inarowgrey', u'inarowfixedwhite']]



# #inarowfixedwhite inarowwhite
# if cell_state == "inarowblack":
# 	pass
# elif cell_state == "inarowgrey":
# 	html_cell.click()
# elif cell_state == "inarowwhite":
# 	pass