from copy import deepcopy as dcp
from torch import tensor
import pickle as pkl
def save_log(obj,path):
    with open(path+'/log_file.pkl','wb') as f:
        pkl.dump(obj,f)
def open_log(path):
    with open(path+'/log_file.pkl','rb') as f:
        return pkl.load(f)
#Iterval for parameter values
par_list = {
    #Local model
    'c_ee': 16.0, #Ex-to-Ex coupling coefficient
    'c_ei': 12.0, #Ex-to-In coupling coefficient
    'c_ie': 15.0, #In-to-Ex coupling coefficient
    'c_ii': 3.0, #In-to-In coupling coefficient
    'tau_e': 8.0, #Ex membrane time-constant
    'tau_i': 8.0, #In membrane time-constant
    'a_e': 1.3, #Ex Value of max slope of sigmoid function (1/a_e) is related to variance of                           distribution of thresholds
    'b_e': 4.0, #Sigmoid function threshold
    'c_e': 1.0, #Amplitude of Ex response function
    'theta_e': 0.0, #Position of max slope of S_e
    'a_i': 2.0, #In Value of max slope of sigmoid function (1/a_e) is related to variance of                           distribution of thresholds
    'b_i': 3.7, #Sigmoid function threshold
    'c_i': 1.0, #Amplitude of In response function
    'theta_i': 0.0, #Position of max slope of S_i
    'r_e': 1.0, #Ex refractory period
    'r_i': 1.0, #In refractory period
    'k_e': 1.0, #Max value of the Ex response function
    'k_i': 1.0, #Max value of the In response function
    'P': 1.25, #Balance between Ex and In masses?
    'Q': 0.0, #Balance between Ex and In masses?
    'alpha_e': 1.0, #Balance between Ex and In masses?
    'alpha_i': 1.0, #Balance between Ex and In masses?
    'Noise 0': 0.00005,
    'Noise 1': 0.00005,
    
}
par_names = [n for n in par_list]
def theta_init(par_n = par_names):
    theta = []
    for n in par_n:
        theta.append(par_list[n])
    return tensor(theta)
theta_initial = tensor([1.6000e+01, 1.2000e+01, 1.5000e+01, 3.0000e+00, 8.0000e+00, 18.0000e+00,
        1.3000e+00, 4.0000e+00, 1.0000e+00, 0.0000e+00, 2.0000e+00, 3.7000e+00,
        1.0000e+00, 0.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00,
        1.2500e+00, 0.0000e+00, 1.0000e+00, 1.0000e+00, 5.0000e-05, 5.0000e-05])

def make_list_dir(tens):
    list_dir = []
    for i in range(tens.shape[0]):
        list_dir.append(make_dir_from_tensor(tens[i]))
    return list_dir
def make_dir_from_tensor(tens,names = par_names, index = 0):
    par_dir = dcp(par_list)
    if tens == None:
        return par_dir
    for i in range(len(names)):
        par_dir[names[i]] = tens[i].data.item()
    return par_dir
regions_labels = ['r_lateralorbitofrontal',
'r_parsorbitalis',
'r_frontalpole',
'r_medialorbitofrontal',
'r_parstriangularis',
'r_parsopercularis',
'r_rostralmiddlefrontal',
'r_superiorfrontal',
'r_caudalmiddlefrontal',
'r_precentral',
'r_paracentral',
'r_rostralanteriorcingulate',
'r_caudalanteriorcingulate',
'r_posteriorcingulate',
'r_isthmuscingulate',
'r_postcentral',
'r_supramarginal',
'r_superiorparietal',
'r_inferiorparietal',
'r_precuneus',
'r_cuneus',
'r_pericalcarine',
'r_lateraloccipital',
'r_lingual',
'r_fusiform',
'r_parahippocampal',
'r_entorhinal',
'r_temporalpole',
'r_inferiortemporal',
'r_middletemporal',
'r_bankssts',
'r_superiortemporal',
'r_transversetemporal',
'r_insula',
'l_lateralorbitofrontal',
'l_parsorbitalis',
'l_frontalpole',
'l_medialorbitofrontal',
'l_parstriangularis',
'l_parsopercularis',
'l_rostralmiddlefrontal',
'l_superiorfrontal',
'l_caudalmiddlefrontal',
'l_precentral',
'l_paracentral',
'l_rostralanteriorcingulate',
'l_caudalanteriorcingulate',
'l_posteriorcingulate',
'l_isthmuscingulate',
'l_postcentral',
'l_supramarginal',
'l_superiorparietal',
'l_inferiorparietal',
'l_precuneus',
'l_cuneus',
'l_pericalcarine',
'l_lateraloccipital',
'l_lingual',
'l_fusiform',
'l_parahippocampal',
'l_entorhinal',
'l_temporalpole',
'l_inferiortemporal',
'l_middletemporal',
'l_bankssts',
'l_superiortemporal',
'l_transversetemporal',
'l_insula'
]