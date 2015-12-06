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
		self.iterations = list()
		self.gamma = 0.99
		self.policy = {}
		# number of times we've taken action from state s
		self.n_s_a = dict()
		# number of trials
		self.trial = []
		self.rmse = []
		self.maxtrial = 1000
		self.maxstep = 50
		# cutoff for exploration
		self.Ne = 20
		# q values
		self.q = {}
		self.expectedUtil = {}
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
	def cal_rmse(self):
		sum_diff = 0
		for state in self.states:
			true = self.utility[state][-1]
			expect = self.expectedUtil[state][-1]
			sum_diff += (true - expect)**2
		return math.sqrt(sum_diff / len(self.states))
	def reinforcement_learning(self):
		for trial in range(1,self.maxtrial):
			self.trial.append(trial)
			index = random.randint(0,len(self.states)-1)
			state = self.states[index]
			for t in range(1,self.maxstep+1):
				alpha = self.alpha(t)
				move = self.optimal_action(state)
				col = state[0]
				row = state[1]
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
				state_action = (state, move)
				self.n_s_a[state_action] = self.n_s_a.get(state_action, 0) + 1
				self.q[state_action] = self.q.get(state_action,0) + alpha * (self.rewards[state] \
					+ self.gamma * self.max_q(new_state) - self.q.get(state_action,0))
				state = new_state
			for statey in self.states:
				if statey not in self.expectedUtil:
					self.expectedUtil[statey] = list()
				self.expectedUtil[statey].append(self.max_q(statey))
			self.rmse.append(self.cal_rmse())


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
				self.policy[state] = '#'
				return 0
		col = state[0]
		row = state[1]
		expect_util = dict()
		for action in self.actions:
			moves = self.actions[action]
			sum_moves = 0
			for move, prob in moves.iteritems():
				if move == 'U':
					new_state = (col, row-1)
				elif move == 'L':
					new_state = (col-1,row)
				elif move == 'R':
					new_state = (col+1, row)
				else:
					# move == 'D'
					new_state = (col, row+1)
				
				if new_state not in self.states:
					new_state = (col, row)
				
				new_state_util = self.utility[new_state][-1]
				sum_moves += prob * new_state_util
			expect_util[action] = sum_moves
		best_policy = max(expect_util.iteritems(), key = operator.itemgetter(1))[0]
		self.policy[state] = best_policy
		return expect_util[best_policy]


	def value_iteration(self, terminal = True):
		self.iterations.append(0)
		for i in range(1,self.maxstep+1):
			self.iterations.append(i)
			for state in self.states:
				new_util = self.rewards[state] + (self.gamma * self.expect_utility(state, terminal))
				self.utility[state].append(new_util)

if __name__ == '__main__':
	maze = Grid()
	maze.setup_grid()
	maze.value_iteration()
	print "Utilities of all states:"
	ret_str = ''
	for i in range(6):
		for j in range(6):
			state = (j,i)
			if state in maze.utility.keys():
				ret_str += '{0:.4f}'.format(maze.utility[state][-1])
			else:
				ret_str += '0.0000'
			ret_str+='\t'
		ret_str+='\n'
	print ret_str

	print "-----------------------"
	print "Optimal policy:"
	ret_str = ''
	for i in range(6):
		for j in range(6):
			state = (j,i)
			if state in maze.utility.keys():
				ret_str += maze.policy[state]
			else:
				ret_str += 'w'
			ret_str+='\t'
		ret_str+='\n'
	print ret_str

	maze.reinforcement_learning()

	fontP = FontProperties()
	fontP.set_size('xx-small')

	plt.plot()
	for i in range(6):
		for j in range(6):
			state = (i,j)
			if state in maze.utility.keys():
				plt.plot(maze.trial, maze.expectedUtil[state], label=str(state))
	plt.xlabel('Number of trials')
	plt.ylabel('Utility estimation')
	plt.legend(prop=fontP, loc='best')
	plt.show()

	plt.plot(maze.trial, maze.rmse, label = 'RMSE')
	plt.xlabel('Number of trials')
	plt.ylabel('Root mean square error')
	plt.legend(loc='best')
	plt.show()


