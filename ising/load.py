# -*- coding: utf-8 -*-
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
#import cmath
import _pybridge
from matplotlib import collections

class Ising:
    width = 200
    height = 200
    temperature = 50.0
    gridData = nm.random.randint(2,size=(width,height))
    dE = 500.0
    @staticmethod
    def draw():
        fig = plt.gcf()
        fig.clf()
        griddata = 1 - Ising.gridData
        plt.grid(which='none', axis='none', linestyle='-', color='r')
        im = plt.imshow(griddata, cmap=plt.cm.gray, interpolation='nearest',vmin=0,vmax=1)
        # matplotlib.pyplot.axis('off')
        DPI = fig.get_dpi()
        fig.set_size_inches(800.0 / float(DPI), 800.0 / float(DPI))
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(im.figure.canvas.get_renderer()._renderer)
        fig.clf()
    @staticmethod
    def step():
        #print Ising.temperature
        width = Ising.width
        height = Ising.height
        gridDataCopy = Ising.gridData.copy()
        for i in range(1500):
            y = nm.random.randint(Ising.width)
            x = nm.random.randint(Ising.height)
            x1 = (x - 1 + height) % height
            x2 = x
            x3 = (x + 1 + height) % height
            y1 = (y - 1 + width) % width
            y2 = y
            y3 = (y + 1 + width) % width
            current = gridDataCopy[x,y]
            numNeighbors = gridDataCopy[x1][y1] + gridDataCopy[x2][y1] + gridDataCopy[x3][y1] + gridDataCopy[x1][
                y2] + gridDataCopy[x3][y2] + gridDataCopy[x1][y3] + gridDataCopy[x2][y3] + gridDataCopy[x3][y3]
            if current==1:
                if numNeighbors<4:
                    Ising.gridData[x][y] = 0
                else:
                    if nm.random.random()<nm.exp(-(2*numNeighbors-8)*Ising.dE/Ising.temperature):
                        Ising.gridData[x][y] = 0
            else:
                if numNeighbors>4:
                    Ising.gridData[x][y] = 1
                else:
                    if nm.random.random()<nm.exp(-(8-2*numNeighbors)*Ising.dE/Ising.temperature):
                        Ising.gridData[x][y] = 1
    @staticmethod
    def setup(width,height,temperature):
        Ising.width = width
        Ising.height = height
        Ising.temperature = temperature
        Ising.gridData = nm.random.randint(2,size=(width,height))
    @staticmethod
    def setTemperature(temperature):
        Ising.temperature = temperature

def Ising_draw(data):
    Ising.draw()

def Ising_step(data):
    Ising.step()

def Ising_setup(data):
    print data
    width = data['width']
    height = data['height']
    temperature = data['temperature']
    try:
        temperature = float(temperature)
        Ising.setup(width, height, temperature)
    except:
        print 'convert to float error'

def Ising_setTemperature(data):
    temperature = data['temperature']
    print temperature
    try:
        temperature = float(temperature)
        Ising.setTemperature(temperature)
    except:
        print 'convert to float error'

PyBridge.registerHandler("Ising_draw", Ising_draw)
PyBridge.registerHandler("Ising_step", Ising_step)
PyBridge.registerHandler("Ising_setup", Ising_setup)
PyBridge.registerHandler("Ising_setTemperature", Ising_setTemperature)
