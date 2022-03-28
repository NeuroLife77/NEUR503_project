from lib.Simulator.simulator import *
from lib.utils import make_list_dir
class Wrapper:
    def __init__(self, settings = None):
        self.simulations = []
        self.speed = []
        self.a_val = []
        self.file = []
        self.length = []
    def add_sim(self,sim, speed = 20, a_val = 0.0042, file = None, length = 32e3):
        #self.simulations.append(make_list_dir(sim)) 
        self.simulations.append(sim) 
        self.speed.append(speed)
        self.a_val.append(a_val)
        self.file.append(file)
        self.length.append(length)
    def run_simulation(self,index):
        return Runner(self.simulations[index],
                     speed = self.speed[index],
                     a_val = self.a_val[index],
                     file = self.file[index],
                     length = self.length[index]
                    ).run()
    def run_simulation_long(self,index):
        return Runner(self.simulations[index],
                     speed = self.speed[index],
                     a_val = self.a_val[index],
                     file = self.file[index],
                     length = self.length[index]
                    ).run_long()

