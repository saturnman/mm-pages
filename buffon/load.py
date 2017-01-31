# -*- coding: utf-8 -*-
from math import sin, cos, pi
import matplotlib
import matplotlib.patches as mpatches
matplotlib.use("agg")
import _pybridge
import matplotlib.pyplot as pl
from matplotlib import collections
import numpy


class Buffon:
    needleList = []
    lineSpace = 50
    numCross = 0
    piEstimationValList = []
    numNeedleList = []
    lineList = []
    needleLength = 30
    world = (500,500)
    numNeedle = 0
    piEstimate = 0.0

    @staticmethod
    def setup():
        Buffon.needleList = []
        Buffon.lineSpace = 50
        Buffon.needleLength = 30
        Buffon.world = (500, 500)
        Buffon.numCross = 0
        Buffon.piEstimationValList = []
        Buffon.piEstimate = 0.0
        Buffon.numNeedleList = []
        Buffon.numNeedle = 0
        for i in range(11):
            Buffon.lineList.append(((0,1+Buffon.lineSpace*i),(500,1+Buffon.lineSpace*i)))
        print Buffon.lineList
    @staticmethod
    def step():
        needleHalf = Buffon.needleLength/2.0
        c = numpy.random.randint(20)
        for i in range(c):
            middle = 500*numpy.random.random(size=(2,))
            rotation = numpy.math.pi*numpy.random.random()
            p = middle[0]+needleHalf*numpy.math.cos(rotation),middle[1]+needleHalf*numpy.math.sin(rotation)
            t = 2*middle-p
            Buffon.needleList.append(((p[0],p[1]),(t[0],t[1])))
            posY = (middle[0] % 50)
            if posY > 25:
                posY = 50-posY
            if posY <= needleHalf*numpy.math.sin(rotation):
                Buffon.numCross += 1
        if Buffon.numCross != 0:
            Buffon.piEstimate = float(2*Buffon.needleLength*Buffon.numNeedle)/(Buffon.lineSpace*Buffon.numCross)
            Buffon.piEstimationValList.append(Buffon.piEstimate)
        else:
            Buffon.piEstimationValList.append(0)
        Buffon.numNeedle += c
        Buffon.numNeedleList.append(Buffon.numNeedle)

    @staticmethod
    def get_lines():
        return Buffon.needleList

def draw(ax):
    lines = Buffon.get_lines()
    linecollections = collections.LineCollection(lines)
    ax.add_collection(linecollections, autolim=True)
    spaceLineCol = collections.LineCollection(Buffon.lineList)
    spaceLineCol.set_facecolor("r")
    spaceLineCol.set_edgecolor("r")
    ax.add_collection(linecollections,autolim=True)
    ax.add_collection(spaceLineCol,autolim=True)
    ax.axis("equal")
    ax.set_axis_off()
    ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
    ax.invert_yaxis()

def Buffon_draw(data):
    fig = pl.gcf()
    fig.patch.set_facecolor("w")
    DPI = fig.get_dpi()
    fig.set_size_inches(1200.0/float(DPI),800.0/float(DPI))

    #for i in xrange(6):
    #    ax = fig.add_subplot(241+i)
    #    draw(ax, rules[i])
    #ax = fig.add_subplot(247)
    #draw_Barnsley(ax)
    #fig.add_subplot(247)
    pl.axis('off')
    ax = fig.add_subplot(121)
    draw(ax)
    ax2 = fig.add_subplot(122)
    ax2.plot(Buffon.numNeedleList,Buffon.piEstimationValList)
    ax2.set_axis_on()
    desp_patch = mpatches.Patch(color='red',label="n needls:%d,pi=%f" %(Buffon.numNeedle,Buffon.piEstimationValList[-1]))
    #draw_Barnsley(ax)
    ax2.legend(handles=[desp_patch])
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
    #pl.show()
    fig.canvas.draw()
    _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
    fig.clf()

def Buffon_setup(data):
    Buffon.setup()

def Buffon_step(data):
    Buffon.step()

PyBridge.registerHandler("Buffon_step", Buffon_step)
PyBridge.registerHandler("Buffon_draw", Buffon_draw)
PyBridge.registerHandler("Buffon_setup", Buffon_setup)

