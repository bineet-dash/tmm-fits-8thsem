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


def get_n_dbr_r(wavelength, n_stack):
    n_list = []
    for i in range(n_stack):
        n_list += [1.47,2.1]    
    return n_list
    
def get_d_dbr_r(n_stack):
    d_a = 48
    d_b = 104
    single_stack_d_list = [d_b,d_a]
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
            
def get_n_list(wv):
    n_list = [1]+ get_n_dbr_r(np.floor(wv),number_of_bilayers)+ [n_gold(np.floor(wv))] +[1]
    return n_list       
     
     
main_fig = plt.figure(100)
plt.ylim([0,1])

wv_l=350
wv_u=1000
wv_range = np.linspace(wv_l,wv_u,num=wv_u-wv_l+1)

Rnorm = []
for wv in wv_range:
    number_of_bilayers = 12
    d_list = [inf] + get_d_dbr_r(number_of_bilayers)+ [50] + [inf]
    n_list = get_n_list(wv)
    del d_list[len(d_list)-3]
    del n_list[len(n_list)-3]
    Rnorm.append(reflectivity(wv,n_list,d_list))
plt.plot(wv_range, Rnorm, 'red', label ="12L Simulation")

expt_wv = []
expt_10L = []
expt_12L = []
with open("SN116_20th_March.tsv") as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        expt_wv.append(row['wv'])
        expt_10L.append(row['10L'])
        expt_12L.append(row['12L'])
expt_wv = map(float,expt_wv)
expt_10L = [i*0.01 for i in map(float,expt_10L)]
expt_12L = [i*0.01 for i in map(float,expt_12L)]
plt.plot(expt_wv,expt_12L, 'black', label = "SN116 12L")



expt_nm_wv = []
expt_nm_10L = []
expt_nm_12L = []
with open("no_metal_10_12L.tsv") as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        expt_nm_wv.append(row['wv'])
        expt_nm_10L.append(row['10L'])
        expt_12L.append(row['12L'])
expt_nm_wv = map(float,expt_nm_wv)
expt_nm_10L = map(float,expt_nm_10L)
expt_nm_12L = map(float,expt_nm_12L)

expt_nm_10L = [i/max(expt_nm_10L) for i in map(float,expt_nm_10L)]
expt_nm_12L = [i/max(expt_nm_10L) for i in map(float,expt_nm_12L)]
plt.plot(expt_nm_wv[0::5],expt_nm_10L[0::5], 'grey', label = "SN116 No Metal 12L")


plt.xlabel('Wavelength (nm)')
plt.ylabel('Fraction reflected')
plt.title('Reflection of unpolarized light at 0$^\circ$ incidence')
plt.legend(loc=7, framealpha = 0.5)

def get_field(event):
    plt.figure(200)
    ax = plt.subplot()
    if event.xdata == None:
        plt.clf()
    else:
        d_copied = list(d_list)
        d_copied[0] = d_copied[len(d_copied)-1] = 0
        x_range = np.linspace(0,sum(d_copied),num=sum(d_copied))
        wv = np.floor(event.xdata)
        n_list = get_n_list(wv)
        del n_list[len(n_list)-3]
        E_norm = e_field(wv, x_range,n_list, d_list)
        E_norm = [float(i)/max(E_norm) for i in E_norm]
        plt.plot(x_range,E_norm, label="Field for $\lambda$="+str(wv))
    ax.set_xticks(np.cumsum(d_copied),minor=True)
    ax.xaxis.grid(True,which='minor')
    plt.xlabel('Distance along device (nm)')
    plt.ylabel('Normalized Electric Field')
    plt.title('Electric Field Across the device')
    plt.legend(loc=7, framealpha = 0.5)
    plt.show() 

cid = main_fig.canvas.mpl_connect('button_press_event', get_field)
plt.show()