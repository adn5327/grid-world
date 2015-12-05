class space(object):

	def __init__(self, reward1 = -0.04):
		self.reward = reward1
		self.expectedUtility = 0

	def __str__(self):
		# return '[{0:.4f},{0:.4f}]'.format(self.reward, self.expectedUtility)
		if self.reward > 0:
			return '+{0:.2f}'.format(self.reward)
		else:
			return '{0:.2f}'.format(self.reward)

class maze(object):

	def __init__(self, n = 6):
		self.grid = list()
		for i in range(n):
			self.grid.append(list())
			for j in range(n):
				self.grid[i].append(space())

		self.size = n

	def __str__(self):
		ret_str = ''
		for i in range(self.size):
			for j in range(self.size):
				ret_str += '\t' + self.grid[i][j].__str__()
			ret_str += '\n'
		return ret_str

	def setup(self, listy):

		for entry in listy:
			self.grid[entry[0]][entry[1]].reward = entry[2]




#TO DO -- ADD PRINT METHODS
