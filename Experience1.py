######################################################
#*
#*                   IAR PROJECT 
#*  
#*  Intrinsically Motivated Reinforcement Learning :
#*           An Evolutionary Perspective
#*
#*
#*  Students:    Luigi Franco Tedesco
#*               Jammal Hammoud
#*
######################################################

import copy
import numpy as np
from Tkinter import *   

#*
#* Global Variables : start
#*

# DEBUG variable
DEBUG = False#True
MSG = False

# Total number of boxes
nb_box = 0

# Box possible states
state_prob = ['open','half-open','closed']

# Possible actions
actions = ["north","south","east","west","open","eat"]
a2num = {'north':0,'south':1,'east':2,'west':3,'open':4,'eat':5}

# Discount factor
gamma = 0.99

copied = False

#*
#* Global Variables : end
#*

#*
#* Auxiliar Functions : start
#*
def rangeF(start, step, stop):
    while start<stop:
        yield start
        start+=step

def vectorAverage(vectors,lifetime):
    rvector = np.zeros(lifetime)
    for vector in vectors:
        rvector = rvector + vector
    
    return rvector
    
#*
#* Auxiliar Functions : end
#*

#*
#* Classes : start
#*

# Each instanced object is a box that can be open and has
# food inside it which can be eaten
class Box:
    def __init__ (self,position):
        global nb_box
        self.s = 'closed'
        self.food = True
        self.pos = position
        self.openingTime = 0
        nb_box += 1
    
    def __del__(self):
        class_name = self.__class__.__name__

    def open_box(self,t):
        self.s = 'half-open' 
        self.openingTime = t
        if not copied and MSG:
            print "Box was half-opened at time", t

    def open_ifhalfopen(self,t):
        if self.s == 'half-open' and t - self.openingTime > 1 :
            if not copied and MSG:
                print "Box was opened at time", t
            self.s = 'open'
            self.food = False

    def close_ifopen(self):        
        if self.s == 'open' and np.random.random() < 0.1:
            self.s = 'closed'
            self.food = True
            if not copied and MSG:
                print "Box closed!"
    
    def foodEaten(self):
        self.food = False
        if not copied and MSG:
            print "Food eaten!"
            
    def food_1e4(self,t,condition):
        if condition == 'step' and t < 1e4 :
            self.food = False
            

# Agent class
# Do : method which allow it to make actions
# where_is_agent : situates in which sub-map the agent is
# alive : tells if the agent is alive
# food_in_place : returns true if there is food in place
class Agent:
    global chart, chart_nw, chart_sw, chart_se, chart_ne, copied

    def __init__(self, position,life, initialQ):
        self.pos = position
        self.hungry = True
        self.timeToHungry = 0
        self.Q = initialQ
        self.where_is_agent()
        self.lifetime = life
        self.history = np.zeros(self.lifetime)
        self.score = 0
        self.eatTime = []

    def where_is_agent(self):
        if self.pos[0] < 4 :
            if self.pos[1] < 4:
                self.temp_chart = chart_nw
            else:
                self.temp_chart = chart_ne
        else:
            if self.pos[1] < 4:
                self.temp_chart = chart_sw
            else:
                self.temp_chart = chart_se
            
    def alive(self,t):
        if t >= self.lifetime:
            return False
        else:
            return True
            
    def hungry_ifnot(self,t):
        if not self.hungry and t - self.timeToHungry > 1:
            self.hungry = True

    def food_in_place(self,boxes):
        foodInPlace = False
        for box in boxes:
            if box.pos == self.pos and box.food == True:
                foodInPlace = True
        return foodInPlace

    def __del__(self):
        class_name = self.__class__.__name__

    def do(self,action,boxes,t): 
        if action == "north":
            if self.temp_chart[self.pos[0] - 1, self.pos[1]] != 1 :
                self.pos[0] -= 1
                self.where_is_agent()

        elif action == "south":
            if self.temp_chart[self.pos[0] + 1, self.pos[1]] != 1:
                self.pos[0] += 1
                self.where_is_agent()
            
        elif action == "east":
            if self.temp_chart[self.pos[0], self.pos[1] + 1] != 1:
                self.pos[1] += 1
                self.where_is_agent()

        elif action == "west": 
            if self.temp_chart[self.pos[0], self.pos[1] - 1] != 1:
                self.pos[1] -= 1
                self.where_is_agent()

        elif action == "open": 
            for box in boxes:
                if box.s == 'closed' and box.pos == self.pos:
                    box.open_box(t)
        
        elif action == "eat":
            for box in boxes:
                if box.s == 'half-open' and box.food and box.pos == self.pos:
                    box.foodEaten()
                    self.hungry = False
                    self.timeToHungry = t
                    self.score += 1
                    self.history[t] = 1
                    self.eatTime.append(t)
        else:
            print "ERROR : No existing action"
