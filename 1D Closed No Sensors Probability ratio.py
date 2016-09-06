## ***This simulation is authored by Morgan Wood, supervised by Frederic Maire.***
#2016 Masters by Research Degree 2016

#Acknowledgement to Daniel Fulcher(supervised by F Maire) for base code which I have modified

##Acknowledgement to third party packages and their respective Authors
    #Pygame
    #numpy

## Simulation
    #This simulation will explore swarm behaviour in a 1D environment
    #The first behaviour explored will be area coverage.
    #An area will be designated in the 1d wold. The swarm will need to co-ordinate and move into that
    #area then explore it.

##Environment
    #Environment will be 1D

##Percepts of agent
    #Sensors measurements
        #IR sensor in two directions 0 degrees, 180 degrees

    #Communication
        #agents will need to communicate to pattern form

##Actions
    #Move Left x squares, Move Right x squares, Stay

#Software versions
# Python 3.4
# Pygame 1.9.2


##Communication Classes
##Actuator Classes

#imports
import random
from encodings.punycode import selective_find

import pygame
import math
import time
import numpy as np
#Iinitialise modules
pygame.init()
from enum import Enum

##Initialise variables
#Colours used in simulation
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#environment variables
pixel_height = 10
pixel_width = 10
pixel_number = 50
world_width = pixel_number*pixel_width
world_height = pixel_height *3
spawning_square = 4
#spawning_square2 = 79
# spawning_square = (10/2)

#agent variables0
no_agents = 0
agent_height = pixel_height
agent_width = pixel_width

#object variables
first_object =20
include_objects = False

#simulation variables
tick_speed = 1000

#initialise objects
simDisplay = pygame.display.set_mode((world_width + 2*agent_width,world_height + agent_height))
pygame.display.set_caption('Simulation')
clock = pygame.time.Clock()
myfont = pygame.font.SysFont(None,20)


class edirection(Enum):
    right = 1
    up = 2
    left = 3
    down = 4

class eaction(Enum):
    right = 1
    left =2
    stop = 3
    cont = 4

class emode(Enum):
    explore = 1
    stop_right =2
    stop_left = 3

#Bump Sensor
class bump_sensor():
    def __init__(self,location):
        self.location = location
        self.value = 0

    def get_percept(self):
        return self.value

class colour_sensor():
    def __init__(self):
        self.value = 0

    def get_percept(self):
        return  self.value
    

##Agent
class agent():

    def __init__(self,height,width):
        self.id = fn_counter()
        self.bump_sensors = []
        self.bump_sensors.append(bump_sensor(edirection.right))
        self.colour_sensors = []
        self.colour_sensors.append(colour_sensor())
        self.height = height
        self.width = width
        self.moved = False
        self.move_count = 0
        #x,y in  pygame is position of upper left corner
        self.x = spawning_square*agent_width
            #random.randrange(0,world_width, agent_width)
        self.belief_x = 0
        self.prev_x = 0
        self.direction = edirection.right #In degrees
        self.count_right = 0
        self.count_left = 0
        self.same_bump_count = 0
        self.prev_bump = 0
        self.prev_action = eaction.right
        self.prev_colour = 0
        self.speed = agent_width
        self.mode = emode.explore


    def update_belief_position(self):
        self.belief_x += (self.x - self.prev_x)
        self.belief_y += (self.y - self.prev_y)
        #print("belief x: " + str(self.belief_x) + ". Actual x:" + str(self.x))

    def random_position(self):
        self.x = random.randrange(0,world_width, agent_width)
        self.y = agent_height
        #self.y = random.randrange(0,world_height,agent_height) -- Used for 2d world

    def move(self,action):
        if action == eaction.right:
            self.x += agent_width
            self.move_count +=1
            self.prev_action = eaction.right
        if action == eaction.left:
            self.x -= agent_width
            self.move_count +=1
            self.prev_action = eaction.left
        if action == eaction.stop:
            self.prev_action = eaction.stop

    def fn_get_percept(self):

        return  [self.bump_sensors[0].get_percept(), self.colour_sensors[0].get_percept()]

    def program(self):
        percepts = self.fn_get_percept()
        bump_perc = percepts[0]
        colour_perc = percepts[1]

        #action_output = eaction.cont
        #add noise to bump sensor
        if random.randint(1,pixel_number) <= spawning_square:
            action_output = eaction.left
        else:
            action_output = eaction.right

        return action_output

        # if random.randint(0,100) >=95:
        #     if percepts[bump_int] ==1:
        #         percepts[bump_int] = 0
        #     else:
        #         percepts[bump_int] =1
        #
        # #add noise to colour sensor
        #
        # # if self.prev_percept == percepts:
        # #     self.same_percept_count+=1
        # # else:
        # #     self.same_percept_count = 0
        #
        # #update to store previous percept
        #
        #
        # if self.prev_action == eaction.stop:
        #     if random.randint(0,20) > 1:
        #          return eaction.stop
        #
        # if percepts[colour_int] ==1:
        #     if self.prev_colour ==1:
        #         if percepts[bump_int] == 1:
        #             self.count_right = 0
        #             self.count_left+=1
        #             if self.count_left > 4:
        #                 action_output = eaction.left
        #         else:
        #             self.count_right+=1
        #             self.count_left = 0
        #             if self.count_right > 3:
        #                 action_output = eaction.right
        #     else:
        #         #just moved into area to cover
        #         if self.prev_action == eaction.right:
        #             #keep going
        #             action_output = eaction.right
        #         else:
        #             action_output = eaction.left
        # else:
        #     if self.prev_colour == 1:
        #         # just moved out of area
        #         if self.prev_action == eaction.right:
        #             #just moved out to the right
        #             if percepts[bump_int] == 1:
        #                 #there is already an agent here
        #                 action_output = eaction.right
        #             else:
        #                 #no agent here stop
        #                 action_output = eaction.stop
        #
        #
        # self.prev_bump = percepts[bump_int]
        # self.prev_colour = percepts[colour_int]



