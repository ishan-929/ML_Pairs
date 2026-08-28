import numpy as np
import random

num_states = 6
num_actions = 2
left = 0
right = 1
goal_state = 5

q_table = np.zeros((num_states,num_actions))

alpha=0.1 #how quick do the q values update
gamma=0.9 
epsilon = 0.2 #chance of exploration
episodes = 1000

for episode in range (episodes):
    state = 0
    while state != goal_state:
        if random.random() < epsilon:
            action = random.choice([left, right])
        else:
            action = np.argmax(q_table[state])

        old_state = state

        if action == left:
            state = max(0,state-1)
        else:
            state = min(goal_state,state+1)

        if (state == goal_state):
            reward = 10
        else:
            reward = -1

        old_q = q_table[old_state][action]
        best_future_q = np.max(q_table[state])

        new_q = old_q + alpha *(reward + gamma*best_future_q - old_q)

        q_table[old_state][action] = new_q

print(q_table)

state = 0

print("Now Testing the agent ooo:")

while state != goal_state:
    print("Current State: ", state)
    action = np.argmax(q_table[state])

    if action == left:
        print("Action: left")
        state = max(0,state-1)

    else:
        print("Action: right")
        state = min(5,state+1)

print("Current State: ", state)
print("Goal Reached!")
