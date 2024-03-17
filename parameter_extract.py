import numpy as np
import pandas as pd
import matplotlib.pyplot as mp

class device:
    def __init__(self, comp):
        self.type = comp
        csv_str = self.type + '.csv'
        self.csv_np = np.array(np.loadtxt(csv_str, delimiter=',', dtype=float))
        self.csv = pd.read_csv(csv_str)
        self.csv.columns = ['vgs', 'length', 'vds', 'vsb', 'gm', 'Id', 'gds', 'cgg', 'gmId', 'Jd', 'ft', 'Avo', 'FoM']
    
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

    # find corresponding param2 for a given param1 value. Used to numerically pinpoint values on a graph after plotting graph
    def find_corresp(self, length, vds, vsb, param1, value, param2):
        filtcsv = self.wavefilter(length, vds, vsb)
        
        array = filtcsv[param1].unique()
        dist = abs(filtcsv[param1] - value)
        index = np.where(dist == min(dist))[0][0]
        
        param1v = array[index]
        param2v = filtcsv.loc[filtcsv[param1] == param1v][param2].iat[0]
        print(param1v)
        print(param2v)
        return param2v

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


nfet = device('nfet')
nfet.waveVsWave_plot(200E-9, 0.6, 0, 'gmId', 'Jd')
nfet.waveVsWave_plot(1E-6, 0.6, 0, 'gmId', 'Jd')
Jd = nfet.find_corresp(200E-9, 0.4, 0, 'gmId', 17, 'Jd')