#I think this won't stand up too different spawning positions
        #if self.same_percept_count > 2:
        # if percepts[bump_int] == 1:
        #     self.count_right = 0
        #     self.count_left+=1
        #     if self.count_left > 4:
        #         return eaction.left
        # else:
        #     self.count_right+=1
        #     self.count_left = 0
        #     if self.count_right > 3:
        #         return eaction.right


##Object
class XYobject():
    def __init__(self,x_head,y_head,length,height):
        self.x = x_head
        self.y = y_head
        self.length = length
        self.height = height

##Environment
class environment():
    #Real Environment classes will inherit from this
    def __init__(self,objects,agents):
        self.objects = objects
        self.agents = agents

    def percept(self,agent):
        #do code here, it makes sense for all agents to get their percept data from this one column
        pass

    def step(self):
        #Steps the environment forward
        pass

class XYEnvironment(environment):
    def __init__(self,width,height,initial_objects,initial_agents ):
        super(XYEnvironment, self).__init__(initial_objects,initial_agents)
        self.width = width
        self.height = height

    def step(self):
        #Shuffle turn order for agents
        random.shuffle(self.agents)
        #Get the list of actions from each agent
        actions = []
        for agent in self.agents:
            self.update_sensors(agent)
            actions.append(agent.program())

        #actions = [agent.program(self.update_sensors(agent))
             #          for agent in self.agents]

        #execute each actin
        for (agent, action) in zip(self.agents, actions):
            self.exec_agent_action(agent, action)

    def check_action_allowed(self,agent,x):
        for a in self.agents:
            if a != agent:
                if a.x == x or x < agent_width or x > world_width:
                    return  False
        return  True

    def exec_agent_action(self,agent,action):

        #world is going to need to check that agent does not collide with wall or other agents
        if action == eaction.right:
            if self.check_action_allowed(agent,agent.x + agent_width):
                agent.move(eaction.right)
        elif action == eaction.left:
            if self.check_action_allowed(agent.x,agent.x - agent_width):
                agent.move(eaction.left)
        elif action == eaction.stop:
            if self.check_action_allowed(agent.x,agent.x):
                agent.move(eaction.stop)
        elif agent.prev_action== eaction.right:
            if self.check_action_allowed(agent,agent.x + agent_width):
                agent.move(eaction.right)
        elif  agent.prev_action == eaction.left:
            if self.check_action_allowed(agent.x,agent.x - agent_width):
                agent.move(eaction.left)

    def spawning_square_check(self,spawningSquare):
        for a in self.agents:
            if a.x == spawningSquare*agent_width:
                return  False
        return  True

    def update_sensors(self,agent):
        #Return each percept to each sensor
        # set all sensor values to 0
        try:
            for b in agent.bump_sensors:
                b.value = 0
        except:
            #there are no bump sensors on this agent
            pass

        for a in self.agents:
            #Agent may not have a bumb sensor
            if a != agent:
                try:
                    for b in agent.bump_sensors:
                        if b.location == edirection.right:
                            if (a.x > agent.x and (a.x - agent.x) <= agent_width) or agent.x == (world_width - agent_width):
                                b.value = 1

                        #if direction == left, up down etc.
                except:
                    #agent does not have a bump sensor
                    pass

        #agents choice to read a sensor value, therefore not returning anything in the environment object
        try:
            for c in agent.colour_sensors:
                c.value = 0
                for obj in self.objects:
                    #if obj.x <= agent.x <= (obj.x + obj.length):
                    if agent.x >= obj.x and agent.x <= (obj.x + obj.length - agent_width):
                       # print(str("x:") + str(obj.x) +".Last x:"+ str(obj.x + obj.length)+ ". Agent:" + str(agent.x))
                        c.value = 1
        except:
            pass


##Calculates the angle between two vectors
def fn_angle_between_vectors(u,v):
    try:
        dot_product = np.vdot(u,v)
        u_norm = np.linalg.norm(u)
        v_norm = np.linalg.norm(v)
        return int(math.degrees(math.acos(dot_product/(u_norm*v_norm))))
    except:
        print("fn_angle_between_vectors: Could not calculate angle for u(" + str(u) + ") and v(" + str(v) + ").")

