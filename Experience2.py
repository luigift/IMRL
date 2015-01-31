# -*- coding: utf-8 -*-

######################################################
#*
#*                 IAR PROJECT 
#*  
#*  Intrinsically Motivated Reinforcement Learning :
#*      An Evolutionary Perspective
#*
#*Experiment2 :Emergent Intrinsic Reward Based on Internal
#*             Environment State 
#*
#*  Students: Luigi Franco Tedesco
#*            Jamal Hammoud
#*
######################################################

import copy
import numpy as np

#*
#* Global Variables : start
#*

DEBUG =True

# Possible actions
actions = ["north","south","east","west","eat"]
a2num = {'north':0,'south':1,'east':2,'west':3,'eat':4}

# Discount factor
gamma = 0.99

#Total number of Worms
nb_worm = 0

# Rewards
rewardSatiated = 1
rewardOther = 0


#*
#* Global Variables : end
#*

#*
#* Auxiliar Functions : start
#*

#*
#* Auxiliar Functions : end
#*

#*
#* Classes : start
#*
class Worm:
    def __init__ (self,position):
        global nb_worm 
        self.alive = True
        self.pos = position
    
    def eat_worm(self):
        print "Worm eaten"
        self.alive = False
        self.revive_worm(self.pos[0])

    def revive_worm(self,x):
        coord = [1,2,3]
        coord.remove(x)
        # Random between the two remaining possible positions
        self.pos = [coord[np.random.randint(2)], self.pos[1]]
        self.alive =True


class Agent:
    global chart, chart_lup, chart_lmid, chart_llow, worm

    def __init__(self, position,life, initialQ):
        self.pos = position
        self.hungry = True
        self.Q = initialQ
        self.where_is_agent()
        self.lifetime = life
        self.timeToHungry = 0
        self.history = np.zeros(self.lifetime)
        self.eatTime = []

    def where_is_agent(self):
        if self.pos[0] <= 1:
                self.temp_chart = chart_lup
        elif self.pos[0] <= 2:
                self.temp_chart = chart_lmid
        elif self.pos[0] <= 3:
                self.temp_chart = chart_llow
            
    def alive(self,t):
        if t >= self.lifetime:
            return False
        else:
            return True

    def hungry_ifnot(self,t):
        if not self.hungry and t - self.timeToHungry > 1:
            self.hungry = True

    def worm_in_place(self,worm):
        foodInPlace = False
        if worm.pos == self.pos and worm.alive == True:
            foodInPlace = True
        return foodInPlace

    def do(self,action,worm,time): 
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
        
        elif action == "eat":
            if self.pos == worm.pos and worm.alive == True:
                self.history[time] = 1
                self.timeToHungry = time
                worm.eat_worm()
                self.hungry = False
        else:
            print "ERROR : No existing action"
#*
#* Classes : end
#*
            
#*
#* Second Expeiment : start 
#*
 
# Map size
xDim = 3
yDim = 3

# Hunger state
nbHun = 2

# Main map definition
chart = np.zeros((5,5))

# Definition of auxiliars maps
chart_lup = np.ones((5,5))     #upper layer
chart_lmid = np.ones((5,5))     #middle layer
chart_llow = np.ones((5,5))   #lower layer

# upper layer Submap 
chart_lup[1,1:4] = np.zeros((1,3))
chart_lup[2,1] = 0
chart_lup[3,1] = 0

#middle layer Submap
chart_lmid[2,1:4] = np.zeros((1,3)) 
chart_lmid[1,1] = 0
chart_lmid[3,1] = 0

#lower layer
chart_llow[3,1:4] = np.zeros((1,3))
chart_llow[2,1] = 0
chart_llow[1,1] = 0

def display_map() : 
    # Map display
    print "UL"
    print chart_lup
    print "ML"
    print chart_lmid
    print "LL"
    print chart_llow


def print_agent_status(theAgent):
    print "AGENT STATUS"
    print "Position: ", theAgent.pos
    print "Hungry : ", theAgent.hungry
    print "Satiated : ", theAgent.satiated


        
