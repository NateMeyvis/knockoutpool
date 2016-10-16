Update Oct. 13. Some of the information below is out of date.

**Data files (in the data/ subfolder)**

(1) powerrankings.tsv

A .tsv file describing teams' power rankings.
Columns: Team; one kind of power ranking; another kind of power ranking
Any power rankings will do as long as the differences between the rankings are supposed to correspond to points of spread (before a home field adjustment).

(2) sched.tsv

A .tsv file describing the NFL season.

Columns: week; away team; home team (prefixed with an "@" sign); exclusion status ("1" for included, "0" for excluded, as might be desirable if your knockout pool ignores Thursday-night games).

(3) prevpicks.tsv

A .tsv file describing the previous picks of lines in a knockout pool

Columns: name of line; week 1 pick; week 2 pick; [...]

**Python files**

(1) gen_schedule.py contains functions for generating a .tsv file with schedule data; it generates point spreads according to power rankings (by default, those kept in data/powerrankings.tsv).

To generate an updated file in data/lines.tsv from the command line, you can use:

>> python genrankings.py

You can also import various functions (e.g., for calculating the spread given teams and a power rankings file [see above]) from this file.

(2) objects.py

Defines three objects: Game, Season, and PickSet (along with a couple functions for dealing with those).

The Season object contains information about the schedule and spreads. It is initialized from a .tsv file such as sched.tsv (see above). It will, by default, load from that file:

>> s = Season() #loads from data/sched.tsv; you can put another path as an argument

The PickSet object is defined relative to a Season. It is also initialized with a list of teams picked already:

>> ps = PickSet(s, ['NE', 'GB']) #if you've picked NE and GB in weeks 1 and 2

You can view the picks of a PickSet:

>> ps #Will print the picks

The PickSet object has various methods for being filled out:

>> ps.add_greedy_week() #Adds the biggest available favorite for the next week
>> ps.add_greedy_season() #Adds the biggest available favorite for the season

A more useful method does an exhaustive search of all sets of picks after discarding all games in which the spread is less than a certain threshold:

>> ps.fill_exhaustive() #Uses default threshold of 5 points
>> ps.fill_exhaustive(-4) #You can pass in other values

So you can fill out a season using the exhaustive algorithm as follows:

>> from objects import Season, PickSet
>> s = Season()
>> ps = PickSet(s, ['SEA', 'CAR'])
>> ps.fill_exhaustive()
>> print ps

PickSet objects also give a method for comparing the probabilities of the best pick sets for each of various choices for the next week. This works as follows: First, the 500 (there's a parameter here, named "depth") pick sets most likely to have every game correct are found; next, for each team that is chosen next week at least once in that set, the highest probability from that set of 500 is found; finally, each team and probability are printed. E.g.:

>> ps.compare_options(until=11) #would calculate through week 11; default is full season

 #This might print:
BUF	0.53
PIT	0.48
PHI	0.46
TEN	0.44
ARI	0.43
DET	0.42
HOU	0.41