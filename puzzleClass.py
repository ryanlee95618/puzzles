#this is essentially a doubly linked list extended to 2-dimensions

class Puzzle():
	cells = []
	height = None
	width = None
	
	def __init__(self, array):

		self.height = len(array)
		self.width = len(array[0])
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

	def column(self, n):
		return self.cells[n::self.width]

	def row(self, n):
		return self.cells[n*self.width:(n+1)*self.width]

	# def columns(self):
	# 	return [self.column(i) for i in range(self.width)]

	# def rows(self):
	# 	return [self.row(i) for i in range(self.height)]

	def to_coordinates(self, n):
		return [n/self.width, n%self.width]

	def to_index(self,y,x):
		return y*self.width + x

	def index(self,n):
		return self.cells[n]

	def coord(self,y,x):
		return self.cells[y*self.width + x]


class Cell():

	def __init__(self, puzzle, value, y, x):
	    self.value = value
	    self.puzzle = puzzle
	    self.y = y
	    self.x = x
	    self.up = None
	    self.down = None
	    self.right = None
	    self.left = None

	def neighbors(self):
		return [neighbor for neighbor in [self.up, self.right, self.down, self.left] if neighbor]

	def row(self):
		return self.puzzle.row(self.y)

	def column(self):
		return self.puzzle.column(self.x)

	def index(self):
		return self.puzzle.width*self.y + self.x



# test = [[1,2,3],
# 		[4,5,6],
# 		[7,8,9]]