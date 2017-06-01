class cell3:
	idNum = 0

	def __init__(self, centrePos, current, start, end, empty):
		cell3.idNum += 1
		self.centrePos = centrePos
		self.id = cell3.idNum
		self.current = current
		self.start = start
		self.end = end
		self.empty = empty
		self.actions = [0.0, 0.0, 0.0, 0.0]

		
		
	
