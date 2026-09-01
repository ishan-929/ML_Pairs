import math 
import numpy as np

angle = 0.0
angular_velocity = 0.0

dt = 0.01

gravity = 9.81
arm_mass = 0.5
payload_mass = 1.0
arm_length = 0.5

angle_bins = [-10,-5,-3,-2,-1,-0.5,0,0.5,1,2,3,5,10,15]
velocity_bins = [-60,-10,10,60]
actions = [-8.0, -4.0, 0.0, 4.0, 8.0]

episode_rewards = []
episode_lengths = []
average_rewards = []

q_table = np.zeros((75,5))
alpha = 0.1
gamma = 0.9
epsilon = 0.2
damping = 0.2
episodes = 1000

for episode in range (episodes):

    angle = 0.0
    angular_velocity = 0.0
    total_reward = 0.0

    for step in range (300): 
        angle_degrees = math.degrees(angle)
        velocity_degrees = math.degrees(angular_velocity)

        angle_bin = np.digitize(angle_degrees, angle_bins)
        velocity_bin = np.digitize(velocity_degrees, velocity_bins)

        state = angle_bin * 5 + velocity_bin 

        if np.random.random() < epsilon:
            action = np.random.randint(0,5)
        else:
            action = np.argmax(q_table[state])

        motor_torque = actions[action]

        arm_gravity_torque = -arm_mass * gravity * (arm_length/2) * math.cos(angle)
        payload_gravity_torque = -payload_mass * gravity * arm_length * math.cos(angle)
        gravity_torque = payload_gravity_torque + arm_gravity_torque
        arm_inertia = (1/3) * arm_mass * arm_length **2
        payload_inertia = payload_mass * arm_length ** 2
        inertia = arm_inertia + payload_inertia
        damping_torque = -damping * angular_velocity
        net_torque = motor_torque + gravity_torque + damping_torque

        angular_acceleration = net_torque / inertia
        angular_velocity = angular_velocity + angular_acceleration * dt
        angle = angle + angular_velocity * dt

        new_angle_degrees = math.degrees(angle)
        new_velocity_degrees = math.degrees(angular_velocity)

        new_angle_bin = np.digitize(new_angle_degrees, angle_bins)
        new_velocity_bin = np.digitize(new_velocity_degrees, velocity_bins)
        new_state = new_angle_bin * 5 + new_velocity_bin

        reward = -abs(new_angle_degrees) - 0.05 * abs(new_velocity_degrees)
        total_reward += reward

        old_q = q_table[state][action]
        better_q = np.max(q_table[new_state])

        new_q = old_q + alpha * (reward + gamma * better_q - old_q)

        q_table[state][action] = new_q

        if abs(math.degrees(angle)) > 30:
            break

    steps_survived = step + 1
    episode_rewards.append(total_reward)
    episode_lengths.append(steps_survived)
    average_rewards.append(total_reward / steps_survived)

angle = 0.0
angular_velocity = 0.0

test_angles = []
test_velocities = []

for step in range (300):
    angle_degrees = math.degrees(angle)
    velocity_degrees = math.degrees(angular_velocity)

    angle_bin = np.digitize(angle_degrees, angle_bins)
    velocity_bin = np.digitize(velocity_degrees, velocity_bins)

    state = angle_bin * 5 + velocity_bin 
    action = np.argmax(q_table[state])

    motor_torque = actions[action]

    arm_gravity_torque = -arm_mass * gravity * (arm_length/2) * math.cos(angle)
    payload_gravity_torque = (
        -payload_mass * gravity * arm_length * math.cos(angle)
    )

    gravity_torque = payload_gravity_torque + arm_gravity_torque

    arm_inertia = (1/3) * arm_mass * arm_length ** 2
    payload_inertia = payload_mass * arm_length ** 2
    inertia = arm_inertia + payload_inertia

    damping_torque = -damping * angular_velocity
    net_torque = motor_torque + gravity_torque + damping_torque

    angular_acceleration = net_torque / inertia

    angular_velocity = angular_velocity + angular_acceleration * dt
    angle = angle + angular_velocity * dt

    test_angles.append(math.degrees(angle))
    test_velocities.append(math.degrees(angular_velocity))

    if abs(math.degrees(angle)) > 30:
        break

print("First 10 lengths:", episode_lengths[:10])
print("Last 10 lengths:", episode_lengths[-10:])

print("First 10 averages:", average_rewards[:10])
print("Last 10 averages:", average_rewards[-10:])

print("Test final angle:", math.degrees(angle))
print("Test final angular velocity:", angular_velocity)
print("Test steps survived:", step + 1)