import gym
from gym_dw import envs
#import env.DeepWellEnv
from stable_baselines import TRPO
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2
import matplotlib
import matplotlib.pyplot as plt

class run_dw:
    def __init__(self):
        env = gym.make('DeepWellEnv-v0')
        ######## use TRPO or PPO2
        #model = TRPO(MlpPolicy, env, verbose=1)
        model = PPO2(MlpPolicy, env, verbose=1)
        model.learn(total_timesteps=100000)

        self.xcoord = []
        self.ycoord = []
        self.obs = env.reset()

        while True:
            action, _states = model.predict(self.obs)
            self.obs, rewards, done, info = env.step(action)
            print(self.obs)
            print("reward: ",rewards)
            self.xcoord.append(self.obs[0])
            self.ycoord.append(self.obs[1])
            if done:
                break

    def get_plot(self):
        fig = plt.figure()
        subplot = fig.add_subplot(111)
        subplot.plot(self.xcoord,self.ycoord)
        plt.gca().invert_yaxis()
        subplot.scatter(self.obs[4],self.obs[5],s=150)
        plt.xlabel("Cross Section")
        plt.ylabel("TVD")
        return fig