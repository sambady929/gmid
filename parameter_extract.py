import numpy as np
import pandas as pd
import matplotlib.pyplot as mp

class device:
    def __init__(self, comp):
        self.type = comp
        csv_str = self.type + '.csv'
        self.csv_np = np.array(np.loadtxt(csv_str, delimiter=',', dtype=float))
        self.csv = pd.read_csv(csv_str)
        self.csv.columns = ['vgs', 'length', 'gm', 'Id', 'gds', 'cgg', 'vgs1', 'vds', 'vsb', 'gmId', 'Jd', 'ft', 'Avo', 'FoM']
        self.csv.drop('vgs1', axis=1)
    
    # retrieve the unique value for a parameter that's closest to the desired value to avoid interpolation
    def find_closest_unique(self, param, value):
        array = np.sort(self.csv[param].unique())
        dist = abs(array - value)
        index = np.where(dist == min(dist))[0][0]
        return array[index]
    
    def find_closest_unique_index(self, param, value):
        array = self.csv[param].unique()
        dist = abs(array - value)
        index = np.where(dist == min(dist))[0][0]
        return index

    def find_corresp(self, length, vds, vsb, param1, value, param2):
        filtcsv = self.wavefilter(length, vds, vsb)
        array = filtcsv[param1].unique()
        dist = abs(array - value)
        index = np.where(dist == min(dist))[0][0]
        return self.csv[param2][index]

    # filter CSV by length, vds, and vsb to then be manipulated
    def wavefilter(self, length_user, vds_user, vsb_user):
        length = self.find_closest_unique('length', length_user)
        vds = self.find_closest_unique('vds', vds_user)
        vsb = self.find_closest_unique('vsb', vsb_user)
        filtlength = self.csv.loc[self.csv['length'] == length]
        filtvds = filtlength.loc[filtlength['vds'] == vds]
        filtvsb = filtvds[filtvds['vsb'] == vsb]
        return filtvsb
    
    # plot one wave against another (how diabolical!)
    def waveVsWave_plot(self, length, vds, vsb, y_ax, x_ax):
        filtcsv = self.wavefilter(length, vds, vsb)
        mp.plot(filtcsv[x_ax], filtcsv[y_ax])
        mp.xscale('log')
        mp.grid(visible=True, which='major', axis='both')

def nfettest():
    nfet = device('nfet')
    nfet.waveVsWave_plot(200E-9, 0.3, 0.1, 'gmId', 'Jd')
    Jd = nfet.find_corresp(200E-9, 0.3, 0.1, 'gmId', 16, 'Jd')
    print(Jd)

nfettest()