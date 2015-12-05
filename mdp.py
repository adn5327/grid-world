from space import *

def value_iteration(maze_obj, iterations = 50, terminal = True):
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
			if ((cur_destination[0] == maze_obj.size) \
				|| (cur_destination[1] == maze_obj.size) \
				|| (cur_destination[0] < 0) \
				|| (cur_destination[1] < 0) \
				|| (maze_obj.grid[cur_destination[0]][cur_destination[1].reward == 0)):
				cur_utility += 0
			else:
				cur_utility += (maze_obj.grid[cur_destination[0]][cur_destination[1]].expectedUtility * cur_destination[2])
		return cur_utility

	def utility(spacey):
		cur_y, cur_x = spacey[0], spacey[1]
		actions = [(cur_y, cur_x + 1, .8), (cur_y, cur_x - 1, .8), (cur_y + 1, cur_x, .8), (cur_y - 1, cur_x, .8)]
		utilities = list()
		for action in actions:
			utilities.append(action_utility(spacey, action))
		return maze_obj.grid[cur_y][cur_x].reward + (maze_obj.discount * max(utilities))

	for n in range(iterations):
		for i in range(maze_obj.size):
			for j in range(maze_obj.size):
				maze_obj.grid[i][j].nextUtility = utility(i, j)
		maze_obj.update_utilities()
		# Change utilities here
