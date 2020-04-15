#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
*********************************************
*
* Covid19 Data Visualization
*
* https://github.com/pcm-dpc/COVID-19
* version: 20200415c
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
    #regionCode = [121]                      #Province
    typeRegion = 'denominazione_regione'   #Regioni
    #typeRegion = 'denominazione_provincia'  #Province
    norm = False
    addTotal = False
    yscale = "log"

def main():
    #try:
    print(sys.argv[1])
    folder_regione = sys.argv[1] + '/dati-regioni'
    folder_province = sys.argv[1] + '/dati-province'
    #dates, headers, R = readDataFiles(sys.argv[1])
    #processData(dates, headers, R, dP.categ, dP.customRegionCode, dP.regionCode, dP.typeRegion, dP.norm, dP.addTotal, dP.yscale)
    processData(folder_regione, 'totale_positivi', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, dP.yscale)
    processData(folder_regione, 'nuovi_positivi', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, 'linear')
    processData(folder_regione, 'variazione_totale_positivi', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, 'linear')
    processData(folder_regione, 'deceduti', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, dP.yscale)
    processData(folder_regione, 'terapia_intensiva', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, dP.yscale)
    processData(folder_regione, 'ricoverati_con_sintomi', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, dP.yscale)
    processData(folder_regione, 'totale_ospedalizzati', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, dP.yscale)
    processData(folder_regione, 'isolamento_domiciliare', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, dP.yscale)
    processData(folder_regione, 'dimessi_guariti', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, dP.yscale)
    processData(folder_regione, 'tamponi', True, [5,9,12,20], 'denominazione_regione', dP.norm, dP.addTotal, dP.yscale)
    processData(folder_province, 'totale_casi', True, [121], 'denominazione_provincia', dP.norm, dP.addTotal, dP.yscale)
    
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
def processData(folder, categ, customRegionCode, regionCode, typeRegion, norm, addTotal, yscale):
    dates, headers, R = readDataFiles(folder)
    print(dates)
    print(headers)
    #print(R[date].loc[16, 'tamponi'])
    #print(R[date].iloc[16, 3])
    if not customRegionCode:
        regionCode = R[dates[0]].index.tolist()
    
    totA = []
    for i in regionCode:
        A = []
        for date in dates:
            A.append(R[date].loc[i, categ])
        if norm:
            A = A/max(A)
        if addTotal:
            try:
                totA = np.add(totA, A)
            except:
                totA = A
        plt.plot(dates, A, label=R[date].loc[i, typeRegion])
    
    if addTotal:
        if norm:
            totA = totA/max(totA)
        print(totA)
        plt.plot(dates, totA, label='Totale')
    plt.title(categ)
    plt.xticks(rotation=45)
    plt.yscale(yscale)
    plt.legend()
    plt.show()
    #plt.savefig(dates[-1] + '_summary.pdf', dpi = 640, format = 'pdf')  # Save plot
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
