class Face:
	def __init__(self, size, label):
		self.cells = [label] * size * size
		self.label = label
		self.size = size
		
	def isSingleFace(self):
		return all(c == self.label for c in self.cells)
	
	def getState(self):
		return list(self.cells)
	
	def getRow(self, row):
		"""
		Get a row of labels into a list
		row: row index
		return: list of labels
		"""
		return self.cells[row*self.size:row*self.size+self.size]
	
	def replaceRow(self, row, val):
		"""
		Replace labels of a row by list of values provided
		row: row index
		val: list new values (should have same size as row length)
		"""
		self.cells[row*self.size:row*self.size+self.size] = val
	
	def getColumn(self, col):
		"""
		Get a column of labels into a list
		col: column index
		return: list of labels
		"""
		return [self.cells[r*self.size+col] for r in range(self.size)]

	def replaceColumn(self, col, val):
		"""
		Replace labels of a column by list of values provided
		col: column index
		val: list new values (should have same size as column length)
		"""
		for r in range(len(val)):
			self.cells[r*self.size+col] = val[r]
		
	def rotateClockwise(self):
		"""
		Rotate labels clockwise
		"""
		temp = [self.getColumn(c)[::-1] for c in range(self.size)]
		# one line code: self.cells = [item for sublist in temp for item in sublist]
		for row in range(self.size):
			self.replaceRow(row, temp[row])

	def rotateAntiClockwise(self):
		"""
		Rotate labels anticlockwise
		"""
		temp = [self.getColumn(c) for c in range(self.size)][::-1]
		# one line code: self.cells = [item for sublist in temp for item in sublist]
		for row in range(self.size):
			self.replaceRow(row, temp[row])
	
