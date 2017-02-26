# -*- coding: utf-8 -*-
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import _pybridge
from matplotlib import collections
from matplotlib import gridspec
from random import shuffle
import matplotlib.patches as mpatches

class Gene(object):
    def __init__(self):
        self.citySequence = range(GeneticTSP.numPoints)
        shuffle(self.citySequence)
        self.length = GeneticTSP.computeLength(self.citySequence)

    def copy(self):
        newObj = Gene()
        newObj.citySequence = self.citySequence[:]
        newObj.length = self.length
        return newObj

    def mutate(self):
        pos1 = 0
        pos2 = 0
        while pos1 == pos2:
            pos1 = nm.random.randint(GeneticTSP.numPoints)
            pos2 = nm.random.randint(GeneticTSP.numPoints)
        if pos1 > pos2:
            pos1, pos2 = pos2, pos1
        tmpList = []
        for i in range(pos1, pos2):
            tmpList.append(self.citySequence[i])
        tmpList.append(self.citySequence[pos2])
        tmpList.reverse()
        for i in range(pos1, pos2):
            self.citySequence[i] = tmpList[i - pos1]
        self.citySequence[pos2] = tmpList[pos2 - pos1]
        self.length = GeneticTSP.computeLength(self.citySequence)

    def crossover(self,other):
        pos1 = 0
        pos2 = 0
        while pos1 == pos2:
            pos1 = nm.random.randint(GeneticTSP.numPoints)
            pos2 = nm.random.randint(GeneticTSP.numPoints)
        if pos1 > pos2:
            pos1, pos2 = pos2, pos1
        otherGeneCrossOverIndexList = []
        cityListToShuffle = []
        otherGeneCityList = []
        for pos in range(pos1,pos2+1):
            city = self.citySequence[pos]
            cityListToShuffle.append(city)
            otherIndex = other.citySequence.index(city)
            otherGeneCrossOverIndexList.append(otherIndex)
        sorted(otherGeneCrossOverIndexList)
        for idx in otherGeneCrossOverIndexList:
            otherGeneCityList.append(other.citySequence[idx])

        for idx in range(len(cityListToShuffle)):
            other.citySequence[otherGeneCrossOverIndexList[idx]] = cityListToShuffle[idx]
            self.citySequence[pos1+idx] = otherGeneCityList[idx]
        self.length = GeneticTSP.computeLength(self.citySequence)
        other.length = GeneticTSP.computeLength(other.citySequence)

