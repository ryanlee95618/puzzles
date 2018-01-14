#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
url = 'https://www.brainbashers.com/shownonogrid.asp?date=1207&size=20'
browser.get(url) 

#get puzzle info from webpage
html_table = browser.find_element_by_id('puzzlediv')

table_rows = [[html_cell for html_cell in html_row.find_elements_by_tag_name('td')[1:]] for html_row in html_table.find_elements_by_tag_name('tr')[1:]]
table_columns = [[row[x] for row in table_rows] for x in range(len(table_rows[1]))]

puzzle_size = len(table_rows)

column_hints =   [[int(number) for number in list] for list in [hint_list.split("\n") for hint_list in [element.text for element in html_table.find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1:]]]]

row_hints = [[int(number) for number in list] for list in [hint_list.split() for hint_list in [row.find_element_by_tag_name('td').text.encode("ASCII").strip() for row in html_table.find_elements_by_tag_name('tr')[1:]]]]


def get_status(cell):
	return cell.find_element_by_tag_name('img').get_attribute("src")[-5:-4]


def func(row_index, row_type):
#hint: 1 4 1
#puzzle size = 10


#number of leading zeros to the left of hint is sum of hints prior to current hint, plus the number of hints prior to current hint. 
#ex. 1 + 1 = 2

#number of trailer zeros is puzzle size minus # leading zeros minus current hint


#[0 0 1 1 1 1 0 0 0 0]
#[0 0 0 0 1 1 1 1 0 0] 


#[1 0 1 1 1 1 0 1 0 0] everything shifted to left
#[0 0 1 0 1 1 1 1 0 1] to the right
#[0 0 0 0 1 1 0 0 0 0] overlap between the two


	hint_list = row_hints[row_index] if row_type == "row" else column_hints[row_index]
	row = table_rows[row_index] if row_type == "row" else table_columns[row_index]

	wiggle_room = puzzle_size - sum(hint_list) - len(hint_list) + 1

	for index, hint in enumerate(hint_list):	
		if hint > wiggle_room:


			start_index = sum(hint_list[:index]) + len(hint_list[:index])

			for cell_index in range(start_index + wiggle_room, start_index + hint):
				cell = row[cell_index]
				if get_status(cell) == 'n':
					cell.click()


def first_and_last(row_index, row_type):

	hint_list = row_hints[row_index] if row_type == "row" else column_hints[row_index]
	row = table_rows[row_index] if row_type == "row" else table_columns[row_index]

	wiggle_room = puzzle_size - sum(hint_list) - len(hint_list) + 1


	#













for row_index, row in enumerate(table_rows):
	func(row_index, "row")
for column_index, column in enumerate(table_columns):
	func(column_index, "column")