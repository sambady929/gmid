import numpy as np
import pandas as pd
import matplotlib.pyplot as mp

class gmidLUT:
    def __init__(self, csv_str, dev_type):
        self.type = dev_type
        #csv_str = self.type + '.csv'
        #self.csv_np = np.array(np.loadtxt(csv_str, delimiter=',', dtype=float))
        self.csv = pd.read_csv(csv_str, header=None, delim_whitespace=True)
        
        self.csv.columns = ['col1', 'L', 'W', 'vgs', 'vds', 'vsb', 'gm', 'gmb', 'gds', 'ron', 
                            'vdsat', 'vth', 'vearly', 'id', 'cgg', 'cgs', 'cgb', 'cgd', 'cds', 'beff']
        self.csv.drop('col1', axis=1, inplace=True)
        
        self.csv['gmid'] = self.csv['gm'] / self.csv['id']
        self.csv['jd'] = self.csv['id'] / self.csv['W']
        self.csv['ft'] = self.csv['gm'] / (2*np.pi*self.csv['cgg'])
        self.csv['intrinsic'] = self.csv['gm'] / self.csv['gds']
        self.csv['fom_noise'] = self.csv['ft'] * self.csv['gmid']
        self.csv['fom_bw'] = self.csv['ft'] * self.csv['intrinsic']
        self.csv['rds'] = 1 / self.csv['gds']
    
    def print_unique(self, param):
        array = self.csv[param].unique()
        return print(array)
    
    def find_closest_unique(self, param, value):
        array = self.csv[param].unique()
        index = np.abs(array - value).argmin()
        return array[index]
    
    def find_closest_unique_index(self, param, value):
        array = self.csv[param].unique()
        index = np.abs(array - value).argmin()
        return array[index]
    
    def find_two_closest(self, param, value):
        array = self.csv[param].unique().sort()
        return [array[np.searchsorted(array, value)] , array[np.searchsorted(array, value)]-1]

    # find corresponding param2 for a given param1 value. Used to numerically pinpoint values on a graph after plotting graph
    def find_corresp(self, const_array, param1, value, param2):
        filtcsv = self.wavefilter(const_array)
        
        array = filtcsv[param1].unique()
        dist = abs(filtcsv[param1] - value)
        index = np.where(dist == min(dist))[0][0]
        
        param1v = array[index]
        param2v = filtcsv.loc[filtcsv[param1] == param1v][param2].iat[0]
        return param2v

    # filter CSV
    def wavefilter(self, const_array):
        for i in range(round(len(const_array)/2)):
            const_array[i*2+1] = self.find_closest_unique(const_array[i*2], const_array[i*2+1])
        return self.csv.loc[self.csv[const_array[0]]==const_array[1]].loc[self.csv[const_array[2]]==const_array[3]].loc[self.csv[const_array[4]]==const_array[5]]
    
    def wavefilterNP(self, const_array, y_ax, x_ax):
        ynp = self.wavefilter(const_array)[y_ax].to_numpy()
        xnp = self.wavefilter(const_array)[x_ax].to_numpy()
        return [xnp,ynp]
    
    def waveVsWave(self, const_array, y_ax, x_ax):
        # Initialize plot
        fig, ax = mp.subplots()
        it=0
        mod_const = const_array
        # Iterate through const_array and plot each combination
        for i in range(round(len(mod_const)/2)):
            var = mod_const[i*2]
            val = mod_const[i*2+1]
            if isinstance(val, (list, np.ndarray)):  # Check if val is an array
                it=1
                itval=val
                itindex=i*2+1
        print(it)
        if it==1:
            for v in itval:
                mod_const[itindex] = v
                filtcsv = self.wavefilter(mod_const)
                mp.plot(filtcsv[x_ax], filtcsv[y_ax], label="{var} = {val}".format(var=mod_const[itindex-1], val=mod_const[itindex]))
        else:
            filtcsv = self.wavefilter(mod_const)
            mp.plot(filtcsv[x_ax], filtcsv[y_ax])

        # Set axis labels and title
        mp.xlabel("{var}".format(var=x_ax))
        mp.ylabel("{var}".format(var=y_ax))
    
        # Move legend outside the plot
        if it==1:
            mp.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        mp.grid(visible=True, which='major', axis='both')
        mp.tight_layout()
        mp.show()
    
    def interpolate(self, y1, y2, y3, z1, z2):
        z3 = np.zeros(len(z1))
        delta=y2-y1
        y1_weight = 1-abs((y3-y1))/delta
        y2_weight = 1-abs((y3-y2))/delta
        for i in range(len(z1)):
            z3[i] = z1[i]*y1_weight + z2[i]*y2_weight
        return z3
    
    def plot_jd(self, vsb, vds, lengths):
        inar = ['vsb', vsb, 'vds', vds, 'L', lengths]
        self.waveVsWave(inar, 'jd', 'gmid')
        mp.yscale('log')
    
    def plot_intrinsic(self, vsb, vds, lengths):
        inar = ['vsb', vsb, 'vds', vds, 'L', lengths]
        self.waveVsWave(inar, 'intrinsic', 'gmid')
    
    def plot_ft(self, vsb, vds, lengths):
        inar = ['vsb', vsb, 'vds', vds, 'L', lengths]
        self.waveVsWave(inar, 'ft', 'gmid')
        mp.yscale('log')
    
    def plot_vdsat(self, vsb, vds, lengths):
        inar = ['vsb', vsb, 'vds', vds, 'L', lengths]
        self.waveVsWave(inar, 'vdsat', 'gmid')
    
    def plot_vearly(self, vsb, vds, lengths):
        inar = ['vsb', vsb, 'vds', vds, 'L', lengths]
        self.waveVsWave(inar, 'vearly', 'gmid')
        
    def plot_fomnoise(self, vsb, vds, lengths):
        inar = ['vsb', vsb, 'vds', vds, 'L', lengths]
        self.waveVsWave(inar, 'fom_noise', 'jd')
    
    def plot_fombw(self, vsb, vds, lengths):
        inar = ['vsb', vsb, 'vds', vds, 'L', lengths]
        self.waveVsWave(inar, 'fom_bw', 'jd')

def testdg():
    dgnfet = gmidLUT('data/dgnfet.csv', 'dgnfet')
    inar=['vsb', 0, 'vgs', [0.1, 0.4, 0.8, 1.2], 'L', 5e-6]
    dgnfet.waveVsWave(inar, 'id', 'vds')
    
def testinterp():
    dgnfet = gmidLUT('data/nfet.csv', 'nfet')
    inar=['vsb', 0, 'vds', 1, 'L', 5e-7]
    [gmid1, jd1]=dgnfet.wavefilterNP(inar, 'gmid', 'jd')
    inar=['vsb', 0, 'vds', 1, 'L', 1e-6]
    [gmid2, jd2]=dgnfet.wavefilterNP(inar, 'gmid', 'jd')
    gmid3 = dgnfet.interpolate(5e-7, 1e-6, 7.5e-7, gmid1, gmid2)
    jd3 = dgnfet.interpolate(5e-7, 1e-6, 7.5e-7, jd1, jd2)
    fig, ax = mp.subplots()
    mp.plot(jd1,gmid1)
    mp.plot(jd2,gmid2)
    mp.plot(jd3,gmid3)
    mp.show()