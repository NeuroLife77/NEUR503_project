from tvb.simulator.lab import *
from tvb.datatypes import *
from numpy import array as ar
from lib.utils import *
from torch import as_tensor,transpose
from lib.Simulator.connectivity_paths import *
from scipy import signal as sgl
from random import randint
from numpy import zeros
from numpy import ones, eye

class Runner:
    
    #Initialize the parameters of the simulation (some default, some flexible) need to work on that
    def __init__(self, param, file = None, speed = 10000, a_val = 0.0042, length = 32e3, conn_rescale = 1e4):
        #2 regions connectivity
        VOI = ar([0])
        if file == 'empty':
            self.conn = connectivity.Connectivity.from_file(
                    source_file=connectivity_source_file_empty)
            self.conn.weights *= 0
            self.conn.tract_lengths *= 0
        else:    
            self.conn = connectivity.Connectivity.from_file(
                    source_file=connectivity_source_file)
            self.conn.weights *= (conn_rescale * (ones((68,68)) - eye(68)))
        self.conn.speed = ar([speed])
        #Variables of interest for the monitor
        self.VOI = VOI
        self.param = param
        par = []
        names = [n for n in param[0]]
        for n in param[0]:
            vals = []
            for i in range(len(param)):
                vals.append(param[i][n])
            par.append(ar(vals))
        #Setting up monitors
        Noise = ar([[par[22][i] for i in range(len(param))],[par[23][i] for i in range(len(param))]])
        self.monitor = monitors.RawVoi()
        #self.monitor.period = 3.90625
        self.monitor.variables_of_interest = VOI
        self.mon = [self.monitor]
        self.a_val = a_val
        #Setting up coupling
        self.coupl = coupling.Linear()
        self.coupl.a = ar([a_val])
        self.coupl.b = ar([0])
        #Setting up integrator
        self.dt = 0.5
        self.integ = integrators.HeunStochastic(dt=self.dt,
                                                noise=noise.Additive(nsig=Noise))
        self.integ.noise.ntau = 0.0
        self.integ.noise.noise_seed = randint(0,2**32)
        self.local_model = models.WilsonCowan()
        self.local_model.variables_of_interest=['E']
        self.local_model.c_ee = par[0]
        self.local_model.c_ei = par[1]
        self.local_model.c_ie = par[2]
        self.local_model.c_ii = par[3]
        self.local_model.tau_e = par[4]
        self.local_model.tau_i = par[5]
        self.local_model.a_e = par[6]
        self.local_model.b_e = par[7]
        self.local_model.c_e = par[8]
        self.local_model.theta_e = par[9]
        self.local_model.a_i = par[10]
        self.local_model.b_i = par[11]
        self.local_model.c_i = par[12]
        self.local_model.theta_i = par[13]
        self.local_model.r_e = par[14]
        self.local_model.r_i = par[15]
        self.local_model.k_e = par[16]
        self.local_model.k_i = par[17]
        self.local_model.P = par[18]
        self.local_model.Q = par[19]
        self.local_model.alpha_e = par[20]
        self.local_model.alpha_i = par[21]
        self.length = length*10
        
    #Running the simulation
    def run(self):
        
        #Make the simulator
        sim = simulator.Simulator(
            model = self.local_model,
            connectivity = self.conn,
            coupling = self.coupl,
            integrator = self.integ,
            monitors = self.mon            
        ).configure()
        
        #Collect data and running time
        y1 = sim.run(simulation_length = self.length)[0][1]
        #print(len(y1))
        
        #Collecting the data, transposing it to have timeseries for each region
        #State variable E - I
        data = ar(y1[:,0,:,0]).T
        PSD_resE = []
        for region in data:
            _ , psd = sgl.welch(region[int(2000*(1/self.dt)):],fs=(1000/self.dt), nperseg=2000/self.dt)
            PSD_resE.append(psd)
        PSD_data = as_tensor(PSD_resE)
        return  ar([PSD_data,self.param],dtype=object)
    def run_long(self):
        
        #Make the simulator
        sim = simulator.Simulator(
            model = self.local_model,
            connectivity = self.conn,
            coupling = self.coupl,
            integrator = self.integ,
            monitors = self.mon            
        ).configure()
        
        #Collect data and running time
        data = sim.run(simulation_length = self.length)[0][1]
        
        #Collecting the data, transposing it to have timeseries for each region
        #State variable E
        data = ar(data[:,0,:,0]).T
        PSD_resE = []
        for region in data:
            _ , psd = sgl.welch(region[int(2000*(1/self.dt)):],fs=(1000/self.dt), nperseg=2000/self.dt)
            PSD_resE.append(psd)
        PSD_resE = as_tensor(PSD_resE)
        return [data,PSD_resE,self.param]
        