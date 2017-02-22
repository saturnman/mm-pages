# -*- coding: utf-8 -*-
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import _pybridge
from matplotlib import collections
from random import shuffle
import matplotlib.patches as mpatches
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.lines as lines
def register_map():
    startcolor = '#002200'  # a dark olive
    midcolor = '#008800'    # a bright yellow
    endcolor = '#00FF00'    # medium dark red
    cmap2 = col.LinearSegmentedColormap.from_list('linear_density',[startcolor,midcolor,endcolor])
    cm.register_cmap(cmap=cmap2)

class AntColonyTSP:
    pointList = []
    lineList = []
    pointSeqList = []
    width = 1000
    height = 1000
    numPoints = 50
    pheromoneMap = nm.ones((numPoints, numPoints),dtype=nm.float32)
    for i in range(numPoints):
        pheromoneMap[i,i] = 0.0
    runSteps = 0
    numAnts = 10
    lengthMap = nm.zeros((numPoints,numPoints))
    @staticmethod
    def setup():
        #init
        width = AntColonyTSP.width
        height = AntColonyTSP.height
        AntColonyTSP.pointList = []
        AntColonyTSP.pointSeqList = []
        AntColonyTSP.lineList = []
        AntColonyTSP.numAnts = 10
        AntColonyTSP.pheromoneMap = nm.ones((AntColonyTSP.numPoints, AntColonyTSP.numPoints))
        AntColonyTSP.lengthMap = nm.zeros((AntColonyTSP.numPoints, AntColonyTSP.numPoints))
        for i in range(AntColonyTSP.numPoints):
            x = nm.random.randint(width)
            y = nm.random.randint(height)
            AntColonyTSP.pointList.append((x,y))
            AntColonyTSP.pointSeqList.append((x,y))
        shuffle(AntColonyTSP.pointSeqList)
        for i in range(AntColonyTSP.numPoints):
            AntColonyTSP.lineList.append((AntColonyTSP.pointSeqList[i],AntColonyTSP.pointSeqList[(i+1)%AntColonyTSP.numPoints]))
        for i in range(AntColonyTSP.numPoints):
            for j in range(i+1,AntColonyTSP.numPoints):
                p1 = AntColonyTSP.pointList[i]
                p2 = AntColonyTSP.pointList[j]
                l = nm.math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
                AntColonyTSP.lengthMap[i,j] = l
                AntColonyTSP.lengthMap[j,i] = l
        for i in range(AntColonyTSP.numPoints):
            AntColonyTSP.lengthMap[i, i] = 1e-6

    @staticmethod
    def getPheromoneDensityLineList():
        line2dList = []
        min = 0.0
        max = nm.max(AntColonyTSP.pheromoneMap) #larger max
        lineList = []
        colorList = []
        #print 'max='+str(max)
        for i in range(AntColonyTSP.numPoints):
            for j in range(i+1,AntColonyTSP.numPoints):
                p1 = AntColonyTSP.pointList[i]
                p2 = AntColonyTSP.pointList[j]
                density = nm.math.sqrt(AntColonyTSP.pheromoneMap[i,j]/max)
                if density > max * 2.0/10:
                    #line2dList.append(lines.Line2D([p1[0],p2[0]],[p1[1],p2[1]],color=(1.0-density,1.0,1.0-density,0.5)))
                    lineList.append((p1,p2))
                    colorList.append(((1.0-density)/1.5,1.0,(1.0-density)/1.5,0.3))
        result = {'lineList':lineList,'colorList':colorList}
        return result

    @staticmethod
    def virtualAnt():
        cityList = []
        startIndex = 0
        cityList.append(startIndex)
        pheromoneMapCopy = AntColonyTSP.pheromoneMap.copy()
        pheromoneMapCopy[:,0] = 0
        probList = pheromoneMapCopy[startIndex] / (AntColonyTSP.lengthMap[startIndex] + 100.0)
        leftCities = range(1,AntColonyTSP.numPoints)
        for _ in range(AntColonyTSP.numPoints-2):
            nextCityArr = nm.random.choice(AntColonyTSP.numPoints,1,p=probList/nm.sum(probList))
            nextCity = nextCityArr[0]
            nextCityInex = leftCities.index(nextCity)

            del leftCities[nextCityInex]
            cityList.append(nextCity)
            pheromoneMapCopy[:,nextCity] = 0.0
            probList = pheromoneMapCopy[nextCity]/(AntColonyTSP.lengthMap[nextCity]+100.0)
            #if probList[0] > 1e-9:
            #    print 'error zero probablity'
            #    print probList
            #    print pheromoneMapCopy[nextCity]
        cityList.append(leftCities[0])
        return cityList

    @staticmethod
    def getTotalLength():
        result = 0.0
        for l in AntColonyTSP.lineList:
            result += nm.math.sqrt((l[0][0]-l[1][0])**2+(l[0][1]-l[1][1])**2)
        return result

    @staticmethod
    def computeLength(cityList):
        totalLength = 0.0
        prevCity = cityList[-1]
        for c in cityList:
            totalLength += nm.math.sqrt((AntColonyTSP.pointList[prevCity][0]-AntColonyTSP.pointList[c][0])**2+(AntColonyTSP.pointList[prevCity][1]-AntColonyTSP.pointList[c][1])**2)
            prevCity = c
        return totalLength

    @staticmethod
    def updatePheromoneMap(path):
        paramQ = 10000.0
        len = AntColonyTSP.computeLength(path)
        pheromoneDencity = paramQ/(len**2)
        prevCity = path[-1]
        for i in range(AntColonyTSP.numPoints):
            curCity = path[i]
            AntColonyTSP.pheromoneMap[prevCity,curCity] += pheromoneDencity
            AntColonyTSP.pheromoneMap[curCity,prevCity] += pheromoneDencity
            prevCity = curCity
    @staticmethod
    def step():
        AntColonyTSP.runSteps += 1
        shortestPathLength = 0.0
        shortestPath = []
        for i in range(AntColonyTSP.numAnts):
            path = AntColonyTSP.virtualAnt()
            pathLen = AntColonyTSP.computeLength(path)
            if shortestPathLength < 1e-9:
                # first
                shortestPathLength = pathLen
                shortestPath = path
                #AntColonyTSP.updatePheromoneMap(shortestPath)
            elif shortestPathLength > pathLen:
                shortestPathLength = pathLen
                shortestPath = path
        AntColonyTSP.updatePheromoneMap(shortestPath)
        AntColonyTSP.pointSeqList = []
        for c in shortestPath:
            AntColonyTSP.pointSeqList.append(AntColonyTSP.pointList[c])
        AntColonyTSP.pheromoneMap *= 0.97
        AntColonyTSP.lineList = []
        for i in range(AntColonyTSP.numPoints):
            AntColonyTSP.lineList.append(
                (AntColonyTSP.pointSeqList[i], AntColonyTSP.pointSeqList[(i + 1) % AntColonyTSP.numPoints]))
    @staticmethod
    def draw():
        lineList = AntColonyTSP.lineList
        linecollections = collections.LineCollection(lineList,linewidths=1,colors="#FF0000")
        fig = plt.gcf()
        fig.clf()
        fig.patch.set_facecolor("w")
        DPI = fig.get_dpi()
        fig.set_size_inches(AntColonyTSP.width/float(DPI),AntColonyTSP.height/float(DPI))
        plt.axis('off')
        plt.tight_layout(pad=0)
        ax = fig.add_subplot(111)


        #pheromoneList = AntColonyTSP.getPheromoneDensityLineList()
        res = AntColonyTSP.getPheromoneDensityLineList()
        p_lineList = res['lineList']
        p_colorList = res['colorList']
        #for l in pheromoneList:
        #    ax.add_line(l)
        p_collection = collections.LineCollection(p_lineList,colors=p_colorList)
        ax.add_collection(p_collection, autolim=True)
        ax.add_collection(linecollections, autolim=True)
        for x in AntColonyTSP.pointList:
            ax.scatter(x[0],x[1],s=30,c="#FF00FF",alpha=1.0)
        totalLength = AntColonyTSP.getTotalLength()
        desp_patch = mpatches.Patch(color='red',
                                    label="length=%f" % (totalLength))
        # draw_Barnsley(ax)
        ax.legend(handles=[desp_patch])
        ax.axis("equal")
        ax.set_axis_off()
        ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
        ax.invert_yaxis()
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
        fig.clf()

def AntColonyTSP_draw(data):
    AntColonyTSP.draw()

def AntColonyTSP_step(data):
    AntColonyTSP.step()

def AntColonyTSP_setup(data):
    AntColonyTSP.setup()

register_map()
PyBridge.registerHandler("AntColonyTSP_setup",AntColonyTSP_setup)
PyBridge.registerHandler("AntColonyTSP_draw", AntColonyTSP_draw)
PyBridge.registerHandler("AntColonyTSP_step", AntColonyTSP_step)
