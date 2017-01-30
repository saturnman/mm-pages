# -*- coding: utf-8 -*-
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import _pybridge
from matplotlib import collections
from random import shuffle
import matplotlib.patches as mpatches

class SimulatedAnnealingTSP:
    pointList = []
    lineList = []
    pointSeqList = []
    width = 800
    height = 800
    numPoints = 50
    temperature = 10000.0
    @staticmethod
    def setup():
        #init
        width = SimulatedAnnealingTSP.width
        height = SimulatedAnnealingTSP.height
        SimulatedAnnealingTSP.pointList = []
        SimulatedAnnealingTSP.pointSeqList = []
        SimulatedAnnealingTSP.lineList = []
        for i in range(SimulatedAnnealingTSP.numPoints):
            x = nm.random.randint(width)
            y = nm.random.randint(height)
            SimulatedAnnealingTSP.pointList.append((x,y))
            SimulatedAnnealingTSP.pointSeqList.append((x,y))
        shuffle(SimulatedAnnealingTSP.pointSeqList)
        for i in range(SimulatedAnnealingTSP.numPoints):
            SimulatedAnnealingTSP.lineList.append((SimulatedAnnealingTSP.pointSeqList[i],SimulatedAnnealingTSP.pointSeqList[(i+1)%SimulatedAnnealingTSP.numPoints]))

    @staticmethod
    def getTotalLength():
        result = 0.0
        for l in SimulatedAnnealingTSP.lineList:
            result += nm.math.sqrt((l[0][0]-l[1][0])**2+(l[0][1]-l[1][1])**2)
        return result

    @staticmethod
    def step():
        SimulatedAnnealingTSP.temperature -= 1
        origLength = SimulatedAnnealingTSP.getTotalLength()
        resultLineList = []
        resultSeqList = []
        for p in SimulatedAnnealingTSP.pointSeqList:
            resultSeqList.append(p)

        pos1 = nm.random.randint(SimulatedAnnealingTSP.numPoints)
        pos2 = nm.random.randint(SimulatedAnnealingTSP.numPoints)
        if pos1==pos2:
            return
        if pos1 > pos2:
            pos1,pos2 = pos2,pos1
        tmpList = []
        for i in range(pos1,pos2):
            tmpList.append(SimulatedAnnealingTSP.pointSeqList[i])
        tmpList.append(SimulatedAnnealingTSP.pointSeqList[pos2])
        tmpList.reverse()
        for i in range(pos1, pos2):
            resultSeqList[i] = tmpList[i-pos1]
        resultSeqList[pos2] = tmpList[pos2-pos1]

        resultLineList = []
        for i in range(SimulatedAnnealingTSP.numPoints):
            resultLineList.append((resultSeqList[i],resultSeqList[(i+1)%SimulatedAnnealingTSP.numPoints]))
        resultLength = 0.0
        for l in resultLineList:
            resultLength += nm.math.sqrt((l[0][0]-l[1][0])**2+(l[0][1]-l[1][1])**2)
        if resultLength < origLength:
            #accept
            SimulatedAnnealingTSP.pointSeqList = resultSeqList
            SimulatedAnnealingTSP.lineList = resultLineList
        else:
            if nm.random.random < nm.math.exp((resultLength-origLength)/SimulatedAnnealingTSP.temperature):
                SimulatedAnnealingTSP.pointSeqList = resultSeqList
                SimulatedAnnealingTSP.lineList = resultLineList

    @staticmethod
    def draw():
        lineList = SimulatedAnnealingTSP.lineList
        linecollections = collections.LineCollection(lineList)
        fig = plt.gcf()
        fig.clf()
        fig.patch.set_facecolor("w")
        DPI = fig.get_dpi()
        fig.set_size_inches(800.0/float(DPI),600.0/float(DPI))
        plt.axis('off')
        ax = fig.add_subplot(111)
        ax.add_collection(linecollections, autolim=True)

        for x in SimulatedAnnealingTSP.pointList:
            ax.scatter(x[0],x[1],s=10,c="#ff0000",alpha=0.8)
        totalLength = SimulatedAnnealingTSP.getTotalLength()
        desp_patch = mpatches.Patch(color='red',
                                    label="temperatur:%f,length=%f" % (SimulatedAnnealingTSP.temperature,totalLength))
        # draw_Barnsley(ax)
        ax.legend(handles=[desp_patch])
        ax.axis("equal")
        ax.set_axis_off()
        ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
        ax.invert_yaxis()
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
        fig.clf()

def SimulatedAnnealingTSP_draw(data):
    SimulatedAnnealingTSP.draw()

def SimulatedAnnealingTSP_step(data):
    SimulatedAnnealingTSP.step()

def SimulatedAnnealingTSP_setup(data):
    SimulatedAnnealingTSP.setup()

PyBridge.registerHandler("SimulatedAnnealingTSP_setup",SimulatedAnnealingTSP_setup)
PyBridge.registerHandler("SimulatedAnnealingTSP_draw", SimulatedAnnealingTSP_draw)
PyBridge.registerHandler("SimulatedAnnealingTSP_step", SimulatedAnnealingTSP_step)
