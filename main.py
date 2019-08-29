

import smopy
import matplotlib.pyplot as plt
import csv
import numpy as np
import glob

def reduce_function(x):
    if x:
        return np.mean(x)
    else:
        return 10

if __name__ == "__main__":
    t = []
    lona = []
    lata = []
    z = []
    #lat_lon_range = [38.149897, -78.450772, 38.170802, -78.424730]
    lat_lon_range = [-100, -100, 100, 100]
    #filelist = ['20190826-214237.csv', '20190827-141146', '20190827-184304', '20190827-201221', '20190828-160033.csv', '20190828-190213.csv']
    filelist = glob.glob('*.csv')
    for filen in filelist:
        with open(filen,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                if (row[1]) and (row[2]):
                    print(row)
                    latr = float(row[1])
                    latd = latr // 100
                    latm = latr - 100 * latd
                    lat = latd + latm / 60

                    lonr = float(row[2])
                    lond = lonr // 100
                    lonm = lonr - 100 * lond
                    lon = -1.0*(lond + lonm / 60)
                    if (lat_lon_range[0]<= lat <=lat_lon_range[2]) and (lat_lon_range[1]<= lon <=lat_lon_range[3]):
                        t.append(row[0])
                        lata.append(lat)
                        lona.append(lon)
                        z.append(float(row[3]))

    lat_lon_rangemap = [min(lata), min(lona), max(lata), max(lona)]
    map = smopy.Map(lat_lon_rangemap, z=16)

    x, y = map.to_pixels(np.asarray(lata), np.asarray(lona))
    ax = map.show_mpl(figsize=(8, 8))

    hb = ax.hexbin(x, y, C=z, gridsize=100, cmap='jet', mincnt=0, reduce_C_function = reduce_function)
    cb = plt.colorbar(hb, ax=ax)
    cb.set_label('Counts Per Second')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_title('Background Radiation Level')
    plt.show()
















'''
import matplotlib.pyplot as plt
import csv
import math

if __name__ == "__main__":
    t = []
    x = []
    y = []
    z = []

    with open('20190826-214237.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            lat = row[1]
            lon = row[2]
            if (lat) and (lon):
                print(row)
                t.append(float(row[0]))
                x.append(float(row[1])-3805)
                y.append(float(row[2])-7826)
                z.append(math.log10(float(row[3])))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x, y, c=z, cmap=plt.cm.jet)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_title('Background Radiation Level')
    plt.show()
'''