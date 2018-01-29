import numpy as np
from colormath.color_objects import LabColor
from colormath import color_diff
import data_processing as dp

def distance(spectrum_pnt, pnt, mode):
    color1 = LabColor(lab_l=spectrum_pnt[0], lab_a=spectrum_pnt[1], lab_b=spectrum_pnt[2])
    color2 = LabColor(lab_l=pnt[0], lab_a=pnt[1], lab_b=pnt[2])
    if mode == 'cie1976':
        return color_diff.delta_e_cie1976(color1, color2)
    elif mode == 'cie1994':
        return color_diff.delta_e_cie1994(color1, color2, K_L=1, K_C=1, K_H=1, K_1=0.045, K_2=0.015)
    elif mode == 'cie2000':
        return color_diff.delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1)
    elif mode == 'cmc':
        return color_diff.delta_e_cmc(color1, color2, pl=2, pc=1)
    else:
        return np.sqrt((spectrum_pnt[0] - pnt[0]) ** 2 + (spectrum_pnt[1] - pnt[1]) ** 2 + (spectrum_pnt[2] - pnt[2]) ** 2)

def derivation(spectrum_pnt, pnt, mode,  h = 0.00001):
    l = (distance(spectrum_pnt, (pnt[0]+h, pnt[1], pnt[2]), mode) - distance(spectrum_pnt, pnt, mode)) / h
    a = (distance(spectrum_pnt, (pnt[0], pnt[1]+h, pnt[2]), mode) - distance(spectrum_pnt, pnt, mode)) / h
    b = (distance(spectrum_pnt, (pnt[0], pnt[1], pnt[2]+h), mode) - distance(spectrum_pnt, pnt, mode)) / h
    return l, a, b

def count_next_point(spectrum_pnt, pnt, step, mode):
    return pnt - np.multiply(step, np.asarray(derivation(spectrum_pnt, pnt, mode)))

def get_step(spectrum_pnt, pnt, mode):
    #golden section method
    eps = 0.00001
    a = 0.0
    b = 10.0
    phi = 1.618034
    x1 = b - (b - a) / phi
    x2 = a + (b - a) / phi
    while (b - a) / 2 >= eps:
        x1_next = count_next_point(spectrum_pnt, pnt, x1, mode)
        x2_next = count_next_point(spectrum_pnt, pnt, x2, mode)
        if distance(spectrum_pnt, x1_next, mode) > distance(spectrum_pnt, x2_next, mode):
            a = x1
            x1 = x2
            x2 = b - (x1 - a)
        else:
            b = x2
            x2 = x1
            x1 = a + (b - x2)
    return (a + b) / 2.0

def fit_into_restrictions(pnt, space_type):
    if space_type == 'rgb':
       if pnt[0] < 0.0 : pnt[0] = 0.0
       if pnt[0] > 1.0: pnt[0] = 1.0
       if pnt[1] < 0.0 : pnt[1] = 0.0
       if pnt[1] > 1.0: pnt[1] = 1.0
       if pnt[2] < 0.0 : pnt[2] = 0.0
       if pnt[2] > 1.0: pnt[2] = 1.0
    elif space_type == 'lab':
        if pnt[0] < 0.0: pnt[0] = 0.0
        if pnt[0] > 100.0: pnt[0] = 100.0
        if pnt[1] < -127.0: pnt[1] = -127.0
        if pnt[1] > 127.0: pnt[1] = 127.0
        if pnt[2] < -127.0: pnt[2] = -127.0
        if pnt[2] > 127.0: pnt[2] = 127.0
    pnt = (pnt[0], pnt[1], pnt[2])
    return pnt

#gets rgb point in range from 0 to 1, but returns rgb in range from 0 to 255
def steepest_descend(spectrum_pnt, mode):
    print('Color for optimization in rgb: ', spectrum_pnt)
    spectrum_pnt = dp.rgb2lab(spectrum_pnt[0], spectrum_pnt[1], spectrum_pnt[2])
    print('Color for optimization in lab: ', spectrum_pnt)
    step = 0.1  #need optimization
    start_pnt = (0.0, 0.0, 0.0)
    pnt = start_pnt - np.multiply(step, np.asarray(derivation(spectrum_pnt, start_pnt, mode)))
    print('First counted pnt: ', pnt)
    eps = 0.00001
    cnt = 0
    print('first distance: ', np.abs(distance(spectrum_pnt, pnt, mode) - distance(spectrum_pnt, start_pnt, mode)))
    while np.abs(distance(spectrum_pnt, pnt, mode) - distance(spectrum_pnt, start_pnt, mode)) > eps:
        start_pnt = pnt
        step = get_step(spectrum_pnt, pnt, mode)
        pnt = start_pnt - np.multiply(step, np.asarray(derivation(spectrum_pnt, start_pnt, mode)))
        pnt = fit_into_restrictions(pnt, 'lab')
        print('Points in the loop: ', start_pnt, pnt)
        print('loop counter: ', cnt, '    STEP: ', step)
        print('distance', np.abs(distance(spectrum_pnt, pnt, mode) - distance(spectrum_pnt, start_pnt, mode)))
        cnt += 1
    print('Result: ', dp.lab2rgb(pnt[0], pnt[1], pnt[2]))
    return dp.lab2rgb(pnt[0], pnt[1], pnt[2])