class Cube:
	# ['plane anti-clockwise', 'plane clockwise', 'row left', 'row right', 'column up', 'column down']
	actions = ['PA', 'PC', 'RL', 'RR', 'CU', 'CD']

	def __init__(self, size=3):
		# [front, top, left, bottom, right, back]
		self.faces = [Face(size, str(i)) for i in range(6)]
		self.size = size

	def __str__(self):
		s = "      +-+-+-+      \n"\
		  + "      |" + " ".join(self.faces[1].getRow(0)) + "|      \n"\
		  + "      |" + " ".join(self.faces[1].getRow(1)) + "|      \n"\
		  + "      |" + " ".join(self.faces[1].getRow(2)) + "|      \n"\
		  + "+-+-+-+-+-+-+-+-+-+\n"\
		  + "|" + " ".join(self.faces[2].getRow(0)) + "|" + " ".join(self.faces[0].getRow(0)) + "|" + " ".join(self.faces[4].getRow(0)) + "|\n"\
		  + "|" + " ".join(self.faces[2].getRow(1)) + "|" + " ".join(self.faces[0].getRow(1)) + "|" + " ".join(self.faces[4].getRow(1)) + "|\n"\
		  + "|" + " ".join(self.faces[2].getRow(2)) + "|" + " ".join(self.faces[0].getRow(2)) + "|" + " ".join(self.faces[4].getRow(2)) + "|\n"\
		  + "+-+-+-+-+-+-+-+-+-+\n"\
		  + "      |" + " ".join(self.faces[3].getRow(0)) + "|      \n"\
		  + "      |" + " ".join(self.faces[3].getRow(1)) + "|      \n"\
		  + "      |" + " ".join(self.faces[3].getRow(2)) + "|      \n"\
		  + "      +-+-+-+      \n"\
		  + "      |" + " ".join(self.faces[5].getRow(0)) + "|      \n"\
		  + "      |" + " ".join(self.faces[5].getRow(1)) + "|      \n"\
		  + "      |" + " ".join(self.faces[5].getRow(2)) + "|      \n"\
		  + "      +-+-+-+      \n"
		return s
	
	def getState(self):
		pass
		
	def suffule(self):
		pass
	
	def movePA(self, i):
		"""
		plane(i) rotate anti-clockwise (left)
		"""
		temp = {2:self.faces[1].getRow(self.size-1-i)[::-1],
		3:self.faces[2].getColumn(self.size-1-i),
		4:self.faces[3].getRow(i)[::-1],
		1:self.faces[4].getRow(i)}
		
		self.faces[1].replaceRow(self.size-1-i, temp[1])
		self.faces[2].replaceColumn(self.size-1-i, temp[2])
		self.faces[3].replaceRow(i, temp[3])
		self.faces[4].replaceColumn(i, temp[4])
		
		if i == 0:
			self.faces[0].rotateAntiClockwise()
			
		if i == self.size-1:
			self.faces[5].rotateAntiClockwise()
	
	def movePC(self, i):
		"""
		plane(i) rotate clockwise (right)
		"""
		temp = {4:self.faces[1].getRow(size-1-i),
		1:self.faces[2].getColumn(self.size-1-i)[::-1],
		2:self.faces[3].getRow(i),
		3:self.faces[4].getRow(i)[::-1]}
		
		self.faces[1].replaceRow(self.size-1-i, temp[1])
		self.faces[2].replaceColumn(self.size-1-i, temp[2])
		self.faces[3].replaceRow(i, temp[3])
		self.faces[4].replaceColumn(i, temp[4])
		
		if i == 0:
			self.faces[0].rotateClockwise()
			
		if i == self.size-1:
			self.faces[5].rotateClockwise()
		
	def moveRL(self, i):
		"""
		row(i) rotate left
		"""
		temp = {2:self.faces[0].getRow(i),
		5:self.faces[2].getRow(i)[::-1],
		4:self.faces[5].getRow(self.size-1-i)[::-1],
		0:self.faces[4].getRow(i)}
		
		self.faces[0].replaceRow(i, temp[0])
		self.faces[2].replaceRow(i, temp[2])
		self.faces[4].replaceRow(i, temp[4])
		self.faces[5].replaceRow(self.size-1-i, temp[5])
		
		if i == 0:
			self.faces[1].rotateAntiClockwise()
			
		if i == self.size-1:
			self.faces[3].rotateAntiClockwise()

	def moveRR(self, i):
		"""
		row(i) rotate right
		"""
		temp = {4:self.faces[0].getRow(i),
		0:self.faces[2].getRow(i),
		2:self.faces[5].getRow(self.size-1-i)[::-1],
		5:self.faces[4].getRow(i)[::-1]}
		
		self.faces[0].replaceRow(i, temp[0])
		self.faces[2].replaceRow(i, temp[2])
		self.faces[4].replaceRow(i, temp[4])
		self.faces[5].replaceRow(self.size-1-i, temp[5])
		
		if i == 0:
			self.faces[1].rotateClockwise()
			
		if i == self.size-1:
			self.faces[3].rotateClockwise()
			
	def moveCU(self, i):
		"""
		column(i) rotate up
		"""
		temp = {1:self.faces[0].getColumn(i),
		0:self.faces[3].getColumn(i),
		3:self.faces[5].getColumn(i),
		5:self.faces[1].getColumn(i)}
		
		self.faces[0].replaceColumn(i, temp[0])
		self.faces[1].replaceColumn(i, temp[1])
		self.faces[3].replaceColumn(i, temp[3])
		self.faces[5].replaceColumn(i, temp[5])
		
		if i == 0:
			self.faces[2].rotateAntiClockwise()
			
		if i == self.size-1:
			self.faces[4].rotateClockwise()
			
	def moveCD(self, i):
		"""
		column(i) rotate down
		"""
		temp = {3:self.faces[0].getColumn(i),
		5:self.faces[3].getColumn(i),
		1:self.faces[5].getColumn(i),
		0:self.faces[1].getColumn(i)}
		
		self.faces[0].replaceColumn(i, temp[0])
		self.faces[1].replaceColumn(i, temp[1])
		self.faces[3].replaceColumn(i, temp[3])
		self.faces[5].replaceColumn(i, temp[5])
		
		if i == 0:
			self.faces[2].rotateClockwise()
			
		if i == self.size-1:
			self.faces[4].rotateAntiClockwise()

			
if __name__ == '__main__':
	cube = Cube()
	cube.movePA(0)
	print cube
	cube.moveRR(2)
	print cube
	