#*
#* Classes : end
#*

#*
#* First Experience : start 
#*
 
# Map size
xDim = 6
yDim = 6

# Hunger state
nbHun = 2

# Main map definition
chart = np.zeros((8,8))

# Definition of auxiliars maps
chart_sw = np.ones((8,8))
chart_se = np.ones((8,8))
chart_nw = np.ones((8,8))
chart_ne = np.ones((8,8))

# North West Submap 
chart_nw[1:4,1:4] = np.zeros((3,3))
chart_nw[1,4] = 0


chart_ne[1:4,4:7] = np.zeros((3,3)) 
chart_ne[1,3] = 0
chart_ne[4,6] = 0

chart_sw[4:7,1:4] = np.zeros((3,3))
chart_sw[5,4] = 0

chart_se[4:7,4:7] = np.zeros((3,3))
chart_se[5,3] = 0 
chart_se[3,6] = 0


def display_map() : 
    # Map display
    print "NW"
    print chart_nw
    print "NE"
    print chart_ne
    print "SW"
    print chart_sw
    print "SE"
    print chart_se



def print_agent_status(theAgent):
    print "\nAGENT STATUS"
    print "Position: ", theAgent.pos
    print "Hungry : ", theAgent.hungry

# Create boxes
def creat_box():
    # Random between the four possible positions 
    coord = [1,6]
    box01 = Box([coord[np.random.randint(2)], coord[np.random.randint(2)]])
    temp_pos = [coord[np.random.randint(2)], coord[np.random.randint(2)]]
    while temp_pos == box01.pos :
        temp_pos = [coord[np.random.randint(2)], coord[np.random.randint(2)]]
        
    box02 = Box(temp_pos)
    return [box01,box02]

def next_state(agent,boxes,action,boxState,t):
    global copied
    copied = True # DEBUG: Do not display prevision state actions results


    # Coping environment
    agentCopy = copy.deepcopy(agent)
    boxesCopy = []
    for box in boxes:
        boxesCopy.append( copy.deepcopy(box) )
        

    if DEBUG:
        print "BoxC01(t",t,") : ",boxesCopy[0].s , boxesCopy[0].food
        print "BoxC02(t",t,") : ",boxesCopy[1].s , boxesCopy[1].food

    # Agent Perform action 
    agentCopy.do(action,boxesCopy,t)

    # Time step,passes
    t+=1
    
    # Evironment actions
    #   Agent gets hungry
    agentCopy.hungry_ifnot(t)
    
    # Box closing (p=0.1) and opening events 
    for box in boxesCopy:
        box.close_ifopen()
    
        box.open_ifhalfopen(t)
    if DEBUG:
        print "BoxC01(t",t,") : ",boxesCopy[0].s , boxesCopy[0].food
        print "BoxC02(t",t,") : ",boxesCopy[1].s , boxesCopy[1].food

    x = agentCopy.pos[0]
    y = agentCopy.pos[1]
    h = int(agentCopy.hungry)
    b = boxState[boxesCopy[0].s,boxesCopy[1].s]
    f = int(agentCopy.food_in_place(boxesCopy))
    
    saNext = (x,y,h,b,f,a2num[action])
    
    # Deleting copies
    del agentCopy
    i = 0
    for box in boxesCopy:
        del box
        i+=1
    del boxesCopy

    copied =False
    return saNext


def box_status_to_state():
    boxState = {}
    boxState['open','open'] = 0

    boxState['open','closed'] = 1
    boxState['closed','open'] = 1

    boxState['open','half-open'] = 2
    boxState['half-open','open'] = 2

    boxState['closed','half-open'] = 3
    boxState['half-open','closed'] = 3

    boxState['closed','closed'] = 4

    # Error detection
    boxState['half-open','half-open'] = 15 # DEBUG: bigger than array dimension

    return boxState

        
