import math 

angle = 0.0
angular_velocity = 0.0

dt = 0.01

gravity = 9.81
mass = 1
arm_length = 0.5

motor_torque = 0.0

damping = 0.2

for step in range (300):
    gravity_torque = -mass * gravity * arm_length * math.cos(angle)
    inertia = mass * arm_length ** 2
    damping_torque = -damping * angular_velocity
    net_torque = motor_torque + gravity_torque + damping_torque

    angular_acceleration = net_torque / inertia
    angular_velocity = angular_velocity + angular_acceleration * dt
    angle = angle + angular_velocity * dt

    print("angle: ", math.degrees(angle))
    print("angular velocity: ", angular_velocity)