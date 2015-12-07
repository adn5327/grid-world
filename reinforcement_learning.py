from __future__ import division
import sys, math, operator, random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

class Grid():

	def __init__(self):
		self.states = list()
		self.rewards = dict()
		self.utility = dict()
		self.actions = dict()
		self.valid_actions()
		self.num_iterations = list()
		self.gamma = 0.99

		self.n_s_a = dict()
		self.trial = list()
		self.rmse = list()
		self.maxtrial = 1000
		self.convergence_number = 50

		self.Ne = 20

		self.q = dict()
		self.expectedUtil = dict()
		self.terminal_list = list()

	def alpha(self, t):
		return 60 / (59 +t)
	def exploration_function(self, u, n):
		if n < self.Ne:
			return sys.maxint
		return u
	def optimal_action(self, state):
		cur_dict = dict()
		for action in self.actions:
			state_action = (state, action)
			cur_dict[action] = self.exploration_function(self.q.get(state_action,0), self.n_s_a.get(state_action,0))
		return max(cur_dict.iteritems(), key=operator.itemgetter(1))[0]
	def max_q(self, state):
		if state in self.terminal_list:
			return self.rewards[state]
		maxy = list()
		for action in self.actions:
			state_action = (state, action)
			maxy.append(self.q.get(state_action,0))
		return max(maxy)
	def calculate_rmse(self):
		summer = 0
		for state in self.states:
			real_utility = self.utility[state][-1]
			expect = self.expectedUtil[state][-1]
			summer += (real_utility - expect)**2
		return math.sqrt(summer / len(self.states))
	def reinforcement_learning(self):
		for trial in range(1,self.maxtrial):
			self.trial.append(trial)
			index = random.randint(0,len(self.states)-1)
			state = self.states[index]
			for t in range(1,self.convergence_number+1):
				alpha = self.alpha(t)
				move = self.optimal_action(state)

				new_state = self.get_new_state(state, move)

				state_action = (state, move)
				self.n_s_a[state_action] = self.n_s_a.get(state_action, 0) + 1
				self.q[state_action] = self.q.get(state_action,0) + alpha * (self.rewards[state] \
					+ self.gamma * self.max_q(new_state) - self.q.get(state_action,0))
				state = new_state
			for statey in self.states:
				if statey not in self.expectedUtil:
					self.expectedUtil[statey] = list()
				self.expectedUtil[statey].append(self.max_q(statey))
			self.rmse.append(self.calculate_rmse())

	def get_new_state(self, state, move):
		col, row = state[0], state[1]
		if move == 'U':
			new_state = (col, row-1)
		elif move == 'L':
			new_state = (col-1, row)
		elif move == 'R':
			new_state = (col+1, row)
		else:
			new_state = (col, row+1)

		if new_state not in self.states:
			new_state = (col, row)

		return new_state
	def setup_grid(self):
		for i in range(6):
			for j in range(6):
				self.states.append((i,j))
		for item in [(3,1),(3,2),(3,3),(3,5)]:
			self.states.remove(item)
		for state in self.states:
			self.utility[state] = list()
			self.utility[state].append(0)
			#make all utilities 0 up front
			if state in [(1,0), (1,5), (4,1), (4,5), (5,5)]:
				self.rewards[state] = -1
				self.terminal_list.append(state)
			elif state in [(0,5)]:
				self.rewards[state] = 1
				self.terminal_list.append(state)
			elif state in [(5,2)]:
				self.rewards[state] = 3
				self.terminal_list.append(state)
			else:
				self.rewards[state] = -0.04

	def valid_actions(self):
		self.actions['U'] = {'U':0.8, 'L':0.1, 'R':0.1}
		self.actions['D'] = {'D':0.8, 'L':0.1, 'R':0.1}
		self.actions['L'] = {'L':0.8, 'U':0.1, 'D':0.1}
		self.actions['R'] = {'R':0.8, 'U':0.1, 'D':0.1}

	def expect_utility(self, state, terminal):
		if terminal:
			if state in self.terminal_list:
				return 0
		col, row = state[0], state[1]
		expect_util = dict()
		for action in self.actions:
			moves = self.actions[action]
			sum_moves = 0
			for move, prob in moves.iteritems():
				new_state = self.get_new_state(state, move)
				
				new_state_util = self.utility[new_state][-1]
				sum_moves += prob * new_state_util
			expect_util[action] = sum_moves
		best_policy = max(expect_util.iteritems(), key = operator.itemgetter(1))[0]
		return expect_util[best_policy]


	def value_iteration(self, terminal = True):
		self.num_iterations.append(0)
		for i in range(1,self.convergence_number+1):
			self.num_iterations.append(i)
			for state in self.states:
				new_util = self.rewards[state] + (self.gamma * self.expect_utility(state, terminal))
				self.utility[state].append(new_util)

	def max_of_neighbors(self, np_array, i , j):
		find_max = list()
		if i-1 > 0:
			value = np_array[i-1][j]
			find_max.append((value, 'U'))

		if i+1 <len(np_array):
			value = np_array[i+1][j]
			find_max.append((value,'D'))
		if j-1 >0:
			value = np_array[i][j-1]
			find_max.append((value, 'L'))
		if j+1 <len(np_array):
			value = np_array[i][j+1]
			find_max.append((value,'R'))


		return max(find_max,key=operator.itemgetter(0))[1]

	def print_policy(self, np_array, terminal):
		listy = [['0' for x in range(len(np_array))] for y in range(len(np_array))]
		for i in range(len(np_array)):
			for j in range(len(np_array[i])):
				policy = self.max_of_neighbors(np_array, i, j)
				if (j,i) not in self.utility.keys():
					policy = 'w'
				if (j,i) in self.terminal_list and terminal:
					policy = 't'
				listy[i][j] = policy
		ret_str = ''
		for each in listy:
			for val in each:
				ret_str+=val
				ret_str+='\t'
			ret_str+='\n'
		print ret_str




if __name__ == '__main__':
	maze = Grid()
	maze.setup_grid()
	terminal = True
	maze.value_iteration(terminal)
	print "utilities"
	arr = np.zeros((6,6), dtype=np.double)

	ret_str = ''
	for i in range(6):
		for j in range(6):
			state = (j,i)
			
			if state in maze.utility.keys():
				ret_str += '{0:.4f}'.format(maze.utility[state][-1])
				arr[i][j] = maze.utility[state][-1]
			else:
				ret_str += '0.0000'
				arr[i][j] = 0
			ret_str+='\t'
		ret_str+='\n'
	print ret_str

	print
	print
	print

	print "policy"
	maze.print_policy(arr, terminal)

	fp = FontProperties()
	fp.set_size('xx-small')
	plt.plot()
	for i in range(6):
		for j in range(6):
			state = (i,j)
			if state in maze.utility.keys():
				plt.plot(maze.num_iterations, maze.utility[state], label=str(state))
	plt.xlabel('Num iterations')
	plt.ylabel('Utility estimate')
	plt.legend(prop=fp, loc='best')
	plt.show()

	maze.reinforcement_learning()



	plt.plot()
	for i in range(6):
		for j in range(6):
			state = (i,j)
			if state in maze.utility.keys():
				plt.plot(maze.trial, maze.expectedUtil[state], label=str(state))
	plt.xlabel('Num trials')
	plt.ylabel('Utility estimate')
	plt.legend(prop=fp, loc='best')
	plt.show()

	plt.plot(maze.trial, maze.rmse, label = 'RMSE')
	plt.xlabel('Num trials')
	plt.ylabel('RMSE')
	plt.legend(loc='best')
	plt.show()


