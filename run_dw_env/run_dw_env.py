import gym
from gym_dw import envs
#import env.DeepWellEnv
from stable_baselines import TRPO
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2
import matplotlib
import matplotlib.pyplot as plt
import sys
from custom_callback.evalcallback import EvalCallback2

# Filter tensorflow version warnings
import os
# https://stackoverflow.com/questions/40426502/is-there-a-way-to-suppress-the-messages-tensorflow-prints/40426709
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import warnings
# https://stackoverflow.com/questions/15777951/how-to-suppress-pandas-future-warning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)
import tensorflow as tf
tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(0)
import logging
tf.get_logger().setLevel(logging.ERROR)


class run_dw:
    def __init__(self):
        self.env = gym.make('DeepWellEnv-v0')
        self.xcoord = []
        self.ycoord = []
        self.obs = self.env.reset()
        self.xt = 0
        self.yt = 0

        
    #Get model either by training a new one or loading an old one
    def get_model(self):
            #Periodically evalute agent, save best model
            eval_callback = EvalCallback2(self.env, best_model_save_path='./model_logs/', 
                           log_path='./model_logs/', eval_freq=1000,
                           deterministic=True, render=False) 
            if len(sys.argv)>1:
                ###### use TRPO or PPO2
                ######To train model run script with an argument (doesn't matter what)
                #model = TRPO(MlpPolicy, self.env, verbose=1, tensorboard_log='logs/')
                model = PPO2('MlpPolicy', self.env, verbose=1, tensorboard_log="logs/")
                model.learn(total_timesteps = 100000, tb_log_name='100k_')
                model.save("ppo2_100k_evalcallback")
                return model
            else:
                #Else it will load a saved one
                #remove "/app/" if not running with docker
                model = PPO2.load("ppo2_100k+240k", tensorboard_log="logs/")
                
                #####This is for retraining the model, for tensorboard integration load
                #####the tensorboard log from your trained model in the line above
                ##### and create a new name in model.learn below.
                ##### Will implement better functionality later, for now just comment/uncomment

                #model.set_env(make_vec_env('DeepWellEnv-v0', n_envs=8))
                #Continue training
                #model.learn(total_timesteps=30000, callback =eval_callback, reset_num_timesteps=False, tb_log_name='PPO2_100_2nd')
                #Save the retrained model
                #model.save("ppo2_100k+240k")
                return model

    #Test the trained model, run until done, return list of visited coords
    def test_model(self,model):
        self.obs = self.env.reset()
        while True:
            action, _states = model.predict(self.obs)
            self.obs, rewards, done, info = self.env.step(action)
            """ print(self.obs)
            print(info)"""
            print("reward: ",rewards) 
            self.xcoord.append(info['x'])
            self.ycoord.append(info['y'])
            if done:
                self.xt = info['xt']
                self.yt = info['yt']
                break
        self.env.close()
        return self.xcoord, self.ycoord
