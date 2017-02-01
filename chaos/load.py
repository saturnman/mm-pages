import sys
sys.path.append(".")
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import _pybridge

class ChaosModel:
    @staticmethod
    def drawLogisticPopulationModel(r,x1start,x2start,iter_count,lines=1):
        def calculate_trajectory(seed, r, count):
            result = []
            x = seed
            f = lambda r, x: r * x * (1 - x)
            for i in range(0, count):
                x = f(r, x)
                result.append(x)
            return result
        if lines == 1:
            x = range(0, iter_count)
            y1 = calculate_trajectory(0.2, r, iter_count)
            fig = plt.gcf()
            fig.set_size_inches(18.5, 10.5)
            labelText = "seed="+str(x1start)+",r="+str(r)+",steps="+str(iter_count)
            plot1 = plt.plot(x, y1, color="r", label=labelText)
            plt.xlabel("steps")
            plt.ylabel("iterated value")
            fig.canvas.draw()
            _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
            fig.clf()
        elif lines==2:
            x = range(0, iter_count)
            y1 = calculate_trajectory(x1start, r, iter_count)
            y2 = calculate_trajectory(x2start, r, iter_count)
            fig = plt.gcf()
            fig.set_size_inches(18.5, 10.5)
            label1Text = "seed=" + str(x1start) + ",r=" + str(r) + ",steps="+str(iter_count)
            label2Text = "seed=" + str(x2start) + ",r=" + str(r) + ",steps=" + str(iter_count)
            plot1 = plt.plot(x, y1, color="r", label=label1Text)
            plot2 = plt.plot(x, y2, color="b", label=label2Text)
            plt.xlabel("steps")
            plt.ylabel("iterated value")
            fig.canvas.draw()
            _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
            fig.clf()
        else:
            print 'illegal param'
    @staticmethod
    def calc_stable_x(start,r):
        x = start
        res = []
        for i in range(0,400):
            x = r*x*(1-x)
        for j in range(100):
            x = r*x*(1-x)
            res.append(x)
        return res
    @staticmethod
    def drawFibu():
        r = nm.arange(2.501,3.8,0.001)
        s = nm.random.random_sample(r.shape)
        x = ChaosModel.calc_stable_x(s,r)
        points = []
        for i in range(len(x)):
            for j in range(len(x[i])):
                points.append((r[j],x[i][j]))
        (x1,y1) = zip(*points)
        fig = plt.gcf()
        plt.clf()
        plt.axis('off')
        DPI = fig.get_dpi()
        fig.set_size_inches(1200.0/float(DPI),800.0/float(DPI))
        #fig = plt.figure()
        plt.scatter(x1,y1,marker='.',lw=0,color="r", s=1)
        #print dir(fig.canvas.get_renderer())
        #print fig.canvas.get_renderer()
        #print fig.canvas.get_renderer().height
        #print dir(fig._cachedRenderer)
        #print fig.canvas.get_renderer().get_content_extents()
        #print fig.canvas.get_renderer()
        #print fig.canvas.renderer._renderer
        #fig.savefig('fibu.png', dpi=fig.dpi)
        plt.axis('on')
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(fig.canvas.renderer._renderer)
        fig.clf()

def drawLogisticPopulationModel(data):
    r = float(data['r'])
    x1start = float(data['x1start'])
    x2start = float(data['x2start'])
    iter_count = int(data['iter_count'])
    lines = int(data['lines'])
    ChaosModel.drawLogisticPopulationModel(r,x1start,x2start,iter_count,lines)

def ChaosModel_drawFibu(data):
    ChaosModel.drawFibu()

PyBridge.registerHandler("drawLogisticPopulationModel", drawLogisticPopulationModel)
PyBridge.registerHandler("ChaosModel_drawFibu",ChaosModel_drawFibu)