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
    
    def uniquearray(self):
        print('vgs')
        print(np.sort(self.csv.vgs.unique()))
        print('length')
        print(np.sort(self.csv.length.unique()))
        print('vds')
        print(np.sort(self.csv.vds.unique()))
        print('vsb')
        print(np.sort(self.csv.vsb.unique()))

    def wavefilter(self, length, vds, vsb):
        filtlength = self.csv.loc[self.csv['length'] == length]
        filtvds = filtlength.loc[filtlength['vds'] == vds]
        filtvsb = filtvds[filtvds['vsb'] == vsb]
        return filtvsb
    
    def waveVsWave_plot(self, length, vds, vsb, y_ax, x_ax):
        filtlength = self.csv.loc[self.csv['length'] == length]
        filtvds = filtlength.loc[filtlength['vds'] == vds]
        filtvsb = filtvds[filtvds['vsb'] == vsb]
        mp.plot(filtvsb[x_ax], filtvsb[y_ax])
        mp.xscale('log')
        mp.grid(visible=True, which='major', axis='both')

def nfettest():
    nfet = device('nfet')
    #nfet.waveVsWave_plot(180E-9, 0.4, 0, 'gmId', 'Jd')
    nfet.waveVsWave_plot(180E-9, 0.4, 0, 'gds', 'Id')
    wave = nfet.wavefilter(180E-9, 0.4, 0)
    #index = wave.get_loc[wave['length'] < 16]
    #nfet.waveVsWave(500E-9, 0.4, 0, 'gmId', 'Jd')

nfettest()