class GeneticTSP:
    pointList = []
    lineList = []
    pointSeqList = []
    width = 1000
    height = 800
    numPoints = 30
    numAgents = 30
    agentList = []
    generation = 0
    top5AgentArray = None
    @staticmethod
    def setup():
        #init
        width = GeneticTSP.width
        height = GeneticTSP.height
        GeneticTSP.pointList = []
        GeneticTSP.pointSeqList = []
        GeneticTSP.lineList = []
        GeneticTSP.generation = 0
        for i in range(GeneticTSP.numPoints):
            x = nm.random.randint(width)
            y = nm.random.randint(height)
            GeneticTSP.pointList.append((x,y))
            GeneticTSP.pointSeqList.append((x,y))
        shuffle(GeneticTSP.pointSeqList)
        for i in range(GeneticTSP.numPoints):
            GeneticTSP.lineList.append((GeneticTSP.pointSeqList[i],GeneticTSP.pointSeqList[(i+1)%GeneticTSP.numPoints]))
        for i in range(GeneticTSP.numAgents):
            GeneticTSP.agentList.append(Gene())

    @staticmethod
    def computeLength(cityList):
        totalLength = 0.0
        prevCity = cityList[-1]
        for c in cityList:
            totalLength += nm.math.sqrt((GeneticTSP.pointList[prevCity][0]-GeneticTSP.pointList[c][0])**2+(GeneticTSP.pointList[prevCity][1]-GeneticTSP.pointList[c][1])**2)
            prevCity = c
        return totalLength

    @staticmethod
    def getTotalLength():
        result = 0.0
        for l in GeneticTSP.lineList:
            result += nm.math.sqrt((l[0][0]-l[1][0])**2+(l[0][1]-l[1][1])**2)
        return result

    @staticmethod
    def step():
        GeneticTSP.generation += 1
        for _ in range(10):
            pos1 = 0
            pos2 = 0
            while pos1 == pos2:
                pos1 = nm.random.randint(GeneticTSP.numPoints/2)
                pos2 = nm.random.randint(GeneticTSP.numPoints/2)
            GeneticTSP.agentList[pos1].crossover(GeneticTSP.agentList[pos2])

        for idx in range(GeneticTSP.numAgents/2):
            #print len(GeneticTSP.agentList)
            GeneticTSP.agentList[idx+GeneticTSP.numAgents/2] = GeneticTSP.agentList[idx].copy()
        for idx in range(GeneticTSP.numAgents/2,GeneticTSP.numAgents):
            if nm.random.random()<0.5:
                GeneticTSP.agentList[idx].mutate()

        GeneticTSP.agentList = sorted(GeneticTSP.agentList,key=lambda p:p.length)
        smallestCity = GeneticTSP.agentList[0]
        GeneticTSP.pointSeqList = []
        for city in smallestCity.citySequence:
            GeneticTSP.pointSeqList.append(GeneticTSP.pointList[city])
        GeneticTSP.lineList = []
        for i in range(GeneticTSP.numPoints):
            GeneticTSP.lineList.append(
                (GeneticTSP.pointSeqList[i], GeneticTSP.pointSeqList[(i + 1) % GeneticTSP.numPoints]))


    @staticmethod
    def draw():
        lineList = GeneticTSP.lineList
        linecollections = collections.LineCollection(lineList)
        fig = plt.gcf()
        fig.clf()
        fig.patch.set_facecolor("w")
        gs = gridspec.GridSpec(1, 2, width_ratios=[2, 4])
        DPI = fig.get_dpi()
        fig.set_size_inches(GeneticTSP.width/float(DPI),GeneticTSP.height/float(DPI))
        plt.axis('off')
        plt.tight_layout(pad=0)
        #ax = fig.add_subplot(111)
        ax1 = plt.subplot(gs[0])
        top5AgentList = []
        for i in range(5):
            citySeq = GeneticTSP.agentList[i].citySequence
            citySeqFix = []
            zeroIndex = citySeq.index(0)
            for _ in range(GeneticTSP.numPoints):
                citySeqFix.append(citySeq[zeroIndex])
                zeroIndex = (zeroIndex + 1)%GeneticTSP.numPoints
            top5AgentList.append(citySeqFix)
        top5AgentArray = nm.array(top5AgentList)
        top5AgentArray = nm.transpose(top5AgentArray)

        table = ax1.table(cellText=top5AgentArray, cellLoc='center', bbox=[0, 0, 1, 1])
        table.set_fontsize(18)

        if GeneticTSP.top5AgentArray is None:
            GeneticTSP.top5AgentArray = top5AgentArray
        else:
            for key, c in table.get_celld().iteritems():
                if GeneticTSP.top5AgentArray[key] != top5AgentArray[key]:
                    c.set(facecolor='#00ff00')
                if key[0]==0:
                    c.set(facecolor='#ff0000')
            GeneticTSP.top5AgentArray = top5AgentArray
        ax1.set_axis_off()
        ax = plt.subplot(gs[1])
        ax.add_collection(linecollections, autolim=True)

        for x in GeneticTSP.pointList:
            ax.scatter(x[0],x[1],s=10,c="#ff0000",alpha=0.8)
        totalLength = GeneticTSP.getTotalLength()
        desp_patch = mpatches.Patch(color='red',
                                    label="generation:%d,length=%f" % (GeneticTSP.generation,totalLength))
        # draw_Barnsley(ax)
        ax.legend(handles=[desp_patch])
        ax.axis("equal")
        ax.set_axis_off()
        ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
        ax.invert_yaxis()
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
        fig.clf()

def GeneticTSP_draw(data):
    GeneticTSP.draw()

def GeneticTSP_step(data):
    GeneticTSP.step()

def GeneticTSP_setup(data):
    GeneticTSP.setup()

PyBridge.registerHandler("GeneticTSP_setup",GeneticTSP_setup)
PyBridge.registerHandler("GeneticTSP_draw", GeneticTSP_draw)
PyBridge.registerHandler("GeneticTSP_step", GeneticTSP_step)
