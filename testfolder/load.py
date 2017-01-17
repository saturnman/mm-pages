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

def drawLogisticPopulationModel(data):
    r = float(data['r'])
    x1start = float(data['x1start'])
    x2start = float(data['x2start'])
    iter_count = int(data['iter_count'])
    lines = int(data['lines'])
    ChaosModel.drawLogisticPopulationModel(r,x1start,x2start,iter_count,lines)
PyBridge.registerHandler("drawLogisticPopulationModel", drawLogisticPopulationModel)