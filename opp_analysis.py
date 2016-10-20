#Tools for analyzing the field in a knockout pool
#See README.md for assumptions about the .tsv file
from collections import Counter

def interpret(team):
	#Given a team abbreviation, attemps to find a
	#standard team abbreviation for it
	#Returns None if it thinks it's not a NFL team name
	TEAMS = ("ATL", "DEN", "SD", "PHI", "WAS", "JAC", "CHI", "CIN", "NE", "BAL", "NYG", "CAR",
		"NO", "DAL", "GB", "IND", "HOU", "PIT", "MIA", "CLE", "TEN", "SF", "BUF", "LA", "DET",
		"KC", "OAK", "SEA", "NYJ", "ARI", "MIN", "TB")
	d = {"k.c." : "KC", "n.e." : "NE", "g.b." : "GB"}
	if team.upper() in TEAMS:
		return team.upper()
	elif team in d:
		return d[team]
	else:
		return None

def recent_pick(path):
	#Returns a counter
	assert type(path) == str
	with open(path, 'r') as f:
		opponents = [i.strip().split() for i in f.readlines()]
	recents = [interpret(opp[-1]) for opp in opponents]
	c = Counter(recents)
	return c.most_common()#Does a sort

def usage_distribution(path):
	assert type(path) == str
	#Abbreviations for the 30 NFL teams.
	TEAMS = ("ATL", "DEN", "SD", "PHI", "WAS", "JAC", "CHI", "CIN", "NE", "BAL", "NYG", "CAR",
		"NO", "DAL", "GB", "IND", "HOU", "PIT", "MIA", "CLE", "TEN", "SF", "BUF", "LA", "DET",
		"KC", "OAK", "SEA", "NYJ", "ARI", "MIN", "TB")
	with open(path, 'r') as f:
		opponents = [i.strip().split() for i in f.readlines()]
	c = Counter(filter(lambda i: i in TEAMS, [interpret(i) for j in opponents for i in j]))
	return c.most_common()#Does a sort

if __name__ == "__main__":
	recent = recent_pick("data/prevpicks.tsv")
	s = sum([i[1] for i in recent])
	print "PICKS THIS WEEK (%d): " % s
	for r in recent:
		print str(r[0]) + "\t" + str(r[1])
	print "USAGE IN FIELD:"
	usage = usage_distribution("data/prevpicks.tsv")
	for u in usage:
		print str(u[0]) + "\t" + str(u[1])