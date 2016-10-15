import sys

def get_powerrankings(power = "data/powerrankings.tsv"):
	with open(power, 'r') as f:
		d = {}
		for line in f.readlines():
		    l = line.split('\t')
		    d[l[0]] = [float(i) for i in l[1:]]
	return d

def lavg(a, b, d):#b is home team, a away
    return (d[a][0] + d[a][1] - d[b][0] - d[b][1]) / 2.0 - 3.0 

def adj(number):
    return -1 * float(int(number * 2)) / 2.0

def gen_spread(away, home, d):
    return adj(lavg(away, home, d))

def gen_lines(out="data/lines.tsv", sched="data/sched.tsv", power="data/powerrankings.tsv"):
    #open files
    f = open(sched, "r")
    h = open(out, "w")
    #Get dict of power rankings
    d = get_powerrankings(power)
    #Generate lines
    for game in f.readlines():
        week, away, home, excl = tuple(game.strip().split('\t'))
        week = int(week)
        assert away in d, "Don't recognize team %s" % away
        assert home[1:] in d, "Don't recognize team %s" % home[1:]#Strip "@"
        if excl == "1":
            points = gen_spread(away, home[1:], d)
            h.write('\t'.join([str(week), away, home, excl, str(points)]) + '\n')

if __name__ == "__main__":
	gen_lines()