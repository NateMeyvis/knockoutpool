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



In kogen.py two objects are defined: Game and Season. A Season is initialized with a list of Game objects and (optionally) a list of teams one has already picked and a .csv file containing lists of game data (week, favorite, underdog, line). So, e.g.:

>> s = Season(['SEA', 'CAR'])

...will create a Season object that allows one to do analyses that assume that one has picked Seattle and Carolina in the first two weeks. Various methods are available on this object, including those for filling out a set of picks in at least three ways. One is a greedy algorithm that takes the biggest remaining favorite every week:

>> s.fill_greedy_week()

Another is a greedy algorithm that takes the biggest remaining favorite over the rest of the _season_ and repeats until one has made a pick for every week:

>> s.fill_greedy_season()

A third one does an exhaustive search of all sets of picks after discarding all games in which the spread is less than a certain threshold:

>> s.fill_exhaustive() #Uses default threshold of 5 points
>> s.fill_exhaustive(-4) #You can pass in other values

One can view a Season object's picks as usual:

>> print s

So you can fill out a season using the exhaustive algorithm as follows:

>> from kogen import Season
>> s = Season(['SEA', 'CAR'])
>> s.fill_exhaustive()
>> print s