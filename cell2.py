class cell2:
	idNum = 0

	def __init__(self, centrePos, current, start, end):
		cell2.idNum += 1
		self.centrePos = centrePos
		self.id = cell2.idNum
		self.current = current
		self.start = start
		self.end = end
		self.actions = [0.0, 0.0, 0.0, 0.0]

		
		
	