def agent_test(agent_lifetime,agent_pos,boxes,rew,condition):
    global actions, gamma

    #    Defining Q (s, a) 
    #
    #    States are defined as s : x (3)
    #                            : y (3)
    #                            : hunger (2)
    #                            : boxes opening status (7)
    #                            : food in place (2)

    Q = np.random.uniform(-0.001,0.001, (8,8,2,5,2, len(actions)))

    # Create agent and box
    agent = Agent(agent_pos,agent_lifetime,Q)
    boxState = box_status_to_state()

    # Simulation Parameters
    eps = 0.3 # 1 - random / 0 - Qlearning
    alpha = 0.9
    time = 0

    while agent.alive(time):
    
        # Agent gets hungry
        agent.hungry_ifnot(time)

        # Box closing (p=0.1) and opening events 
        for box in boxes:
            box.close_ifopen()
            box.open_ifhalfopen(time)
            box.food_1e4(time,condition)

        # State s = (x,y,h,b,f)
        x = agent.pos[0]
        y = agent.pos[1]
        h = int(agent.hungry)
        b = boxState[boxes[0].s,boxes[1].s]
        f = int(agent.food_in_place(boxes))

        s = (x,y,h,b,f)
        
        # Choose action ( eps-greedy random/Qlearning )
        if np.random.random() < eps: 
            # random action
            if DEBUG:
                print "random aciton"
            current_action = actions[np.random.randint(len(actions))]
        else : 
            # Q-learning action
            sa = (x,y,h,b,f,a2num[actions[0]])
            maxQ = Q[sa]
            best_action = actions[0]
            for action in actions[1:len(actions)]:
                sa = (x,y,h,b,f,a2num[action])
                if agent.Q[sa] > maxQ:
                    maxQ = agent.Q[sa]
                    best_action = action
            if DEBUG:
                    print "Qlearning action :", best_action
            current_action = best_action

        #MAXaction Q
        san = next_state(agent,boxes,current_action,boxState,time)
        maxQ = agent.Q[san]
        for action in actions[1:len(actions)]:
            if agent.Q[san[0],san[1],san[2],san[3],san[4],a2num[action]] > maxQ:
                maxQ = agent.Q[san[0],san[1],san[2],san[3],san[4],a2num[action]]

        a =a2num[current_action]

        sa = (x,y,h,b,f,a)

        temp = Q[sa]
        
        # Update Q        
        agent.Q[sa] = (1-alpha)*agent.Q[sa] + alpha*(rew[b,h] + gamma*maxQ)

        #print sa,current_action,temp, agent.Q[sa], maxQ , time

        if DEBUG :
            ####### DISPLAY EXPERIENCE ########
            print "\n=========== TIME : ",time ,"=============="
            print_agent_status(agent)
            print "Next Action : " , current_action

            print "\nBOX STATUS"
            print "             Box01    Box02"
            print "Overture  : " , boxes[0].s, " ", boxes[1].s
            print "Food      : " , boxes[0].food, "   ", boxes[1].food,"\n"
            current_map = copy.deepcopy(agent.temp_chart)
            current_map[boxes[0].pos[0],boxes[0].pos[1]] = 2
            current_map[boxes[1].pos[0],boxes[1].pos[1]] = 2
            current_map[agent.pos[0],agent.pos[1]] = 3
            
            
            print s
            
            print current_map

            current_map[agent.pos[0],agent.pos[1]] = 0

        # Agent Perform action 
        agent.do(current_action,boxes,time)
        
        # Time passes... tic tac tic tac
        time += 1

    #print "Agent Fitness : ", agent.score
    if False or (not DEBUG and MSG):
        print boxes[0].pos
        print boxes[1].pos

    #print agent.eatTime
    return agent.history


