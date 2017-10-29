import matplotlib.pyplot as plt
import numpy as np

import data_loading as dl

def plot_data(data, axis, xlabel, ylabel, title, interpolation):
    plt.rcParams["figure.figsize"] = [10,4]
    x = np.linspace(380, 780, 41)
    plt.plot(data[:, 0], data[:, 1], x, interpolation(x))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.axis(axis if axis else [300, 800, 0, 1])
    plt.grid(True)
    plt.title(title)
    plt.show()

def to_xyz(interpolation, x, y, z):
    delta_lambda = 5
    wave_length = np.linspace(380, 780, 81)
    interpolation_res = interpolation(wave_length)
    spectrum_density = np.where(interpolation_res > 1, 1, interpolation_res)
    Y = np.sum(delta_lambda * np.multiply(spectrum_density, y))
    k = 100.0 / Y
    X = k * np.sum(delta_lambda * np.multiply(spectrum_density, x))
    Y = k * Y
    Z = k * np.sum(delta_lambda * np.multiply(spectrum_density, z))
    print 'XYZ coordinate: (', X, Y, Z, ')'
    return X, Y, Z

def xyz_to_rgb(X, Y, Z):
    R =  3.2404542*X - 1.5371385*Y - 0.4985314*Z
    G = -0.9692660*X + 1.8760108*Y + 0.0415560*Z
    B =  0.0556434*X - 0.2040259*Y + 1.0572252*Z
    return R, G, B


def plot_to_xyz(interpolation):
    wave_length, x, y, z = dl.load_xyz_csv()
    #need data from 380 to 780 nm: wave_length[4:85]
    X, Y, Z = to_xyz(interpolation, x[4:85], y[4:85], z[4:85])
    R, G, B = xyz_to_rgb(X, Y, Z)
    print 'RGB: ', R, G, B
    return R,G,B
