from operator import itemgetter

from space import *
from mdp import value_iteration

def main():
	mazey = maze()

	listy = [(0,1,-1), (1,3,0), (1,4,-1), (2,3,0), (2,5,3), (3,3,0), (5,0,1), (5,1,-1), (5,3,0), (5,4,-1), (5,5,-1)]

	mazey.setup(listy)
	policy(mazey, True)

	print mazey


def policy(mazey, terminal = True):
	#call value iteration here
	# value_iteration(mazey)
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
		left = mazey.grid[i-1][j].expectedUtility
		find_max.append((left, 'L'))

	if i+1 <6:
		right = mazey.grid[i+1][j].expectedUtility
		find_max.append((right,'R'))
	if j-1 >0:
		up = mazey.grid[i][j-1].expectedUtility
		find_max.append((up, 'U'))
	if j+1 <6:
		down = mazey.grid[i][j+1].expectedUtility
		find_max.append((down,'D'))


	return max(find_max,key=itemgetter(1))[1]


if __name__ == '__main__':
	main()