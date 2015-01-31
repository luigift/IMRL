

##################################################
#*						*#
#*		     READ ME			*#
#*						*#
#*						*#
#* Luigi Franco Tedesco				*#
#* Jamal Hammoud				*#
##################################################

All our code was developed by us from scratch.

Our programming work was divided in two, following 
the two experiments prosed by the article studied:

Intrinsically Motivated Reinforcement Learning:
	   An Evolutionary Perspective

To simulate the experiences you should just type:

$ python Experience#.py

being # the number of the experience you want to
test.

The fist experience:
    The agent interacts in a 6x6 grid markovian
environment where the agent can only walk 
through single line divisions.

His goal defined by its feature is to eat the most
food possible which are situated inside boxes.

state : 
      : agent position
      : boxes condition
      : agent hungry
      : food in place

 _______________________________________________
|	|	|      |||	|	|	|	
| box1	|	|      |||	|	|	|
|_______|_______|______|||______|_______|_______|
|	|	|	|	|	|	|
|	|	|	|	|	|	|
|_______|_______|_______|_______|_______|_______|
|	|	|      |||	|	|	|	
|	|	|      |||	|agent	|	|
|=======|=======|======|||======|_______|=======|
|=======|=======|======|||======|	|=======|
|	|	|      |||	|	|	|
|	|	|      |||	|	|	|
|_______|_______|______|||______|_______|_______|
|	|	|	|	|	|	|	
|	|	|	|	|	|	|
|_______|_______|_______|_______|_______|_______|
|	|	|      |||	|	|	|
|	|	|      |||	|	| box2	|
|_______|_______|______|||______|_______|_______|

To learn from its experience, the agent uses a 
e-greedy Q-learning.

The experience is completely coded and the results
presented were verified.

The result of the experiment is a txt file with
the mean history of each reward function tested
to be plot further.

The second experience:
    The agent moves in a non-markovian environment
described as a 3x3 grid. The agent s goal is to 
eat the greater number of worms possible.
After been eaten the worm apear in any of the two
others most-right areas avaible randomly.

state : 
      : agent pos
      : agent hungre
      : worm in place
 _______________________
|	|	|	|
| Agent	|	|	|
|	|	|	|
|-------|=======|=======|
|	|	|	|
|	|	|	|
|-------|=======|=======|
|	|	|	|
|	|	|	|
|-------|=======|=======|
|	|	|	|
|	|	| worm	|
|_______|_______|_______|

The code for this experiement is not completely
finished. Thus, It was not possible to have the
final results. However the problem is already
structured.
