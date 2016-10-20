from objects import Season, Game
from math import log
from Queue import PriorityQueue
from sys import argv

def gen_games(withdummy=True):
	#First, chop the season up into weeks
	#Get games within interval
	s = Season()
	#Augment season with dummy game
	dummy = Game(18, "CLE", "CLE", -14)
	d = {i : filter(lambda g: g.week == i, s.games + [dummy]) for i in range(19)[1:]}#Includes dummy game at end
	return d

d = gen_games()

def heuristic(node, until, d=d):
	filtered = [filter(lambda g: g.favorite() not in node.games, d[week]) for week in range(until + 1)[1 + len(node.games):]]
	best = [max(wk, key=lambda g: g.prob) for wk in filtered]
	return sum([g.prob for g in best])

class Node:

	#HEUR_CONST = -1 * log(MAX_P_WIN)#Supposes max p(win) is .95

	def __init__(self, games, back_cost, until=17, dummy=False):
		#If <games> is a list of strings, find relevant games
		if len(games) > 0 and type(games[0]) == str:
			self.games = [filter(lambda i: i.favorite() == j, d[games.index(j)+1])[0] for j in games]
		else:
			self.games = games
		self.dummy = dummy
		self.teams = set([g.favorite() for g in self.games])
		self.back_cost = back_cost
		self.heuristic = heuristic(self, until)
		self.score = self.back_cost + self.heuristic
		self.week = max([i.week for i in self.games]) if len(self.games) > 0 else 0

	def __repr__(self):
		return ' '.join([i.favorite() for i in self.games])

	def permissible(self):
		#Which games in <games> are permissible successors?
		return filter(lambda g: g.favorite() not in self.teams, d[self.week + 1])

def do_astar(until, used, verbose=False):
	#Create fringe
	fringe = PriorityQueue()
	#Create initial node
	n_init = Node(used, 0)
	curr = n_init
	while curr.week != until+1:#The +1 is for the dummy week
	    #Add to fringe
	    for game in curr.permissible():
	        n = Node(curr.games + [game], curr.back_cost - log(game.prob))
	        fringe.put(n)
	        if verbose:
	        	print "Push: ", n, "%.2f\t%.2f\t%.2f" % (n.back_cost, n.heuristic, n.score)
		#Pop lowest cost
	    curr = fringe.get()
	    if verbose:
		    print "Pop: ", curr, "%.2f\t%.2f\t%.2f" % (curr.back_cost, curr.heuristic, curr.score)
	return curr

node = do_astar(17, ['ATL', 'CAR', 'NE'], False)
print node