import pybullet as p
import time
import pybullet_data
import numpy as np

physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.8)  

p.setAdditionalSearchPath(pybullet_data.getDataPath())  

planeId = p.loadURDF("plane.urdf")  
robotId = p.loadURDF("kuka_iiwa/model.urdf", basePosition=[0, 0, 0.5])  
boxId = p.loadURDF("r2d2.urdf", basePosition=[1, 0, 0.5])  

conveyorId = p.loadURDF("cube.urdf", basePosition=[2, 0, 0.5], globalScaling=2)

time_step = 0.01  
p.setTimeStep(time_step)
p.setRealTimeSimulation(1)  


joint_positions_log = []
target_positions_log = []

def control_robot_arm(target_joint_positions):
    for i in range(p.getNumJoints(robotId)):
        p.setJointMotorControl2(robotId, i, p.POSITION_CONTROL, targetPosition=target_joint_positions[i])

def control_conveyor():
    conveyor_position = np.sin(time.time()) * 0.5  
    p.resetBasePositionAndOrientation(conveyorId, [2 + conveyor_position, 0, 0.5], [0, 0, 0, 1])

def detect_collisions():
    contact_points = p.getContactPoints()
    if contact_points:
        for contact in contact_points:
            print(f"Collision detected: {contact}")

def log_joint_positions():
    joint_positions = []
    for i in range(p.getNumJoints(robotId)):
        joint_state = p.getJointState(robotId, i)
        joint_positions.append(joint_state[0])
    joint_positions_log.append(joint_positions)

def pick_up_box():
    
    approach_position = [0.7, 0, 0.5]
    target_joint_positions = [0.5 * np.sin(time.time() * 0.1),  
                              -1.0 * np.cos(time.time() * 0.2), 
                              1.0 * np.sin(time.time() * 0.3),  
                              -1.5 * np.cos(time.time() * 0.4),  
                              1.0 * np.sin(time.time() * 0.5),  
                              -0.5 * np.cos(time.time() * 0.6),  
                              0.2 * np.sin(time.time() * 0.7)]  

    control_robot_arm(target_joint_positions)

for step in range(5000):  
 
    pick_up_box()

    control_conveyor()

    log_joint_positions()

    detect_collisions()

    p.stepSimulation()

    time.sleep(time_step)

print("Logged joint positions during simulation:")
for i, positions in enumerate(joint_positions_log[:5]):  
    print(f"Step {i}: {positions}")

p.disconnect()
