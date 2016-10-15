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
		temp = filter(lambda i: ll[0][0].favorite() not in [j.favorite() for j in i], every_combination(ll[1:]))
		return [ll[0] + i for i in temp]
	else:
		return every_combination([[ll[0][0]]] + ll[1:]) + every_combination([ll[0][1:]] + ll[1:])

def cum_prob(gg):
	'''Given a list of games <gg>, gives the probability they all win'''
	return reduce(lambda x, y: x * y, [g.prob for g in gg])

class Game:
	#Abbreviations for the 30 NFL teams.
	TEAMS = ("ATL", "DEN", "SD", "PHI", "WAS", "JAC", "CHI", "CIN", "NE", "BAL", "NYG", "CAR",
		"NO", "DAL", "GB", "IND", "HOU", "PIT", "MIA", "CLE", "TEN", "SF", "BUF", "LA", "DET",
		"KC", "OAK", "SEA", "NYJ", "ARI", "MIN", "TB")

	#Conversions between point spreads and winning probabilities.
	#In practice, a simple (game line -> probability) function works pretty well.
	CONV = {0: .5, .5: .505, 1: .5125, 1.5: .525, 2: .535, 2.5: .55, 3: .595, 3.5: .6425,
		4: .6577, 4.5: .6725, 5: .681, 5.5: .69, 6: .7065, 6.5: .7235, 7: .7521, 7.5: .78,
		8: .7914, 8.5: .8021, 9: .8066, 9.5: .8111, 10: .8356, 10.5: .8602, 11: .8713, 11.5: .8824,
		12: .8845, 12.5: .8867, 13: .8932, 13.5: .9, 14: .9242, 14.5: .9487,
        15: .95, 15.5: .945, 16: .95, 17: .95, 17.5: .95, 18.5: .95, 21:.95, 21.5: .95}

	def __init__(self, week, away, home, points):
		#Make sure the inputs make sense
		for team in (away, home):
			assert team in self.TEAMS, "Did not recognize team %s." % team
		assert -1 * float(points) in self.CONV or float(points) in self.CONV, "No probability stored for %d points." % float(points)
		assert int(week) in range(18)[1:], "There is no week %s." % str(week)
		self.week = int(week)
		self.away = away
		self.home = home
		self.points = float(points)#Spread relative to the home team
		self.prob = (1 - self.CONV[self.points]) if self.points >= 0 else self.CONV[-1 * self.points]
		#self.prob is the probability that the home team wins

	def __repr__(self):
		wk = "Week " + str(self.week) + ": "
		match = self.away + " at " + self.home
		if self.points > 0:
			spr = " (" + self.away + " -" + str(self.points) + ")"
		elif self.points < 0:
			spr = " (" + self.home + " " + str(self.points) + ")"
		else:
			spr = " (PK)."
		return wk + match + spr

	def favorite(self):
		return self.away if self.points <= 0 else self.home

class Season:
	def __init__(self, games="data/lines.tsv"):
		#Initialize from a .tsv file describing the season's games.
		if type(games) == list:#Can also accept a list of games
			self.games = games
		elif type(games) == str:
			with open(games, "r") as f:
				lines = [[i.strip() for i in line.strip().split('\t')] for line in f.readlines()]
				self.games = [Game(i[0], i[1], i[2][1:], i[4]) for i in lines if i[3] == "1"]

	def weeks(self):
		return set([game.week for game in self.games])

	def last_week(self):
		return max(self.weeks())

class PickSet:
	TEAMS = ("ATL", "DEN", "SD", "PHI", "WAS", "JAC", "CHI", "CIN", "NE", "BAL", "NYG", "CAR",
		"NO", "DAL", "GB", "IND", "HOU", "PIT", "MIA", "CLE", "TEN", "SF", "BUF", "LA", "DET",
		"KC", "OAK", "SEA", "NYJ", "ARI", "MIN", "TB")

	def __init__(self, season, used=[]):
		for i in used:
			assert i in self.TEAMS, "Didn't recognize team %s." % i
		self.season = season
		self.picks = used + [None] * (17 - len(used))

	def __repr__(self):
		return '\t'.join(filter(lambda i: i is not None, self.picks))

	def add_greedy_week(self):
		#Add the best game from the first unpicked week to self.picks
		#Find the first unpicked week
		first_empty = self.picks.index(None) + 1 #Start at Week 1, not Week 0
		#Find the games available that week; order them by win probability
		available = filter(lambda g: g.week == first_empty, self.season.games)
		available.sort(key=lambda i: -1 * i.prob)
		#Find the first available one.
		ix = 0
		while available[ix].favorite() in self.picks:
			ix += 1
		#Add it to self.picks
		self.picks[first_empty-1] = best_pick.favorite()#Remember first_empty was incremented above

	def add_greedy_season(self):
		#Slight bug in theory that's not a problem in practice:
		#Sometimes we need to pick an underdog at the very end, if things break very oddly
		#What's left?
		best_remaining = min(filter(lambda g: (g.favorite() not in self.picks) and (self.picks[g.week - 1] == None), self.season.games), key=lambda g: g.points)
		self.picks[best_remaining.week - 1] = best_remaining.favorite()

	def fill_greedy_week(self):
		#Fills out the rest of the season greedily week-by-week
		last = self.season.last_week() #Only compute once
		while self.picks.index(None) + 1 <= last:
			self.add_greedy_week()

	def fill_greedy_season(self):
		#Fills out the rest of the season greedily,
		#taking the best game remaining _in the whole season_
		last = self.season.last_week() #Only compute once
		while None in self.picks and self.picks.index(None) + 1 <= last:
			self.add_greedy_season()

	def exhaustive(self, threshold = 5, until = 17, return_many=False):
		#Look at every combination of lines. Find the one that's best
		#First, group lines by week and filter
		filtered = filter(lambda g: g.favorite() not in self.picks, self.season.games)
		grouped = []
		for week in filter(lambda week: self.picks[week-1] == None and week <= until, self.season.weeks()):
			grouped.append(filter(lambda g: g.week == week and abs(g.points) >= threshold, filtered))
		combinations = every_combination(grouped)
		if return_many:
			combinations.sort(key=lambda i: -1 * cum_prob(i))
			return combinations[:return_many]
		return max(combinations, key=lambda i: -1 * cum_prob(i))

	def fill_exhaustive(self, threshold = -5):
		exh = self.exhaustive(threshold)
		for game in exh:
			self.picks[game.week - 1] = game.favorite()