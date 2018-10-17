# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 11:44:13 2018

@author: bineet
"""

from __future__ import division, absolute_import

from numpy import inf
import numpy as np
import csv
from matplotlib import  pyplot as plt

from core_lib import reflectivity, e_field


def get_n_dbr(wavelength, n_stack):
    n_list = []
    for i in range(n_stack):
        n_list += [2.1,1.47]    
    return n_list
    
def get_d_dbr(n_stack):
    d_a = 53
    d_b = 103
    single_stack_d_list = [d_a,d_b]
    d_list = []
    for i in range(n_stack):
        d_list += single_stack_d_list
    return d_list        
    
def read_csv(csv_file):
    with open(csv_file,'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            yield [ float(i) for i in row ]

def n_gold(search):
    my_list =  list(read_csv('gold.csv'))
    for sublist in my_list:
        if sublist[0]==search:
            return sublist[1]+1j*sublist[2]
            break
            
wv_l=350
wv_u=1000
wv_range = np.linspace(wv_l,wv_u,num=wv_u-wv_l+1)

number_of_bilayers = 6
d_list = [inf] + [30] + get_d_dbr(number_of_bilayers) + [inf]

def get_n_list(wv, metal=0):
    if metal==1:
        n_list = [1]+ [n_gold(np.floor(wv))] + get_n_dbr(np.floor(wv),number_of_bilayers) +[1]
    else:
        n_list = [1]+ [1] + get_n_dbr(np.floor(wv),number_of_bilayers) +[1]
    return n_list       
     
d_copied = list(d_list)
d_copied[0] = d_copied[len(d_copied)-1] = 0
x_range = np.linspace(0,sum(d_copied),num=sum(d_copied))

def get_field(event):
    plt.figure(200)
    ax = plt.subplot()
    if event.xdata == None:
        plt.clf()
    else:
        wv = np.floor(event.xdata)
        E_norm = e_field(wv, x_range, get_n_list(wv), d_list)
        E_norm = [float(i)/max(E_norm) for i in E_norm]
        plt.plot(x_range,E_norm, label="Field for $\lambda$="+str(wv))
    ax.set_xticks(np.cumsum(d_copied),minor=True)
    ax.xaxis.grid(True,which='minor')
    plt.xlabel('Distance along device (nm)')
    plt.ylabel('Normalized Electric Field')
    plt.title('Electric Field Across the device')
    plt.legend(loc=7, framealpha = 0.5)
    plt.show() 
     

Rnorm = []
for wv in wv_range:
    n_list = get_n_list(wv)
    Rnorm.append(reflectivity(wv,n_list,d_list))
    
main_fig = plt.figure(100)
plt.ylim([0,1])
plt.plot(wv_range, Rnorm, 'red', label ="R1 No metal Simulation")

expt_wv = []
expt_r1 = []
with open("plot_data_ri.tsv") as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        expt_wv.append(row['wv'])
        expt_r1.append(row['R0'])        
expt_wv = map(float,expt_wv)
expt_r1 = [i*0.01 for i in map(float,expt_r1)]
plt.plot(expt_wv, expt_r1, 'black', label ="R1  Simulation")

plt.xlabel('Wavelength (nm)')
plt.ylabel('Fraction reflected')
plt.title('Reflection of unpolarized light at 0$^\circ$ incidence')
plt.legend(loc=7, framealpha = 0.5)

cid = main_fig.canvas.mpl_connect('button_press_event', get_field)
plt.show()