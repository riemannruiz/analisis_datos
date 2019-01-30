# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 20:16:35 2019

@author: if715029
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans



data = pd.read_csv('Data/AC.csv', index_col='0')
#%%
def crear_ventanas(data,n_ventana):
    n_data = len(data)
    dat_new = np.zeros((n_data-n_ventana+1,n_ventana))
    for k in np.arange(n_ventana):
        dat_new[:,k] = data[k:(n_data-n_ventana+1)+k]
    return dat_new

#%%
ndias = [5,20,125]
vent = []
for i in ndias:
    vent.append(crear_ventanas(data['Close'],i))
#%%
cont = len(ndias)    
    
for i in range(cont):
    vent[i] = np.transpose((vent[i].transpose()-vent[i].mean(axis=1))/vent[i].std(axis=1))
#%% Función para la gráfica de codo
def grafica_codo_kmeans(data,n_centroides):
    inercias = np.zeros(n_centroides.shape)
    for k in n_centroides:
        model = KMeans(n_clusters=k,init='k-means++').fit(data)
        inercias[k-1] = model.inertia_
    # Grafica de codo
    plt.plot(n_centroides,inercias)
    plt.xlabel('Num grupos')
    plt.ylabel('Inercia')
    plt.show()
    return n_centroides,inercias
#%%
for i in range(cont):
    grafica_codo_kmeans(vent[i],np.arange(1,16))
#%%
model_close = []
for i in range(cont):
    model_close.append(KMeans(n_clusters=4,init='k-means++').fit(vent[i]))

#%% Función para dibujar los centroides del modelo
def ver_centroides(centroides):
    n_subfig = np.ceil(np.sqrt(centroides.shape[0]))
    for k in np.arange(centroides.shape[0]):
        plt.subplot(n_subfig,n_subfig,k+1)
        plt.plot(centroides[k,:])
        plt.ylabel('Grupo %d'%k)
    plt.show()
#%%
for i in range(cont):
    ver_centroides(model_close[i].cluster_centers_)

#%%
clasif_close = []
for i in range(cont):
    clasif_close.append(model_close[i].predict(vent[i]))
    
#%%  
for i in range(cont):
    clasif_close[i]=clasif_close[i][:-len(clasif_close[-1])-1:-1]
    
#%%    
sit = np.zeros(len(clasif_close[0]))
for i in range(cont):
    sit += clasif_close[i]*4**i


