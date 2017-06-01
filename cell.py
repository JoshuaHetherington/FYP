class cell:
	idNum = 0

	def __init__(self, centrePos, current, start, end):
		cell.idNum += 1
		self.centrePos = centrePos
		self.id = cell.idNum
		self.current = current
		self.start = start
		self.end = end
		self.actions = [0.0, 0.0, 0.0]

		
		
	
