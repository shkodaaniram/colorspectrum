import csv
import numpy as np

def load_xyz_csv():
    wave_length = []
    x,y,z = [], [],[]
    with open('data/xyz_plot.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            wave_length.append(row[0])
            x.append(row[1])
            y.append(row[2])
            z.append(row[3])
    return wave_length, x, y, z

def load_txt(filename):
    path = "data/"+filename
    wave_length = np.genfromtxt(path, delimiter=" ")
    print wave_length[:][0]
    print '-----------------'
    #print y
