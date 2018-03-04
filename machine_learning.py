import numpy as np
import data_loading as dl
from scipy.interpolate import interp1d

def load_training_data():
    data = np.loadtxt("data/training_data.txt", delimiter=" ", dtype='str')
    return data[:, 0], data[:, 1]

def get_data_by_name():
    file_names, rgb_vals = load_training_data()
    print(file_names)
    print(rgb_vals)
    for file_name in file_names:
        data = np.loadtxt("D:/Documents/University/6_course/Diplom/Data/" + file_name, delimeter=" ")
        func = interp1d(data[:, 0], data[:, 1], kind='slinear')
       # R, G, B = dp.plot_to_xyz(func)