# -*- coding: utf-8 -*-
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import _pybridge
from matplotlib import collections

class Pendulum:
    posList = [10,13,16,19,22,25,28,31,34,37]
    speedList = [0,0,0,0,0,0,0,0,0,0]
    coffList = [1,0.99,0.98,0.97,0.96,0.95,0.94,0.93,0.92,0.91]
    delta = 0.002
    @staticmethod
    def step():
        for i in range(len(Pendulum.posList)):
            pos = Pendulum.posList[i]
            speed = Pendulum.speedList[i]
            coff = Pendulum.coffList[i]
            acce = -pos*2*coff
            speed = speed + acce * Pendulum.delta
            pos = pos+speed*Pendulum.delta+0.5*acce*(Pendulum.delta**2)
            Pendulum.posList[i] = pos
            Pendulum.speedList[i] = speed
    @staticmethod
    def draw():
        lineList = []
        lineList.append(((10,20),(110,20)))
        lineList.append(((10,40),(110,40)))
        lineList.append(((10,60),(110,60)))
        lineList.append(((10,80),(110,80)))
        lineList.append(((10,100),(110,100)))
        lineList.append(((10, 120), (110, 120)))
        lineList.append(((10, 140), (110, 140)))
        lineList.append(((10, 160), (110, 160)))
        lineList.append(((10, 180), (110, 180)))
        lineList.append(((10, 200), (110, 200)))
        linecollections = collections.LineCollection(lineList)
        fig = plt.gcf()
        fig.clf()
        fig.patch.set_facecolor("w")
        DPI = fig.get_dpi()
        fig.set_size_inches(800.0/float(DPI),600.0/float(DPI))
        plt.axis('off')
        ax = fig.add_subplot(111)
        ax.add_collection(linecollections, autolim=True)
        ypos = 20
        for x in Pendulum.posList:
            xpos = 60+x
            ax.scatter(xpos,ypos,s=700,c=nm.random.rand(),alpha=0.5)
            ypos += 20
        ax.axis("equal")
        ax.set_axis_off()
        ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
        ax.invert_yaxis()
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
        fig.clf()

def Pendulum_draw(data):
    Pendulum.draw()

def Pendulum_step(data):
    for i in range(70):
        Pendulum.step()

PyBridge.registerHandler("Pendulum_draw", Pendulum_draw)
PyBridge.registerHandler("Pendulum_step", Pendulum_step)