def agent_test(agent_lifetime):
    global actions, chart, xDim,yDim

    # Learning rate
    alpha = 0
    # Exploration parameter
    eps = 1
    time = 0

    #    Defining Q
    #      Q (s1, a) 
    #
    #    States are defined as s : x (3)
    #                            : y (3)
    #                            : hunger (2)
    #                            : worm in place (2)
    #
    Q = np.zeros((4,4,2,2,len(actions)))
    T = np.zeros((4,4,2,2,len(actions),4,4,2,2))
    for xt in range(4):
        for yt in range(4):
            for ht in range(2):
                for wt in range(2):
                    T[xt,yt,ht,wt,:,xt,yt,ht,wt] = 1
    Nsa = np.zeros((4,4,2,2,len(actions)))
    Nsasn = np.zeros((4,4,2,2,len(actions),4,4,2,2))
    
    # Create agent and box
    agent = Agent([1,1],agent_lifetime,Q)
    coord = [1,2,3]
    worm = Worm([coord[np.random.randint(3)], 3])

    while agent.alive(time):
        
        current_map = copy.deepcopy(agent.temp_chart)

        # Agent gets hungry                                                                         
        agent.hungry_ifnot(time)
        
        # Saves past action
        if time > 0:
            sb = s
            ab = a
        
        x = agent.pos[0]
        y = agent.pos[1]
        h = int(agent.hungry)
        w = int(agent.worm_in_place(worm))
        
        s = (x,y,h,w)
        
        # Choose action ( eps-greedy random/Qlearning )                                             
        if np.random.random() < eps:
            # random action                                                                        
            current_action = actions[np.random.randint(len(actions))]
        else :
            # Q-learning action
            sa = (x,y,h,w,a2num[actions[0]])
            maxQ = Q[sa]
            best_action = actions[0]
            for action in actions[1:len(actions)]:
                sa = (x,y,h,w,a2num[action])
                if agent.Q[sa] > maxQ:
                    maxQ = agent.Q[sa]
                    best_action = action
            if DEBUG:
                    print "Qlearning action :", best_action
            current_action = best_action

        # state action tuple to acess array Q
        a = a2num[current_action]
        sa = (x,y,h,w,a)
        # Calculate number of times a action was taken in a given state
        if time > 0 : 
            Nsa[sa] += 1
            Nsasn[sb[0],sb[1],sb[2],sb[3],ab,s[0],s[1],s[2],s[3]] += 1
        
        print (x,y,h,w,current_action), time

        # Calculates T (transition probability)
        T[sb[0],sb[1],sb[2],sb[3],ab,s[0],s[1],s[2],s[3]] = Nsasn[sb[0],sb[1],sb[2],sb[3],ab,s[0],s[1],s[2],s[3]] / Nsa[sa]

        # TO BE DONE

        # Calculation of maxQ
        san = next_state(agent,boxes,actions[0],boxState,time)
        maxQ = agent.Q[san]
        best_action= actions[0]
        san_next = san
        if DEBUG :
            print san, actions[0]
        for action in actions[1:len(actions)]:
            san = next_state(agent,boxes,action,boxState,time)
            if DEBUG:
                print san, action
            if agent.Q[san] > maxQ:
                maxQ = agent.Q[san]
                best_action = action
                san_next = san

        # Update Q
        agent.Q[sa] = rew[s,a] + gamma* sum( T[s,a,:] * maxQ ) )


        if False:
            current_map[worm.pos[0],worm.pos[1]] = 2
            current_map[agent.pos[0], agent.pos[1]] = 3
        
            print "============", time, "=============="
            print "Next action : ", current_action
            print current_map


        # Agent Perform action
        agent.do(current_action,worm,time)

        # Time passes... tic tac tic tac
        time += 1
        
    #print agent.history
    print sum(agent.history)
agent_test(1e4)

#*
#* Second Experience : end
#*