def test_reward_function():

    # Best CONSTANT condition reward

    # Best Reward
    c_b_rew = np.zeros((5,2))
    c_b_rew[0,0] = 0.7
    c_b_rew[1,0] = 0.3
    c_b_rew[0,1] = -0.01
    c_b_rew[1,1] = -0.05
    c_b_rew[2,1] = 0.2
    c_b_rew[3,1] = 0.1
    c_b_rew[4,1] = -0.02

    # Best fitness-based Reward
    c_bfb_rew = np.zeros((5,2))
    c_bfb_rew[0,0] = 0.7
    c_bfb_rew[1,0] = 0.7
    c_bfb_rew[0,1] = -0.005
    c_bfb_rew[1,1] = -0.005
    c_bfb_rew[2,1] = -0.005
    c_bfb_rew[3,1] = -0.005
    c_bfb_rew[4,1] = -0.005

    # Best STEP condition reward

    # Best Reward
    s_b_rew = np.zeros((5,2))
    s_b_rew[0,0] = 0.5
    s_b_rew[1,0] = 0.3
    s_b_rew[0,1] = -0.05
    s_b_rew[1,1] = -0.05
    s_b_rew[2,1] = -0.01
    s_b_rew[3,1] = -0.01
    s_b_rew[4,1] = -0.05
    
    # Best fitness-based Reward 
    s_bfb_rew = np.zeros((5,2))
    s_bfb_rew[0,0] = 0.5
    s_bfb_rew[1,0] = 0.5
    s_bfb_rew[0,1] = -0.01
    s_bfb_rew[1,1] = -0.01
    s_bfb_rew[2,1] = -0.01
    s_bfb_rew[3,1] = -0.01
    s_bfb_rew[4,1] = -0.01
    
    rews = [[c_b_rew,'best reward','constant'], [c_bfb_rew, 'best fitness-based reward','constant'], [s_b_rew,'best reward', 'step'], [s_bfb_rew,'best fitness-based reward','step']]
    
    print "Starting Experience"
    for rew, name, condition in rews:
        print "============================="
        print "Condition : ", condition
        print "Reward    : ", name
        print "============================="
        # Clean Result Vectors
        vectorFitness = []
        vectorHistory = []
        
        # Define each experiment condition : Constant or Step
        if condition == 'constant':
            agent_lifetime = 1e4
            alwaysFood = True
        elif condition == 'step':
            agent_lifetime = 2e4
            alwaysFood = False
        else :
            print " ERROR: Missing operation condition "

        # set (alpha, eps)
        for alpha in rangeF(0, 0.05,1):
            for eps in rangeF(0, 0.1,1): # 200 (alpha,eps) pairs

                # Display chosen alpha and epsilon
                print "Setted (Alpha, Epsilon) = (",alpha,", ", eps,")"
                
                # Sample a random environment Ei        
                boxes = creat_box()
                agent_pos = [np.random.randint(6)+1,np.random.randint(6)+1]
            
                # Creates agent history
                history = agent_test(agent_lifetime,agent_pos,boxes,rew,condition)
            
                # Computes fitness
                vectorFitness.append(sum(history))
                vectorHistory.append(history)

                #print "History", history
                #print "Fitness : ", sum(history)
            
        #print "Mean Fitness : ", np.mean(vectorFitness)
        average = vectorAverage(vectorHistory,agent_lifetime)
        for i in average:
            print i,
        print " "

test_reward_function()

# funciton to display environment    
def display_environment(): # Has to be finished
    window = Tk()
    window.title('test')


    # def des couleurs                                                                                    
    myred="#D20B18"
    mygreen="#25A531"
    myblue="#0B79F7"
    mygrey="#E8E8EB"
    myyellow="#F9FB70"
    myblack="#2D2B2B"
    mywalls="#5E5E64"
    mywhite="#FFFFFF"
    color=[mywhite,mygreen,myblue,myred,myblack]

    #taille de la grille                                                                                  
    nblin=6
    nbcol=6

    g= np.zeros((nblin+2,nbcol+2), dtype=np.int)

    zoom=1

    wWidth = 50*nbcol+100
    wHeight = 50*nblin+100

    Canevas = Canvas(window, width = wWidth, height =wHeight, bg =mywhite)
    Canevas.focus_set()
    Canevas.pack(padx = 10, pady =10)

    for i in range(nblin+1):
        ni=50*i+50                                                                             
        Canevas.create_line(20, ni, wWidth-20,ni)                                                  
     
    for j in range(nbcol+1):                                                                    
        nj=50*j+50                                                                              
        Canevas.create_line(nj, 20, nj, wHeight-20)                                                 
      

    # Close window
    Button(window, text ='Quit', command = window.destroy).pack(side=LEFT,padx=5,pady=5)

    aPos = [1,1]
    
    agentCanvas = Canevas.create_oval(50*aPos[0]+50,50*aPos[1]+50,50*aPos[0]+100,50*aPos[1]+100,width=2,outline='black',fill=myblack)

    aPos = [3,3]

#    Canvas.coords(agentCanvas,50*aPos[0]+50,50*aPos[1]+50,50*aPos[0]+100,50*aPos[1]+100)

    window.mainloop()


#display_environment()

#*
#* First Experience : end
#*
