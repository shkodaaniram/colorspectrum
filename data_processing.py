import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from colormath.color_objects import XYZColor, sRGBColor, LabColor
from colormath.color_conversions import convert_color
import pandas as pd
from matplotlib import cm

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
    L = 116.0 * f_y - 16.0
    a = 500.0 * (f_x - f_y)
    b = 200.0 * (f_y - f_z)
    return L, a, b

def rgb_to_lab(r,g,b):
    x,y,z = rgb_to_xyz(r, g, b)
    return xyz_to_lab(x, y, z)

def rgb_to_lms(r,g,b):
    l = 0.3811 * r + 0.5783 * g + 0.0402 * b
    m = 0.1967 * r + 0.7244 * g + 0.0782 * b
    s = 0.0241 * r + 0.1288 * g + 0.8444 * b
    return l, m, s

def rgb2lab(r, g, b):
    '''lab = cv2.cvtColor(np.uint8([[[r * 255.0, g * 255.0, b * 255.0]]]), cv2.COLOR_RGB2LAB)
    return lab[0][0][0], lab[0][0][1], lab[0][0][2]'''
    rgb = sRGBColor(r, g, b)
    lab = convert_color(rgb, LabColor, target_illuminant='d50')
    return lab.get_value_tuple()

def lab2rgb(l, a, b):
    '''rgb = cv2.cvtColor(np.uint8([[[l, a, b]]]), cv2.COLOR_LAB2RGB)
    return rgb[0][0][0], rgb[0][0][1], rgb[0][0][2]'''
    lab = LabColor(l, a, b)
    rgb = convert_color(lab, sRGBColor)
    return rgb.get_value_tuple()

def rgb_ro_lab_using_lms(r, g, b):
    l, m, s = rgb_to_lms(r*255.0, g*255.0, b*255.0)
    log_l = 0.0
    log_m = 0.0
    log_s = 0.0
    if l > 0: log_l = np.log10(l)
    if m > 0: log_m = np.log10(m)
    if s > 0: log_s = np.log10(s)
    L = 0.5757 * log_l + 0.5757 * log_m + 0.5757 * log_s
    A = 0.4082 * log_l + 0.4082 * log_m - 0.8164 * log_s
    B = 0.7071 * log_l - 0.7071 * log_m
    print(r,g,b, L,A,B)
    return L, A, B
    '''print(r, g, b, rgb_to_lab(r*255, g*255, b*255))
    return rgb_to_lab(r*255, g*255, b*255)'''

def plot_to_xyz(interpolation):
    wave_length, x, y, z = dl.load_xyz_csv()
    #need data from 380 to 780 nm: wave_length[4:85]
    X, Y, Z = to_xyz(interpolation, x[4:85], y[4:85], z[4:85])
    R, G, B = xyz_to_rgb(X, Y, Z)
    print('RGB: ', R, G, B)
    return R,G,B

def get_rgb_points():
    a = []
    b=[]
    L=[]
    ll = 0.05#0.0625
    file = open("rgbcubepoints.txt", "w")
    '''for i in np.arange(0.0, 1.0, ll):
        for j in np.arange(0.0, 1.0, ll):
            for k in np.arange(0.0, 1.0, ll):
                tmp = rgb2lab(i, j, k)#rgb_to_lab(i,j,k)
                L.append(tmp[0])
                a.append(tmp[1])
                b.append(tmp[2])
                file.write("{0} {1} {2}\n".format(tmp[0], tmp[1], tmp[2]))
    file.close()'''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(L, a, b, c='c', s=1)
    ax.set_xlabel('L')
    ax.set_ylabel('a')
    ax.set_zlabel('b')
    '''ax.set_xlim3d(0, max(L))
    ax.set_ylim3d(min(a), max(a))
    ax.set_zlim3d(min(b), max(b))'''
    #print('max(L): {}; min(f) - {}, max(a) - {}, min(b) - {}, max(b) - {}'.format(max(L), min(a), max(a), min(b), max(b)))
    a2 = []
    b2 = []
    L2 = []
    for i in np.arange(0.0, 1.0, ll):
        for j in np.arange(0.0, 1.0, ll):
            tmp = rgb2lab(i, j, 0.0) #rgb_to_lab(i, j, 0)
            L2.append(tmp[0]), a2.append(tmp[1]), b2.append(tmp[2])
            tmp = rgb2lab(i, j, 1.0) #rgb_to_lab(i, j, 1)
            L2.append(tmp[0]), a2.append(tmp[1]), b2.append(tmp[2])
            tmp = rgb2lab(0.0, i, j) #rgb_to_lab(0, i, j)
            L2.append(tmp[0]), a2.append(tmp[1]), b2.append(tmp[2])
            tmp = rgb2lab(1.0, i, j) #rgb_to_lab(1, i, j)
            L2.append(tmp[0]), a2.append(tmp[1]), b2.append(tmp[2])
            tmp = rgb2lab(i, 0.0, j) #rgb_to_lab(i, 0, j)
            L2.append(tmp[0]), a2.append(tmp[1]), b2.append(tmp[2])
            tmp = rgb2lab(i, 1.0, j) #rgb_to_lab(i, 1, j)
            L2.append(tmp[0]), a2.append(tmp[1]), b2.append(tmp[2])
    #ax.scatter(L2, a2, b2, c='r', s=15)
    #ax.plot_trisurf(L2, a2, b2, color='red', linewidth=0.05, antialiased=True)
    df = pd.DataFrame({'x': L2, 'y': a2, 'z': b2})
    surf = ax.plot_trisurf(df.x, df.y, df.z, cmap=cm.jet, linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

'''def get_rgb_cube_surface():
    ll = 0.0625
    t1 = []
    t2 = []
    file = open("rgbsurfacepoints.txt", "w")
    for i in np.arange(0.0, 1.01, ll):
        for j in np.arange(0.0, 1.01, ll):
            tmp = rgb_to_lab(i, j, 0)
            file.write("{0} {1} {2}\n".format(tmp[0], tmp[1], tmp[2]))
            tmp = rgb_to_lab(i, j, 1)
            file.write("{0} {1} {2}\n".format(tmp[0], tmp[1], tmp[2]))
            tmp = rgb_to_lab(0, i, j)
            file.write("{0} {1} {2}\n".format(tmp[0], tmp[1], tmp[2]))
            tmp = rgb_to_lab(1, i, j)
            file.write("{0} {1} {2}\n".format(tmp[0], tmp[1], tmp[2]))
            tmp = rgb_to_lab(i, 0, j)
            file.write("{0} {1} {2}\n".format(tmp[0], tmp[1], tmp[2]))
            tmp = rgb_to_lab(i, 1, j)
            file.write("{0} {1} {2}\n".format(tmp[0], tmp[1], tmp[2]))
    file.close()'''