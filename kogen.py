def every_combination(ll):
	'''Given a list of game-lists [l1, l2, ..., ln],
	gives a list of every list [e1, e2, ..., e_n]
	such that e1 is in l1, e2 in l2, and so on
	(and the favorites are unique).'''
	assert type(ll) == list
	for item in ll:
		assert type(item) == list, "%s is not a list" % str(item)
	if len(ll) == 1:
		return [[i] for i in ll[0]]
	if len(ll[0]) == 1:
		temp = filter(lambda i: ll[0][0].favorite not in [j.favorite for j in i], every_combination(ll[1:]))
		return [ll[0] + i for i in temp]
	else:
		return every_combination([[ll[0][0]]] + ll[1:]) + every_combination([ll[0][1:]] + ll[1:])

def cum_prob(gg):
	'''Given a list of games <gg>,
	gives the probability they all win'''
	return reduce(lambda x, y: x * y, [g.win_prob() for g in gg])

class Game:
	conv = {0: .5, .5: .505, 1: .5125, 1.5: .525, 2: .535, 2.5: .55, 3: .595, 3.5: .6425,
	4: .6577, 4.5: .6725, 5: .681, 5.5: .69, 6: .7065, 6.5: .7235, 7: .7521, 7.5: .78,
	8: .7914, 8.5: .8021, 9: .8066, 9.5: .8111, 10: .8356, 10.5: .8602, 11: .8713, 11.5: .8824,
	12: .8845, 12.5: .8867, 13: .8932, 13.5: .9, 14: .9242, 14.5: .9487}

	def __init__(self, week, favorite, underdog, line=0, money=-110):
		self.week = int(week)
		self.favorite = favorite
		self.underdog = underdog
		self.line = float(line)
		self.money = money

	def __repr__(self):
		return "Week " + str(self.week) + ": " + self.favorite + " > " + self.underdog + " (" + str(self.line) + ")"

	def win_prob(self):
		if -1 * self.line in self.conv:
			return self.conv[-1 * self.line]
		else:
			raise ValueError, "No probability stored for point spread %s." % str(self.line)

class Season:
	def __init__(self, used=[], games="lines_nothurs.csv"):
		#Initialize from a list of Games.
		#TODO: Input santization
		self.picks = used + [None] * (17 - len(used))
		if type(games) == list:
			self.games = games
		elif type(games) == str:
			with open(games, "r") as f:
				lines = [[i.strip() for i in line.strip().split(',')] for line in f.readlines()]
				self.games = [Game(i[0], i[1], i[2], i[3]) for i in lines]

	def prune_games(self):
		'''Eliminates games you can't pick from self.games.
		Do not use if you want to keep game information
		(e.g. for game-theoretic analysis)!'''
		self.games = filter(lambda i: i.favorite not in self.picks and self.picks[i.week - 1] == None, self.games)

	def weeks(self):
		return set([game.week for game in self.games])

	def last_week(self):
		return max(self.weeks())

	def add_greedy_week(self):
		#Add the best game from the first unpicked week to self.picks
		#Find the first unpicked week
		first_empty = self.picks.index(None) + 1 #Start at Week 1, not Week 0
		#Find games available that week
		ordered = filter(lambda g: g.week == first_empty and g.favorite not in self.picks, self.lines)
		#Add the best one to self.picks
		best_pick = min(ordered, key=lambda g: g.line)
		self.picks[first_empty-1] = best_pick.favorite

	def add_greedy_season(self):
		best_remaining = min(lambda g: g.favorite not in self.picks and self.picks[g.week - 1] == None, key=lambda g: g.line)
		self.picks[g.week - 1] = best_remaining.favorite

	def fill_greedy_week(self):
		#Fills out the rest of the season greedily week-by-week
		last = self.last_week() #Only compute once
		while self.picks.index(None) + 1 < last:
			self.add_greedy_week()

	def fill_greedy_season(self):
		#Fills out the rest of the season greedily,
		#taking the best game remaining _in the whole season_
		last = self.last_week() #Only compute once
		while self.picks.index(None) + 1 < last:
			self.add_greedy_season()

	def exhaustive(self, threshold = -5):
		#Look at every combination of lines. Find the one that's best
		#First, group lines by week and filter
		filtered = filter(lambda g: g.favorite not in self.picks, self.games)
		grouped = []
		for week in self.weeks():
			grouped.append(filter(lambda g: g.week == week and g.line <= threshold, filtered))
		combinations = every_combination(grouped)
		return max(combinations, key=lambda i: cum_prob(i))