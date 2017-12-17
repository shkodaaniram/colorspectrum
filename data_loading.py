import csv
import numpy as np

def load_xyz_csv():
    wave_length = []
    x,y,z = [], [],[]
    with open('data/xyz_plot.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            wave_length.append(row[0])
            x.append(float(row[1]))
            y.append(float(row[2]))
            z.append(float(row[3]))
    return wave_length, x, y, z

def load_txt(filename):
    path = "data/"+filename
    data = np.loadtxt(path, delimiter=" ")
    for i, value in np.ndenumerate(data[:, 1]):
        if value < 0 or value > 1:
            data[i,1] = int(value)
    return data

