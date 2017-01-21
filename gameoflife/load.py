import sys
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import _pybridge

class GameOfLife:
    width = 50
    height = 50
    gridData = nm.zeros((width,height))
    @staticmethod
    def setState(w,h,data):
        GameOfLife.width = w
        GameOfLife.height = h
        GameOfLife.gridData = data

    @staticmethod
    def step():
        width = GameOfLife.width
        height = GameOfLife.height
        gridDataCopy = GameOfLife.gridData.copy()
        for y in range(GameOfLife.width):
            for x in range(GameOfLife.height):
                x1 = (x-1+height)%height
                x2 = x
                x3 = (x+1+height)%height
                y1 = (y-1+width)%width
                y2 = y
                y3 = (y+1+width)%width
                numNeighbors = gridDataCopy[x1][y1]+gridDataCopy[x2][y1]+gridDataCopy[x3][y1]+gridDataCopy[x1][y2] + gridDataCopy[x3][y2]+gridDataCopy[x1][y3]+gridDataCopy[x2][y3]+gridDataCopy[x3][y3]
                if numNeighbors < 2 or numNeighbors>3:
                    GameOfLife.gridData[x][y] = 0
                if numNeighbors==2 or numNeighbors==3:
                    if gridDataCopy[x][y]==1:
                        pass
                if numNeighbors==3:
                    if gridDataCopy[x][y]==0:
                        GameOfLife.gridData[x][y] = 1
    @staticmethod
    def draw():
        fig = plt.gcf()
        fig.clf()
        griddata = 1-GameOfLife.gridData
        plt.grid(which='none', axis='none', linestyle='-', color='r')
        im = plt.imshow(griddata, cmap=plt.cm.gray, interpolation='nearest')
        #matplotlib.pyplot.axis('off')
        DPI = fig.get_dpi()
        fig.set_size_inches(1000.0 / float(DPI), 468.0 / float(DPI))
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(im.figure.canvas.get_renderer()._renderer)
        fig.clf()

def GameOfLife_setState(data):
    width = data['width']
    height = data['height']
    gridData = data['gridData']
    gridDataArr = nm.asarray(gridData)
    #print gridDataArr.shape
    GameOfLife.setState(width,height,gridDataArr)

def GameOfLife_step(data):
    GameOfLife.step()

def GameOfLife_draw(data):
    GameOfLife.draw()

PyBridge.registerHandler("GameOfLife_setState", GameOfLife_setState)
PyBridge.registerHandler("GameOfLife_step", GameOfLife_step)
PyBridge.registerHandler("GameOfLife_draw", GameOfLife_draw)
