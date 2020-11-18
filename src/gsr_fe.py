# SCARES
# Capstone Fall 2020
# GSR Feature Extraction

# Import Modules

import math as m
import numpy as np
from scipy import signal as sig
from cvxEDA import cvxEDA

def gsr_fe(gsr):

    # Define Signal Properties
    fs = 20
    Ts = 1/fs
    l_window = 10

    # Deconvolve GSR into Components
    scr, driver, scl, _,_,_,_ = cvxEDA(gsr, Ts)


    # Extract Time Domain Features
    ScrMaxDeriv = np.amax(np.diff(scr)/Ts)
    ScrAvgDeriv = (scr[len(scr)-1]-scr[0])/l_window
    ScrAvg = np.mean(scr)
    GsrStDev = np.std(gsr)
    GsrDRange = np.amax(gsr) - np.amin(gsr)
    SclMaxDeriv = np.amax(np.diff(scl)/Ts)
    SclAvgDeriv = (scl[len(scr)-1]-scl[1])/l_window

    peak_ind,_ = sig.find_peaks(driver,height = 0.1)

    DriverMax = np.amax(driver)
    DriverNum = len(peak_ind)

    # Extract Frequency Domain Features
    Y = np.fft.fft(gsr)
    P2 = np.abs(Y/len(gsr))
    P1 = P2[0:m.floor(len(gsr)/2)+1]
    P1[1:-1] = 2*P1[1:-1]
    f = fs*np.arange(m.floor(len(gsr)/2)+1)/len(gsr);


    idxmin = np.argmax(f >= 0.2)
    idxmax = np.argmax(f >= 1.5)
    Fpower = sum(P1[idxmin:(idxmax)])

    # Ouput Features
    features = [ScrMaxDeriv,ScrAvgDeriv,ScrAvg,GsrStDev,GsrDRange,
                SclMaxDeriv,SclAvgDeriv,DriverMax,DriverNum,Fpower]
    return features