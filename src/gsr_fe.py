# SCARES
# Capstone Fall 2020
# GSR Feature Extraction

# Import

import numpy as np
from scipy import signal as sig
from cvxEDA import *

def gsr_fe(gsr):

    # Define Signal Properties
    fs = 20
    Ts = 1/fs
    l_window = 10

    # Deconvolve GSR into Components

    scr, driver, scl, _,_,_,_ = cvxEDA(gsr, Ts)
    scr(np.where(scr < 0)) = 0

    scr = []
    scl = []
    driver = []

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
    fft_gsr = np.fft.fft(gsr)/len(gsr)
    fft_gsr = fft_gsr[range(int(len(gsr)/2))]
    values = np.arange(int(len(gsr)/2))
    timePeriod = len(gsr)/fs

    f = values/timePeriod
    f_pow = np.square(np.absolute(fft_gsr))

    min_idx = np.where(f >= 0.2)
    min_idx = min_idx[0]
    max_idx = np.where(f >= 1.5)
    max_idx = max_idx[0]+1

    f_pow = np.sum(f_pow[min_idx:max_idx])

    features = [f_powm,ScrMaxDeriv,ScrAvgDeriv,ScrAvg,GsrStDev,GsrDRange,
                SclMaxDeriv,SclAvgDeriv,DriverMax,DriverNum,f_pow]

    return features