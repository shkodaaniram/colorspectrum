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
    #I - reference illuminant; we are using D50
    I = np.loadtxt('data/D50_reference_illuminant.txt', delimiter=" ")[:,1] #I: wave_length - I[:,0],  illuminant - I[:,1]
    N = np.sum(delta_lambda * np.multiply(y, I))
    X = 1.0 / N * np.sum(delta_lambda * np.multiply(np.multiply(x, spectrum_density), I))
    Y = 1.0 / N * np.sum(delta_lambda * np.multiply(np.multiply(y, spectrum_density), I))
    Z = 1.0 / N * np.sum(delta_lambda * np.multiply(np.multiply(z, spectrum_density), I))
    '''Y = np.sum(delta_lambda * np.multiply(spectrum_density, y))
    k = 100.0 / Y
    X = k * np.sum(delta_lambda * np.multiply(spectrum_density, x))
    Y = k * Y
    Z = k * np.sum(delta_lambda * np.multiply(spectrum_density, z))'''
    print('XYZ coordinate: (', X, Y, Z, ')')
    return X, Y, Z

def xyz_to_rgb(X, Y, Z):# RGB values in range of (0;1)
    #http://brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    R = (3.1338561*X - 1.6168667*Y - 0.6168667*Z)
    G = (-0.6168667*X + 1.9161415*Y + 0.0334540*Z)
    B = (0.0719453*X - 0.2289914*Y + 1.2289914*Z)
    return R, G, B

def rgb_to_xyz(r, g, b):# RGB values in range of (0;1)
    #http://brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    X = 0.4360747*r + 0.3850649*g + 0.1430804*b
    Y = 0.2225045*r + 0.7168786*g + 0.0606169*b
    Z = 0.0139322*r + 0.0971045*g + 0.7141733*b
    return X,Y,Z

def xyz_to_lab(x, y, z):
    #X_n, Y_n, Z_n - values for illuminant D50 - https://en.wikipedia.org/wiki/Lab_color_space
    X_n = 96.6797
    Y_n = 100.0
    Z_n = 82.5188
    x_r = x / X_n
    y_r = y / Y_n
    z_r = z / Z_n
    f_x = 0.0
    f_y = 0.0
    f_z = 0.0
    e = 216.0 / 24389.0
    k = 24389.0 / 27.0
    if x_r > e:
        f_x = np.power(x_r, 1/3)
    else:
        f_x = (k * x_r + 16.0) / 116.0
    if y_r > e:
        f_y = np.power(y_r, 1/3)
    else:
        f_y = (k * y_r + 16.0) / 116.0
    if z_r > e:
        f_z = np.power(z_r, 1/3)
    else:
        f_z = (k * z_r + 16.0) / 116.0
    L = 116.0 * f_y - 16
    a = 500.0 * (f_x - f_y)
    b = 200.0 * (f_y - f_z)
    return L,a,b

def rgb_to_lab(r,g,b):
    x,y,z = rgb_to_xyz(r, g, b)
    return xyz_to_lab(x, y, z)

def plot_to_xyz(interpolation):
    wave_length, x, y, z = dl.load_xyz_csv()
    #need data from 380 to 780 nm: wave_length[4:85]
    X, Y, Z = to_xyz(interpolation, x[4:85], y[4:85], z[4:85])
    R, G, B = xyz_to_rgb(X, Y, Z)
    print('RGB: ', R, G, B)
    return R,G,B
