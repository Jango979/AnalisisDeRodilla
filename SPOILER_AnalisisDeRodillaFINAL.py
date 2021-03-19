# -*- coding: utf-8 -*-
"""
Author: César Daniel Bravo Alvarado
Dr. Jose Marco Balleza Ordaz
Dra. Ma Isabel Delgadillo Cano
"""
import pandas as pd
from pandas import read_table, DataFrame
import matplotlib.pyplot as plt
#from scipy.signal import *
from math import floor
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import detrend
from scipy.signal import medfilt
from scipy import signal
from numpy import pi
from numpy import amax


DF1=read_table('Data_Experiment.csv',sep=',',header=None,names=['Tiempo',
                                                                'IRD',
                                                                'IRI',
                                                                'FRD',
                                                                'FRI',
                                                                'PRRD',
                                                                'PIRD',
                                                                'PRRI',
                                                                'PIRI'])
######################################
def Pasa_baja(data=None,n='time',y=None,freq=1):

    DFcopy=data.copy()
    Time=DFcopy[n]
    Y=DFcopy[y]
    NoOffset=detrend(Y,0)
    
    TimeMax=amax(Time)
    NT=len(Time)
    Fs=NT/TimeMax
    Fn=Fs/2
    Wn=2*freq*pi
    
    sos=signal.butter(9,Wn,'lowpass',fs=Fs,output='sos')
    YFiltered=signal.sosfiltfilt(sos,NoOffset)
    print(YFiltered)
    MedFiltered=medfilt(NoOffset)
    
    plt.figure()
    plt.plot(Time,Y)
    plt.plot(Time,NoOffset)
    
    plt.figure()
    plt.plot(Time,NoOffset)
    plt.plot(Time,MedFiltered)
    
    plt.figure()
    plt.plot(Time,NoOffset)
    plt.plot(Time,YFiltered)
    plt.savefig(str(y)+'Filtered.jpg')
    return YFiltered

###########################################################################

def IdentificaPicos(Signal,height=.009,distance=500):
    
    PicosXCurva=[]
    
        
    Picos,_ =find_peaks(Signal,height=.009,distance=500)
    plt.figure()
    plt.plot(Signal)
    plt.show()
    Up_Or_Down=input('Up or Down \n').upper()
    while(Up_Or_Down!='UP' and Up_Or_Down!='DOWN'):
        Up_Or_Down=input('Wrong answer, choose Up or Down\n').upper()
    if Up_Or_Down=='UP':
        Picos,_ =find_peaks(Signal,height=height,distance=distance)
        plt.plot(Signal)
        plt.plot(Picos,Signal[Picos],'x')
        plt.show()
    else:
        Picos,_=find_peaks(-Signal,height=height,distance=distance)
        plt.plot(Signal)
        plt.plot(Picos,Signal[Picos],'x')
        plt.show()
    return Picos

###########################################################################

def Limits(PicosXCurva):
    Lim=[]
    for i in range(0,len(PicosXCurva)):
        if i==0:
            ActualLim=floor(PicosXCurva[i]/2)-1
        else:
            ActualLim=floor((PicosXCurva[i]-PicosXCurva[i-1])/2)-1
        Lim.append(ActualLim)
    RealLim=[]
    for k in range(0,len(Lim)):
        RealLim.append(np.amin(Lim[k])) #se puede tambien devolver los Lim
    return RealLim
    
###########################################################################

def GraphWithLimits(Filtrado,PicosXCurva,RealLim,name):
    Out=[]
    
    plt.figure()
    for i in range(0,len(PicosXCurva)):
        Ex=[]
        A=PicosXCurva[i]-RealLim[i];B=PicosXCurva[i]+RealLim[i]
        Ex.append([A,B])
        Out.append(Filtrado[A:B])
        plt.plot(Filtrado[A:B])
    plt.title('Peaks compared '+ str(name))
    plt.savefig('Peaks compared '+ str(name))    
    return Out

#####################################################
    

DFcopy=DF1.drop(labels='Tiempo',axis=1)

Filtrado=[]
for Categoria in DFcopy.columns:
    Y=Pasa_baja(data=DF1,n='Tiempo',y=Categoria,freq=1)
 #   print(Y)
    Filtrado.append(Y)
    P=IdentificaPicos(Signal=Y)

    Lim=Limits(P)
    print(Lim)
    GraphWithLimits(Y,P,Lim,Categoria)
#print(Lim)