#Generates and sets the initial agen positions
def fn_make_init_pos_unique(agents,blnSmallStateSpace):
    if blnSmallStateSpace:
        #for small statespace randomly chose agent positions from a list of possible positions
        state_space = []
        for i in range(0,first_object*agent_width,agent_width):
            state_space.append(i)
        #shuffle positions
        random.shuffle(state_space)

        for i in range(0,no_agents):
            agents[i].x = state_space[i]

    else:
        #State space is too large
        #random initial positions and check that positions are not the same
        print("Make Positions unique")
        non_unique_initial = True
        while non_unique_initial == True:
            for i in range(0,xyEnv.agents.__len__()):
                for j in range(0,xyEnv.agents.__len__()):
                    if i != j:
                        if (abs(xyEnv.agents[i].x - xyEnv.agents[j].x) < agent_width):
                            xyEnv.agents[i].random_position()
                            non_unique_initial = False
                        #code only used in 2d problem
                        # if (xyEnv.agents[0].y - xyEnv.agents[1].y <= xyEnv.height):
                        #     xyEnv.agents[i].random_position()
                        #     break
            if not non_unique_initial:
                non_unique_initial = True


##counter used to initialise ids and anything else that must be unique
def fn_counter():
    fn_counter.count+=1
    return fn_counter.count

def fn_debug():
    return  False

def simLoop():
    simulation_exit = False
    step_count =0
    agent_colour = black
    while not simulation_exit:
        total_agent_moves = 0
        total_agents_env = 0
        step_count +=1
        simDisplay.fill(white) # fill the whole screen with white
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulation_exit = True

        xyEnv.step()

        if xyEnv.spawning_square_check(spawning_square) == True:
            a = agent(agent_height,agent_width)
            xyEnv.agents.append(a)

        # if xyEnv.spawning_square_check(spawning_square2) == True:
        #     a = agent(agent_height,agent_width)
        #     a.x = spawning_square2*agent_width
        #     xyEnv.agents.append(a)


        #Draw objects
        for i in range(0,len(xyEnv.objects)):
            pygame.draw.rect(simDisplay,green,[xyEnv.objects[i].x,xyEnv.objects[i].y,xyEnv.objects[i].length, agent_height])

        #Draw agents
        for i in range(0,len(xyEnv.agents)):
            agent_colour = black
            for j in range(0,len(xyEnv.objects)):
                if xyEnv.agents[i].x == xyEnv.objects[j].x or xyEnv.agents[i].x == xyEnv.objects[j].x + xyEnv.objects[j].length - agent_width:
                    agent_colour = red


            pygame.draw.rect(simDisplay,agent_colour,[xyEnv.agents[i].x,agent_height,agent_width, agent_height])
            #pygame.draw.rect(simDisplay,black,[xyEnv.agents[i].x,agent_height,agent_width, agent_height])
            #label =  myfont.render(str(xyEnv.agents[i].id),1,white)
           # simDisplay.blit(label, (xyEnv.agents[i].x, agent_height) )
            total_agent_moves += xyEnv.agents[i].move_count
            total_agents_env += xyEnv.agents[i].colour_sensors[0].get_percept()

        pygame.display.update()
        clock.tick(tick_speed)

        # if step_count % 100 == 0:
        #     print("Step : " + str(step_count) + ". No. Agents: " +str(len(xyEnv.agents)) + ". Possible Number: " + str((world_width/agent_width)))

        if step_count % 100 == 0:
            #print output
            print(str(step_count) +"\t"+str(len(xyEnv.agents))+"\t"+str(total_agent_moves)  )

        if len(xyEnv.agents) == (world_width/agent_width):
            print(str(step_count) +"\t"+str(len(xyEnv.agents))+"\t"+str(total_agent_moves) )
            simulation_exit = True
            print("Step Count When Finished " + str(step_count))




############# MAIN PROGRAM ##########################

#Set up Main Program
xyEnv = XYEnvironment(world_width,world_height,[],[])

#initialise variables
fn_counter.count = 0

print("Initialise Agents with IR sensor and beacon sensor")
for i in range(0,no_agents):
    a = agent(agent_height,agent_width)
    #if i == no_agents:
        #make the last agent a beacon transmitter
       # a.beacon_transmitter = beacon(world_width,90)
   # else:
       # a.beacon_sensor  = beacon_receiver(world_width,90)
    xyEnv.agents.append(a)



if include_objects == True:
    print("Create Objects")
    obj = XYobject(first_object*agent_width,agent_height,(world_width - (2*first_object)*agent_width),0)
    xyEnv.objects.append(obj)

# obj = XYobject(world_width - 5 *agent_width,0,agent_width,agent_height)
# xyEnv.objects.append(obj)


#Make sure agents have unique positions
fn_make_init_pos_unique(xyEnv.agents,True)

print("Enter main simulation loop")
simLoop()
pygame.display.update()
clock.tick(1) #tick the clock forward














