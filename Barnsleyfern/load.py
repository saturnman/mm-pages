# -*- coding: utf-8 -*-
from math import sin, cos, pi
import matplotlib
matplotlib.use("agg")
import _pybridge
import matplotlib.pyplot as pl
from matplotlib import collections
import numpy
class L_System(object):
    def __init__(self, rule):
        info = rule['S']
        for i in range(rule['iter']):
            ninfo = []
            for c in info:
                if c in rule:
                    ninfo.append(rule[c])
                else:
                    ninfo.append(c)
            info = "".join(ninfo)
        self.rule = rule
        self.info = info
    def get_lines(self):
        d = self.rule['direct']
        a = self.rule['angle']
        p = (0.0, 0.0)
        l = 1.0
        lines = []
        stack = []
        for c in self.info:
            if c in "Ff":
                r = d * pi / 180
                t = p[0] + l*cos(r), p[1] + l*sin(r)
                lines.append(((p[0], p[1]), (t[0], t[1])))
                p = t
            elif c == "+":
                d += a
            elif c == "-":
                d -= a
            elif c == "[":
                stack.append((p,d))
            elif c == "]":
                p, d = stack[-1]
                del stack[-1]
        return lines
    @staticmethod
    def get_Barnsley_lines(paramsMatrix):
        lines = []
        p = (0.0, 0.0)
        l = 1.0
        for i in range(100000):
            rnd = numpy.random.random()
            if rnd < paramsMatrix[0,6]:
                t = paramsMatrix[0,0]*p[0]+paramsMatrix[0,1]*p[1]+paramsMatrix[0,4],paramsMatrix[0,2]*p[0]+paramsMatrix[0,3]*p[1]+paramsMatrix[0,5]
            elif rnd < paramsMatrix[0,6]+paramsMatrix[1,6]:
                t = paramsMatrix[1,0]*p[0]+paramsMatrix[1,1]*p[1]+paramsMatrix[1,4],paramsMatrix[1,2]*p[0]+paramsMatrix[1,3]*p[1]+paramsMatrix[1,5]
            elif rnd < paramsMatrix[0,6]+paramsMatrix[1,6]+paramsMatrix[2,6]:
                t = paramsMatrix[2,0]*p[0]+paramsMatrix[2,1]*p[1]+paramsMatrix[2,4],paramsMatrix[2,2]*p[0]+paramsMatrix[2,3]*p[1]+paramsMatrix[2,5]
            else:
                t = paramsMatrix[3,0]*p[0]+paramsMatrix[3,1]*p[1]+paramsMatrix[3,4],paramsMatrix[3,2]*p[0]+paramsMatrix[3,3]*p[1]+paramsMatrix[3,5]
            lines.append((t[0], t[1]))
            p = t
        return lines
rules = [
    {
        "F":"F+F--F+F", "S":"F",
        "direct":180,
        "angle":60,
        "iter":6,
        "title":"Koch"
    },
    {
        "X":"X+YF+", "Y":"-FX-Y", "S":"FX",
        "direct":0,
        "angle":90,
        "iter":13,
        "title":"Dragon"
    },
    {
        "f":"F-f-F", "F":"f+F+f", "S":"f",
        "direct":0,
        "angle":60,
        "iter":7,
        "title":"Triangle"
    },
    {
        "X":"F-[[X]+X]+F[+FX]-X", "F":"FF", "S":"X",
        "direct":-45,
        "angle":25,
        "iter":6,
        "title":"Plant"
    },
    {
        "S":"X", "X":"-YF+XFX+FY-", "Y":"+XF-YFY-FX+",
        "direct":0,
        "angle":90,
        "iter":6,
        "title":"Hilbert"
    },
    {
        "S":"L--F--L--F", "L":"+R-F-R+", "R":"-L+F+L-",
        "direct":0,
        "angle":45,
        "iter":10,
        "title":"Sierpinski"
    },
]
def draw(ax, rule, iter=None):
    if iter!=None:
        rule["iter"] = iter
    lines = L_System(rule).get_lines()
    linecollections = collections.LineCollection(lines)
    ax.add_collection(linecollections, autolim=True)
    ax.axis("equal")
    ax.set_axis_off()
    ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
    ax.invert_yaxis()
def draw_Barnsley(ax,paramsMatrix):
    lines = L_System.get_Barnsley_lines(paramsMatrix)
    (x, y) = zip(*lines)
    ax.scatter(x,y,marker=',',lw=0, s=1,c='g')
    #ax.axis("equal")
    #ax.set_axis_off()
    #ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
    #ax.invert_yaxis()

def LSystem_draw_Barnsley(data):
    params = data['params']
    paramsMatrix = numpy.asarray(params)
    slim = data['slim']

    print paramsMatrix.shape
    print paramsMatrix
    fig = pl.gcf()
    fig.patch.set_facecolor("w")
    DPI = fig.get_dpi()
    if slim:
        fig.set_size_inches(300.0 / float(DPI), 600.0 / float(DPI))
    else:
        fig.set_size_inches(1000.0/float(DPI),600.0/float(DPI))

    #for i in xrange(6):
    #    ax = fig.add_subplot(241+i)
    #    draw(ax, rules[i])
    #ax = fig.add_subplot(247)
    #draw_Barnsley(ax)
    #fig.add_subplot(247)
    pl.axis('off')
    ax = fig.add_subplot(111)
    #draw(ax,rules[rule])
    draw_Barnsley(ax,paramsMatrix)
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
    #pl.show()
    fig.canvas.draw()
    _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
    fig.clf()

PyBridge.registerHandler("LSystem_draw_Barnsley", LSystem_draw_Barnsley)

