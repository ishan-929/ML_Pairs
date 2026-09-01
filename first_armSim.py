import math 

angle = 0.0
angular_velocity = 0.0

dt = 0.01

gravity = 9.81
arm_mass = 0.5
payload_mass = 1.0
arm_length = 0.5

motor_torque = 6.0

damping = 0.2

for step in range (300):
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

    print("angle: ", math.degrees(angle))
    print("angular velocity: ", angular_velocity)