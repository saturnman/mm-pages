# -*- coding: utf-8 -*-
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
#import cmath
import _pybridge
from matplotlib import collections
import matplotlib.colors as col
import matplotlib.cm as cm
from matplotlib import gridspec
from random import shuffle

def discrete_cmap(N=4):
    """create a colormap with N (N<15) discrete colors and register it"""
    # define individual colors as hex values
    cpool = [ '#0000ff', '#ff0000', '#00ff00', '#ffff00', '#000000',
              '#faf214', '#2edfea', '#ea2ec4', '#ea2e40', '#cdcdcd',
              '#577a4d', '#2e46c0', '#f59422', '#219774', '#8086d9' ]
    cmap3 = col.ListedColormap(cpool[0:N], 'indexed')
    cm.register_cmap(cmap=cmap3)
"""0 means CC,1 means DD,2 means DC,3 means CD"""
class SpatialGame:
    width = 120
    height = 120
    gridData = nm.random.randint(2,size=(width,height))
    #gridData = nm.ones((width, height))
    gridData[0:60,:] = 0
    gridReturn = nm.zeros(gridData.shape)
    b = 1.0
    w = 1e-6
    #constants
    CC=0
    DD=1
    DC=2
    CD=3
    @staticmethod
    def draw():
        fig = plt.gcf()
        fig.clf()
        fig.subplots_adjust(top=0.8, bottom=0.05, left=0.01, right=0.99)
        gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])
        x = nm.arange(0, 10, 0.2)
        y = nm.sin(x)
        ax0 = plt.subplot(gs[0])
        ax1 = plt.subplot(gs[1])
        griddata = SpatialGame.gridData
        print griddata[(0,0)]
        plt.grid(which='none', axis='none', linestyle='-', color='r')
        im = ax0.imshow(griddata, cmap=plt.cm.get_cmap('indexed'),interpolation="nearest",vmin=0, vmax=4)
        ax1.scatter(20,20,s=700,c='#0000ff',alpha=1.0)
        ax1.annotate('CC',
                    xy=(20, 20), xycoords='data',
                    xytext=(20, 20), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->"))
        ax1.scatter(20, 40, s=700, c='#ff0000', alpha=1.0)
        ax1.annotate('DD',
                     xy=(20, 40), xycoords='data',
                     xytext=(20, 40), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->"))
        ax1.scatter(20, 60, s=700, c='#00ff00', alpha=1.0)
        ax1.annotate('DC',
                     xy=(20, 60), xycoords='data',
                     xytext=(20, 60), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->"))
        ax1.scatter(20, 80, s=700, c='#ffff00', alpha=1.0)
        ax1.annotate('CD',
                     xy=(20, 80), xycoords='data',
                     xytext=(20, 80), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->"))
        matplotlib.pyplot.axis('off')
        DPI = fig.get_dpi()
        fig.set_size_inches(1200.0 / float(DPI), 1000.0 / float(DPI))
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(im.figure.canvas.get_renderer()._renderer)
        fig.clf()

    @staticmethod
    def updateGridReturn():
        """calculate grid game return"""
        width = SpatialGame.width
        height = SpatialGame.height
        for i in range(height):
            for j in range(width):
                neighborIndexList = SpatialGame.getNeighborIndexList(i,j)
                result = 0.0
                current = SpatialGame.gridData[i,j]
                if current==0 or current==2:
                    for idx in neighborIndexList:
                        if SpatialGame.gridData[idx]==0 or SpatialGame.gridData[idx]==2:
                            result+= 1.0

                else:
                    for idx in neighborIndexList:
                        if SpatialGame.gridData[idx] == 0 or SpatialGame.gridData[idx] == 2:
                            result += SpatialGame.b
                        else:
                            result += SpatialGame.w
                SpatialGame.gridReturn[(i,j)] = result

    @staticmethod
    def updateCellReturn(i,j):
        neighborIndexList = SpatialGame.getNeighborIndexList(i, j)
        result = 0.0
        current = SpatialGame.gridData[i, j]
        if current == 0 or current == 2:
            for idx in neighborIndexList:
                if SpatialGame.gridData[idx] == 0 or SpatialGame.gridData[idx] == 2:
                    result += 1.0

        else:
            for idx in neighborIndexList:
                if SpatialGame.gridData[idx] == 0 or SpatialGame.gridData[idx] == 2:
                    result += SpatialGame.b
                else:
                    result += SpatialGame.w
        SpatialGame.gridReturn[(i, j)] = result

    @staticmethod
    def async_step():
        for i in range(500):
            width = SpatialGame.width
            height = SpatialGame.height
            y = nm.random.randint(width)
            x = nm.random.randint(height)
            neighborIndexList = SpatialGame.getNeighborIndexList(x, y)
            currentReturn = 0.0
            current = SpatialGame.gridData[x, y]
            if current == 0 or current == 2:
                for idx in neighborIndexList:
                    if SpatialGame.gridData[idx] == 0 or SpatialGame.gridData[idx] == 2:
                        currentReturn += 1.0

            else:
                for idx in neighborIndexList:
                    if SpatialGame.gridData[idx] == 0 or SpatialGame.gridData[idx] == 2:
                        currentReturn += SpatialGame.b
                    else:
                        currentReturn += SpatialGame.w
            SpatialGame.gridReturn[(x, y)] = currentReturn
            highestReturn = currentReturn
            highestIdx = (x,y)
            for idx in neighborIndexList:
                if SpatialGame.gridReturn[idx] > highestReturn:
                    # update rule
                    highestIdx = idx
                    highestReturn = SpatialGame.gridReturn[idx]
            if highestIdx != (x, y):
                # update
                if SpatialGame.gridData[(x, y)] == SpatialGame.CC or SpatialGame.gridData[(x, y)] == SpatialGame.DC:
                    if SpatialGame.gridData[highestIdx] == SpatialGame.CC or SpatialGame.gridData[
                        highestIdx] == SpatialGame.DC:
                        # CC
                        SpatialGame.gridData[(x, y)] = SpatialGame.CC
                    else:
                        # CD
                        SpatialGame.gridData[(x, y)] = SpatialGame.CD
                else:
                    if SpatialGame.gridData[highestIdx] == SpatialGame.CC or SpatialGame.gridData[
                        highestIdx] == SpatialGame.DC:
                        SpatialGame.gridData[(x, y)] = SpatialGame.DC
                    else:
                        SpatialGame.gridData[(x, y)] = SpatialGame.DD
                for idx in neighborIndexList:
                    SpatialGame.updateCellReturn(idx[0],idx[1])
            else:
                if SpatialGame.gridData[(x, y)] == SpatialGame.CC or SpatialGame.gridData[(x, y)] == SpatialGame.DC:
                    SpatialGame.gridData[(x, y)] = SpatialGame.CC
                else:
                    SpatialGame.gridData[(x, y)] = SpatialGame.DD


    @staticmethod
    def getNeighborIndexList(x,y):
        width = SpatialGame.width
        height = SpatialGame.height
        x1 = (x - 1 + height) % height
        x2 = x
        x3 = (x + 1 + height) % height
        y1 = (y - 1 + width) % width
        y2 = y
        y3 = (y + 1 + width) % width
        neighborIndexList = [(x1, y1), (x2, y1), (x3, y1), (x1, y2), (x3, y2), (x1, y3), (x2, y3), (x3, y3)]
        shuffle(neighborIndexList)
        return neighborIndexList

    @staticmethod
    def step():
        SpatialGame.updateGridReturn()
        width = SpatialGame.width
        height = SpatialGame.height
        #gridDataCopy = SpatialGame.gridData.copy()
        for i in range(height):
            for j in range(width):
                neighborIndexList = SpatialGame.getNeighborIndexList(i,j)
                highestReturn = SpatialGame.gridReturn[(i,j)]
                highestIdx = (i,j)
                for idx in neighborIndexList:
                    if SpatialGame.gridReturn[idx] > highestReturn:
                        #update rule
                        highestIdx = idx
                        highestReturn = SpatialGame.gridReturn[idx]
                if highestIdx != (i,j):
                    #update
                    if SpatialGame.gridData[(i,j)]==SpatialGame.CC or SpatialGame.gridData[(i,j)]==SpatialGame.DC:
                        if SpatialGame.gridData[highestIdx]==SpatialGame.CC or SpatialGame.gridData[highestIdx]==SpatialGame.DC:
                            #CC
                            SpatialGame.gridData[(i,j)] = SpatialGame.CC
                        else:
                            #CD
                            SpatialGame.gridData[(i,j)] = SpatialGame.CD
                    else:
                        if SpatialGame.gridData[highestIdx] == SpatialGame.CC or SpatialGame.gridData[
                            highestIdx] == SpatialGame.DC:
                            SpatialGame.gridData[(i,j)] = SpatialGame.DC
                        else:
                            SpatialGame.gridData[(i,j)] = SpatialGame.DD
                else:
                    if SpatialGame.gridData[(i,j)]==SpatialGame.CC or SpatialGame.gridData[(i,j)]==SpatialGame.DC:
                        SpatialGame.gridData[(i,j)] = SpatialGame.CC
                    else:
                        SpatialGame.gridData[(i,j)] = SpatialGame.DD

    @staticmethod
    def setup(width,height):
        SpatialGame.width = width
        SpatialGame.height = height
        SpatialGame.gridData = nm.random.randint(2,size=(width,height))

    @staticmethod
    def config(command,b=None,probablity=0.5):

        #probablity is for all CC
        if b is not None:
            SpatialGame.b = b
        if command == 'random':
            mod = [0,1]
            SpatialGame.gridData = nm.random.choice(mod, (SpatialGame.width, SpatialGame.height), p=[probablity, 1 - probablity])
        elif command == 'allc':
            SpatialGame.gridData = nm.zeros((SpatialGame.width,SpatialGame.height))
        elif command == 'alld':
            SpatialGame.gridData = nm.ones((SpatialGame.width,SpatialGame.height))
        else:
            print 'Wrong preset param'

    @staticmethod
    def patch(xIndex,yIndex,objectGridData):
        s = objectGridData.shape
        SpatialGame.gridData[xIndex:xIndex+s[0],yIndex:yIndex+s[1]] = objectGridData

    @staticmethod
    def setb(b):
        SpatialGame.b = b


def SpatialGame_draw(data):
    SpatialGame.draw()

def SpatialGame_step(data):
    SpatialGame.step()


def SpatialGame_asyncstep(data):
    SpatialGame.async_step()

def SpatialGame_patch(data):
    posX = data['posX']
    posY = data['posY']
    d = nm.asarray(data['d'])
    SpatialGame.patch(posX,posY,d)

def SpatialGame_setup(data):
    print data
    width = data['width']
    height = data['height']
    SpatialGame.setup(width,height)

def SpatialGame_setTemperature(data):
    temperature = data['temperature']
    SpatialGame.setTemperature(temperature)


def SpatialGame_setb(data):
    b = float(data['b'])
    SpatialGame.setb(b)

def SpatialGame_config(data):
    command = data['command']
    SpatialGame.config(command)

PyBridge.registerHandler("SpatialGame_draw", SpatialGame_draw)
PyBridge.registerHandler("SpatialGame_step", SpatialGame_step)
PyBridge.registerHandler("SpatialGame_asyncstep",SpatialGame_asyncstep)
PyBridge.registerHandler("SpatialGame_setup", SpatialGame_setup)
PyBridge.registerHandler("SpatialGame_setTemperature", SpatialGame_setTemperature)
PyBridge.registerHandler("SpatialGame_setb",SpatialGame_setb)
PyBridge.registerHandler("SpatialGame_patch",SpatialGame_patch)
PyBridge.registerHandler("SpatialGame_config",SpatialGame_config)
discrete_cmap()
