import pybullet as p
import time
import pybullet_data
import numpy as np
import gym
from stable_baselines3 import PPO

physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.8)  
p.setAdditionalSearchPath(pybullet_data.getDataPath())  

planeId = p.loadURDF("plane.urdf")  
robotId = p.loadURDF("kuka_iiwa/model.urdf", basePosition=[0, 0, 0.5])  
boxId = p.loadURDF("r2d2.urdf", basePosition=[0.5, 0, 0.5])  


time_step = 0.01
p.setTimeStep(time_step)
p.setRealTimeSimulation(1)  

class RoboticArmEnv(gym.Env):
    def __init__(self):
        super(RoboticArmEnv, self).__init__()

        self.action_space = gym.spaces.Box(low=-2.0, high=2.0, shape=(7,), dtype=np.float32)

        self.observation_space = gym.spaces.Box(low=-5.0, high=5.0, shape=(14,), dtype=np.float32)

        self.step_count = 0

    def reset(self):
       
        p.resetBasePositionAndOrientation(robotId, [0, 0, 0.5], [0, 0, 0, 1]) 
        p.resetBasePositionAndOrientation(boxId, [0.5, 0, 0.5], [0, 0, 0, 1])  
        self.step_count = 0
        return self.get_state()

    def step(self, action):
        self.step_count += 1

        for i in range(p.getNumJoints(robotId)):
            p.setJointMotorControl2(robotId, i, p.POSITION_CONTROL, targetPosition=action[i])

        p.stepSimulation()

        state = self.get_state()

        reward = -np.linalg.norm(np.array(state[:3]) - np.array(state[7:10]))  

        done = self.step_count > 500 or reward > -0.1  

        return state, reward, done, {}

    def get_state(self):
     
        joint_positions = [p.getJointState(robotId, i)[0] for i in range(p.getNumJoints(robotId))]

        box_position, _ = p.getBasePositionAndOrientation(boxId)

        state = joint_positions + list(box_position)
        return state

    def render(self):

        pass

env = RoboticArmEnv()

model = PPO('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=100000)

model.save("robotic_arm_ppo")

obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    if done:
        break

p.disconnect()
