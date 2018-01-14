import sys
#initiate selenium
from selenium import webdriver
browser = webdriver.Chrome()

#open 'root' webpage
url = 'https://www.brainbashers.com/showbattleships.asp?date=1208&puzz=A&size=15'
browser.get(url) 

#get puzzle info from webpage
html_table = browser.find_element_by_id('puzzlediv')

table_rows = [html_row.find_elements_by_tag_name('td')[1:-1] for html_row in html_table.find_elements_by_tag_name('tr')[1:-1]]
table_columns = [[row[x] for row in table_rows] for x in range(len(table_rows[1]))]

puzzle_size = len(table_rows)

column_hints =  [element.text.encode("ASCII") for element in html_table.find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1:]]

row_hints = [row.find_element_by_tag_name('td').text.encode("ASCII").strip() for row in html_table.find_elements_by_tag_name('tr')[1:]]

print column_hints
print row_hints


def get_status(cell):
	return cell.find_element_by_tag_name('img').get_attribute("src")[-5:-4]
# 1: 1-celld ship
# X: empty cell (sea)
# 0: grey (undecided)




def count_ship(row):
	return sum([not (get_status(cell) == "X" or get_status(cell) == "0") for cell in row])



#if the number of ship cells in a row is equal to the number of hints, fill in the rest of the squares with sea
def hint_fufilled(row_index, row_type):
	row = table_rows[row_index] if row_type == "row" else table_columns[row_index]	
	hint_list = row_hints[row_index] if row_type == "row" else column_hints[row_index]
	print row_index
	if count_ship(row) == int(hint_list[row_index]):

		for cell_index, cell in enumerate(row):

			if get_status(cell) == "0":
				cell.click()



for row_index, row in enumerate(table_rows):
	print len(row)
# 	hint_fufilled(row_index, "row")