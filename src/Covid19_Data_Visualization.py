#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
*********************************************
*
* Covid19 Data Visualization
*
* https://github.com/pcm-dpc/COVID-19
* version: 20200414a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************
'''
print(__doc__)

import numpy as np
import pandas as pd
import sys, os.path, h5py
import sys, os.path, getopt, time, configparser
import platform, pickle, h5py, csv, glob
from datetime import datetime, date
import matplotlib.pyplot as plt

#**********************************************
''' main '''
#********************************************
class dP:
    #categ = 'totale_positivi'
    #categ = 'nuovi_positivi'
    #categ = 'deceduti'
    categ = 'totale_casi'
    customRegionCode = False
    regionCode = [5,9,12,20]                #Regioni
    #regionCode = [121]                      #Provincie
    #typeRegion = 'denominazione_regione'   #Regioni
    typeRegion = 'denominazione_provincia'  #Provincie
    norm = False
    addTotal = False
    yscale = "linear"

def main():
    #try:
    print(sys.argv[1])
    dates, headers, R = readDataFiles(sys.argv[1])
    processData(dates, headers, R)

    #except:
    #    usage()
    #    sys.exit(2)

#**********************************************
''' Open and process individual files '''
#**********************************************
def readDataFiles(folder):
    # process sample data
    R = {}
    dates = []
    for file in glob.glob(folder+'/*.csv'):
        #print(file)
        date = os.path.splitext(file)[0][-8:]
        if date.isnumeric():
            dates.append(date)
            R[date] = pd.read_csv(file)
            #print(R[date])
            #print(R[date].loc[16, 'tamponi'])
            #print(R[date].iloc[16, 3])
            
    headers = R[dates[0]].columns.tolist()
    dates.sort()
    return dates, headers, R
    
#**********************************************
''' Process data '''
#**********************************************
def processData(dates, headers, R):
    print(dates)
    print(headers)
    #print(R[date].loc[16, 'tamponi'])
    #print(R[date].iloc[16, 3])
    if dP.customRegionCode:
        regionCode = dP.regionCode
    else:
        regionCode = R[dates[0]].index.tolist()
    
    totA = []
    for i in regionCode:
        A = []
        for date in dates:
            A.append(R[date].loc[i, dP.categ])
        if dP.norm:
            A = A/max(A)
        if dP.addTotal:
            try:
                totA = np.add(totA, A)
            except:
                totA = A
        plt.plot(dates, A, label=R[date].loc[i, dP.typeRegion])
    
    if dP.addTotal:
        if dP.norm:
            totA = totA/max(totA)
        print(totA)
        plt.plot(dates, totA, label='Totale')
    plt.title(dP.categ)
    plt.xticks(rotation=45)
    plt.yscale(dP.yscale)
    plt.legend()
    plt.show()
    plt.close()
    
#************************************
''' Lists the program usage '''
#************************************
def usage():
    print('\n Usage:\n')
    print('  python3 Covid19_Data_Visualization.py <folder with data> \n')
    print(' Requires python 3.x. Not compatible with python 2.x\n')

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
