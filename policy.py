from operator import itemgetter

from space import *
from mdp import value_iteration

def main():
	mazey = maze()
	listy = [(0,1,-1), (1,3,0), (1,4,-1), (2,3,0), (2,5,3), (3,3,0), (5,0,1), (5,1,-1), (5,3,0), (5,4,-1), (5,5,-1)]

	mazey.setup(listy)
	# print mazey

	policy(mazey, True)
	print mazey.policy_printer()
	print mazey




def policy(mazey, terminal = True):
	#call value iteration here
	value_iteration(mazey, terminal)
	for i in range(mazey.size):
		for j in range(mazey.size):
			policy = max_of_neighbors(mazey, i, j)
			if terminal and mazey.grid[i][j].is_terminal():
				policy = 't'
			if mazey.grid[i][j].is_wall():
				policy = 'w'
			mazey.grid[i][j].policy = policy




def max_of_neighbors(mazey, i,j):
	find_max = list()
	if i-1 > 0:
		value = mazey.grid[i-1][j].expectedUtility
		find_max.append((value, 'U'))

	if i+1 <mazey.size:
		value = mazey.grid[i+1][j].expectedUtility
		find_max.append((value,'D'))
	if j-1 >0:
		value = mazey.grid[i][j-1].expectedUtility
		find_max.append((value, 'L'))
	if j+1 <mazey.size:
		value = mazey.grid[i][j+1].expectedUtility
		find_max.append((value,'R'))


	return max(find_max,key=itemgetter(0))[1]


if __name__ == '__main__':
	main()