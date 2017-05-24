# -*- coding: utf-8 -*-
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
from pylab import *
import _pybridge
from matplotlib import collections
from random import shuffle
import matplotlib.patches as mpatches

class PredatorPrey:
    pointList = []
    lineList = []
    pointSeqList = []
    width = 800
    height = 800
    a, b, m, n = 1, 0.8, 1, 0.5
    startX = 1.0
    startY = 1.0
    x = 1.0
    y = 1.0
    dt = 0.01
    @staticmethod
    def setup(x,y):
        #init
        PredatorPrey.startX = x
        PredatorPrey.startY = y
        width = PredatorPrey.width
        height = PredatorPrey.height
        PredatorPrey.x = PredatorPrey.startX
        PredatorPrey.y = PredatorPrey.startY


    @staticmethod
    def step():
        for i in range(10):
            a, b, m, n = 1, 0.8, 1, 0.5
            dx = (a-b*PredatorPrey.y)*PredatorPrey.x*PredatorPrey.dt
            PredatorPrey.x = PredatorPrey.x + dx
            dy = (-m+n*PredatorPrey.x)*PredatorPrey.y*PredatorPrey.dt

            PredatorPrey.y = PredatorPrey.y + dy
    @staticmethod
    def draw():
        fig = plt.gcf()
        fig.clf()
        fig.patch.set_facecolor("w")
        DPI = fig.get_dpi()
        fig.set_size_inches(800.0/float(DPI),600.0/float(DPI))
        #plt.axis('off')
        ax = fig.add_subplot(111)
        a, b, m, n = 1, 0.8, 1, 0.5
        X, Y = meshgrid(arange(-0.1, 4, .3), arange(-0.1, 4, .3))
        U = a * X - b * X * Y
        V = -m * Y + n * X * Y
        Q = ax.quiver(U, V)
        l, r, b, t = axis()
        dx, dy = r - l, t - b
        ax.scatter(PredatorPrey.x, PredatorPrey.y, s=10, c="#ff0000", alpha=0.8)


        desp_patch = mpatches.Patch(color='red',
                                    label="x:%f,y=%f" % (PredatorPrey.x,PredatorPrey.y))
        # draw_Barnsley(ax)
        ax.legend(handles=[desp_patch])
        ax.axis("equal")
        #ax.set_axis_off()
        ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
        fig.clf()

def PredatorPrey_draw(data):
    PredatorPrey.draw()

def PredatorPrey_step(data):
    PredatorPrey.step()

def PredatorPrey_setup(data):
    x = float(data['x'])
    y = float(data['y'])
    PredatorPrey.setup(x,y)

PyBridge.registerHandler("PredatorPrey_setup",PredatorPrey_setup)
PyBridge.registerHandler("PredatorPrey_draw", PredatorPrey_draw)
PyBridge.registerHandler("PredatorPrey_step", PredatorPrey_step)
