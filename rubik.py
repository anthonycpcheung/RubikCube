import random

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
	
	def getTopLeftConer(self):
		return self.cells[0]
		
	def getTopRightConer(self):
		return self.cells[self.size-1]
		
	def getBottomLeftConer(self):
		return self.cells[(self.size-1)*self.size]
		
	def getBottomRightConer(self):
		return self.cells[(self.size-1)*self.size+(self.size-1)]
		
	def getTopEdgeCell(self, i):
		return self.cells[i]
		
	def getLeftEdgeCell(self, i):
		return self.cells[i*self.size]
		
	def getBottomEdgeCell(self, i):
		return self.cells[(self.size-1)*self.size+i]
	
	def getRightEdgeCell(self, i):
		return self.cells[i*self.size+(self.size-1)]
	
class Cube:
	# ['plane anti-clockwise', 'plane clockwise', 'row left', 'row right', 'column up', 'column down']
	actions = ['PA', 'PC', 'RL', 'RR', 'CU', 'CD']

	def __init__(self, size=3):
		# [front, top, left, bottom, right, back]
		self.faces = [Face(size, str(i)) for i in range(6)]
		self.size = size

	def __str__(self):
		hedge = "+".join(["-"]*self.size)
		spaces = " " * (len(hedge) + 1)
		s = spaces + "+" + hedge + "+" + spaces + "\n"
		for i in range(self.size):
			s += spaces + "|" + " ".join(self.faces[1].getRow(i)) + "|" + spaces + "\n"
		s += "+" + hedge + "+" + hedge + "+" + hedge + "+\n"
		for i in range(self.size):
			s += "|" + " ".join(self.faces[2].getRow(i)) + "|" + " ".join(self.faces[0].getRow(i)) + "|" + " ".join(self.faces[4].getRow(i)) + "|\n"
		s += "+" + hedge + "+" + hedge + "+" + hedge + "+\n"
		for i in range(self.size):
			s += spaces + "|" + " ".join(self.faces[3].getRow(i)) + "|" + spaces + "\n"
		s += " " + " " * len(hedge) + "+" + hedge + "+" + " " * len(hedge) + " \n"
		for i in range(self.size):
			s += spaces + "|" + " ".join(self.faces[5].getRow(i)) + "|" + spaces + "\n"
		s += spaces + "+" + hedge + "+" + spaces + "\n"
		return s
	
	def validate(self):
		fs = [f.getState() for f in self.faces]

		# count number of labels
		counter = {}
		for s in fs:
			for l in s:
				counter.setdefault(l, 0)
				counter[l] += 1
		assertLabelCount = all(counter[l] == self.size**2 for l in counter)
		if not assertLabelCount:
			print counter

		# count coners
		conerList = []
		conerList.append(tuple(sorted([self.faces[0].getTopLeftConer(), self.faces[1].getBottomLeftConer(), self.faces[2].getTopRightConer()])))
		conerList.append(tuple(sorted([self.faces[0].getTopRightConer(), self.faces[1].getBottomRightConer(), self.faces[4].getTopLeftConer()])))
		conerList.append(tuple(sorted([self.faces[0].getBottomLeftConer(), self.faces[2].getBottomRightConer(), self.faces[3].getTopLeftConer()])))
		conerList.append(tuple(sorted([self.faces[0].getBottomRightConer(), self.faces[3].getTopRightConer(), self.faces[4].getBottomLeftConer()])))
		conerList.append(tuple(sorted([self.faces[5].getTopLeftConer(), self.faces[2].getBottomLeftConer(), self.faces[3].getBottomLeftConer()])))
		conerList.append(tuple(sorted([self.faces[5].getTopRightConer(), self.faces[3].getBottomRightConer(), self.faces[4].getBottomRightConer()])))
		conerList.append(tuple(sorted([self.faces[5].getBottomLeftConer(), self.faces[1].getTopLeftConer(), self.faces[2].getTopLeftConer()])))
		conerList.append(tuple(sorted([self.faces[5].getBottomRightConer(), self.faces[1].getTopRightConer(), self.faces[4].getTopRightConer()])))
		assertConerCount = len(set(conerList)) == 8
		if not assertConerCount:
			print conerList
		
		# count edges
		if self.size > 2:
			counter = {} 
		for i in range(1,self.size-1):
			e = tuple(sorted([self.faces[0].getTopEdgeCell(i), self.faces[1].getBottomEdgeCell(i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[0].getLeftEdgeCell(i), self.faces[2].getRightEdgeCell(i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[0].getBottomEdgeCell(i), self.faces[3].getTopEdgeCell(i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[0].getRightEdgeCell(i), self.faces[4].getLeftEdgeCell(i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[5].getTopEdgeCell(i), self.faces[3].getBottomEdgeCell(i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[5].getLeftEdgeCell(i), self.faces[2].getLeftEdgeCell(self.size-1-i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[5].getBottomEdgeCell(i), self.faces[1].getTopEdgeCell(i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[5].getRightEdgeCell(i), self.faces[4].getRightEdgeCell(self.size-1-i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[2].getTopEdgeCell(i), self.faces[1].getLeftEdgeCell(i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[2].getBottomEdgeCell(i), self.faces[3].getLeftEdgeCell(self.size-1-i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[4].getTopEdgeCell(i), self.faces[1].getRightEdgeCell(self.size-1-i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
			e = tuple(sorted([self.faces[4].getBottomEdgeCell(i), self.faces[3].getRightEdgeCell(i)]))
			counter.setdefault(e, 0)
			counter[e] += 1
		assertEdgeCount = all(counter[e] == self.size-2 for e in counter)
		if not assertEdgeCount:
			print counter
		
		return assertLabelCount and assertConerCount and assertEdgeCount
		
	def shuffle(self, minSteps=50, maxSteps=100, showSteps=False):
		stepsRange = (minSteps, maxSteps)
		steps = [(self.actions[random.randint(0, len(self.actions)-1)], random.randint(0, self.size-1)) for i in range(random.randint(*stepsRange))]

		for (act, idx) in steps:
			self.move(act, idx)
			if not self.validate():
				print act, "has error"
			if showSteps:
				print act, idx, '\n', self
		
		return steps
		
	def move(self, act, idx):
		if act == 'PA':
			self.movePA(idx)
		elif act == 'PC':
			self.movePC(idx)
		elif act == 'RL':
			self.moveRL(idx)
		elif act == 'RR':
			self.moveRR(idx)
		elif act == 'CU':
			self.moveCU(idx)
		elif act == 'CD':
			self.moveCD(idx)
		else:
			raise ValueError()
	
	def movePA(self, i):
		"""
		plane(i) rotate anti-clockwise (left)
		"""
		temp = {1:self.faces[4].getColumn(i),
		2:self.faces[1].getRow(self.size-1-i)[::-1],
		3:self.faces[2].getColumn(self.size-1-i),
		4:self.faces[3].getRow(i)[::-1]}
		
		self.faces[1].replaceRow(self.size-1-i, temp[1])
		self.faces[2].replaceColumn(self.size-1-i, temp[2])
		self.faces[3].replaceRow(i, temp[3])
		self.faces[4].replaceColumn(i, temp[4])
		
		if i == 0:
			self.faces[0].rotateAntiClockwise()
			
		if i == self.size-1:
			self.faces[5].rotateClockwise()
	
	def movePC(self, i):
		"""
		plane(i) rotate clockwise (right)
		"""
		temp = {1:self.faces[2].getColumn(self.size-1-i)[::-1],
		2:self.faces[3].getRow(i),
		3:self.faces[4].getColumn(i)[::-1],
		4:self.faces[1].getRow(self.size-1-i)}
		
		self.faces[1].replaceRow(self.size-1-i, temp[1])
		self.faces[2].replaceColumn(self.size-1-i, temp[2])
		self.faces[3].replaceRow(i, temp[3])
		self.faces[4].replaceColumn(i, temp[4])
		
		if i == 0:
			self.faces[0].rotateClockwise()
			
		if i == self.size-1:
			self.faces[5].rotateAntiClockwise()
		
	def moveRL(self, i):
		"""
		row(i) rotate left
		"""
		temp = {0:self.faces[4].getRow(i),
		2:self.faces[0].getRow(i),
		4:self.faces[5].getRow(self.size-1-i)[::-1],
		5:self.faces[2].getRow(i)[::-1]}
		
		self.faces[0].replaceRow(i, temp[0])
		self.faces[2].replaceRow(i, temp[2])
		self.faces[4].replaceRow(i, temp[4])
		self.faces[5].replaceRow(self.size-1-i, temp[5])
		
		if i == 0:
			self.faces[1].rotateClockwise()
			
		if i == self.size-1:
			self.faces[3].rotateAntiClockwise()

	def moveRR(self, i):
		"""
		row(i) rotate right
		"""
		temp = {0:self.faces[2].getRow(i),
		2:self.faces[5].getRow(self.size-1-i)[::-1],
		4:self.faces[0].getRow(i),
		5:self.faces[4].getRow(i)[::-1]}
		
		self.faces[0].replaceRow(i, temp[0])
		self.faces[2].replaceRow(i, temp[2])
		self.faces[4].replaceRow(i, temp[4])
		self.faces[5].replaceRow(self.size-1-i, temp[5])
		
		if i == 0:
			self.faces[1].rotateAntiClockwise()
			
		if i == self.size-1:
			self.faces[3].rotateClockwise()
			
	def moveCU(self, i):
		"""
		column(i) rotate up
		"""
		temp = {0:self.faces[3].getColumn(i),
		1:self.faces[0].getColumn(i),
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
		temp = {0:self.faces[1].getColumn(i),
		1:self.faces[5].getColumn(i),
		3:self.faces[0].getColumn(i),
		5:self.faces[3].getColumn(i)}
		
		self.faces[0].replaceColumn(i, temp[0])
		self.faces[1].replaceColumn(i, temp[1])
		self.faces[3].replaceColumn(i, temp[3])
		self.faces[5].replaceColumn(i, temp[5])
		
		if i == 0:
			self.faces[2].rotateClockwise()
			
		if i == self.size-1:
			self.faces[4].rotateAntiClockwise()

			
if __name__ == '__main__':
	cube = Cube(3)
	cube.validate()
	print cube
	#cube.shuffle(printSteps=True)
	steps = cube.shuffle(minSteps=50, maxSteps=100, showSteps=False)
	print(len(steps))
	print steps
	print cube
	