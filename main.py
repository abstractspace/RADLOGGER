

import smopy

import matplotlib.pyplot as plt
import csv
import numpy as np
import matplotlib.colors as mcolors
import mplleaflet


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

    filelist = ['20190826-214237.csv', '20190827-141146', '20190827-184304']
    #filelist = ['20190827-184304']
    for filen in filelist:
        with open(filen,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                lat = row[1]
                lon = row[2]
                if (lat) and (lon):
                    print(row)
                    t.append(float(row[0]))

                    lat = float(row[1])
                    latd = lat//100
                    latm = lat  - 100*latd
                    lata.append(latd + latm/60)

                    lon = float(row[2])
                    lond = lon // 100
                    lonm = lon - 100 * lond
                    lona.append(-1.0*(lond + lonm / 60))

                    z.append(float(row[3]))

    map = smopy.Map((min(lata), min(lona), max(lata), max(lona)), z=19)

    x, y = map.to_pixels(np.asarray(lata), np.asarray(lona))
    ax = map.show_mpl(figsize=(8, 8))
    #ax.plot(x, y, 'or', ms=10, mew=2);

    #plt.hold(True)
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.scatter(lona, lata, c=z, cmap=plt.cm.jet)
    hb = ax.hexbin(x, y, C=z, gridsize=1000, cmap='jet', mincnt=0, reduce_C_function = reduce_function)
    #cb = fig.colorbar(hb, ax=ax)
    #cb.set_label('Counts Per Second')
    #gamma = 0.0
    #ax.hist2d(lona, lata, bins = 200, weights = z, norm=mcolors.PowerNorm(gamma), cmap=plt.cm.jet)
    #ax.plot(t, z, '*--')
    #print(lata)
    #print(lona)
    #ax.plot(lona, lata)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_title('Background Radiation Level')
    plt.show()
    #mplleaflet.show()
















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