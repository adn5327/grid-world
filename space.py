class space(object):

	def __init__(self, reward1 = -0.04):
		self.reward = reward1
		self.expectedUtility = 0
		self.nextUtility = 0
		self.policy = '#'

	def __str__(self):

		# return '[{0:.4f},{0:.4f}]'.format(self.reward, self.expectedUtility)
		# # if self.reward > 0:
		# # 	return '+{0:.2f}'.format(self.reward)
		# # else:
		# # 	return '{0:.2f}'.format(self.reward)
		return self.policy

	def policy_printer(self):
		return self.policy
	def formatted_printer(self):
		return '[{:.4f},{:.4f}]'.format(self.reward, self.expectedUtility)
	def reward_printer(self):
		if self.reward > 0:
			return '+{0:.2f}'.format(self.reward)
		else:
			return '{0:.2f}'.format(self.reward)		




	def is_terminal(self):
		if(self.reward != 0 and self.reward != -.04):
			return True
		else:
			return False

	def is_wall(self):
		if self.reward == 0:
			return True
		return False

	def change_next_utility(self, newUtility):
		self.nextUtility = newUtility

	def change_utility(self, newUtility):
		self.expectedUtility = newUtility

class maze(object):

	def __init__(self, n = 6, discount = .99):
		self.grid = list()
		for i in range(n):
			self.grid.append(list())
			for j in range(n):
				self.grid[i].append(space())

		self.size = n
		self.discount = discount

	def __str__(self):
		ret_str = ''
		for i in range(self.size):
			for j in range(self.size):
				ret_str += '\t' + self.grid[i][j].formatted_printer()
			ret_str += '\n'
		return ret_str

	def policy_printer(self):
		ret_str = ''
		for i in range(self.size):
			for j in range(self.size):
				ret_str += '\t' + self.grid[i][j].policy_printer()
			ret_str += '\n'
		return ret_str		

	def setup(self, listy):

		for entry in listy:
			self.grid[entry[0]][entry[1]].reward = entry[2]



	def update_utilities(self):
		for i in range(self.size):
			for j in range(self.size):
				# print '{' + str(self.grid[i][j].nextUtility) + '}'
				# print '[' + str(self.grid[i][j].expectedUtility) + ']'

				self.grid[i][j].change_utility(self.grid[i][j].nextUtility)
				self.grid[i][j].change_next_utility(0)
	


#TO DO -- ADD PRINT METHODS
