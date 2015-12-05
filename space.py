class space(object):

	def __init__(self, reward1 = -0.04):
		self.reward = reward1
		self.expectedUtility = 0
		self.nextUtility = 0
		self.policy = '#'

	def __str__(self):
		return '[{0:.4f},{0:.4f}]'.format(self.reward, self.expectedUtility)
		# if self.reward > 0:
		# 	return '+{0:.2f}'.format(self.reward)
		# else:
		# 	return '{0:.2f}'.format(self.reward)
		# return self.policy

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
				ret_str += '\t' + self.grid[i][j].__str__()
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
	
	def value_iteration(self, iterations = 50, terminal = True):
		def action_utility(space, destination):
			spaces = list()
			spaces.append(destination)
			if space[0] == destination[0]:
				spaces.append((space[0] + 1, space[1], .1))
				spaces.append((space[0] - 1, space[1], .1))
			else:
				spaces.append((space[0], space[1] + 1, .1))
				spaces.append((space[0], space[1] - 1, .1))
			cur_utility = 0
			for cur_destination in spaces:
				if (cur_destination[0] == self.size) or (cur_destination[1] == self.size) or (cur_destination[0] < 0) or (cur_destination[1] < 0) or (self.grid[cur_destination[0]][cur_destination[1]].is_wall()):
					cur_utility += 0
				else:
					cur_utility += (self.grid[cur_destination[0]][cur_destination[1]].expectedUtility * cur_destination[2])
			return cur_utility

		def utility(spacey):
			cur_y, cur_x = spacey[0], spacey[1]
			actions = [(cur_y, cur_x + 1, .8), (cur_y, cur_x - 1, .8), (cur_y + 1, cur_x, .8), (cur_y - 1, cur_x, .8)]
			utilities = list()
			for action in actions:
				utilities.append(action_utility(spacey, action))
			result = self.grid[cur_y][cur_x].reward + (self.discount * max(utilities))
			# print result
			return result

		for n in range(iterations):
			for i in range(self.size):
				for j in range(self.size):
					self.grid[i][j].change_next_utility(utility((i,j)))
			self.update_utilities()

		print (self)
		return self


#TO DO -- ADD PRINT METHODS
