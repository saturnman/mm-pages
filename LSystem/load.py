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
    def get_Barnsley_lines():
        lines = []
        p = (0.0, 0.0)
        l = 1.0
        for i in range(100000):
            rnd = numpy.random.random()
            if rnd < 0.01:
                t = 0,0.16*p[1]
            elif rnd < 0.86:
                t = 0.85*p[0]+0.04*p[1],-0.04*p[0]+0.85*p[1]+1.6
            elif rnd < 0.93:
                t = 0.2*p[0]-0.26*p[1],0.23*p[0]+0.22*p[1]+1.6
            else:
                t = -0.15*p[0]+0.28*p[1],0.26*p[0]+0.24*p[1]+0.44
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
def draw_Barnsley(ax):
    lines = L_System.get_Barnsley_lines()
    (x, y) = zip(*lines)
    ax.scatter(x,y,marker=',',lw=0, s=1,c='g')
    #ax.axis("equal")
    #ax.set_axis_off()
    #ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
    #ax.invert_yaxis()

def LSystem_draw_Barnsley(data):
    rule = data['rule']
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
    ax = fig.add_subplot(111)
    draw(ax,rules[rule])
    #draw_Barnsley(ax)
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
    #pl.show()
    fig.canvas.draw()
    _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
    fig.clf()

PyBridge.registerHandler("LSystem_draw_Barnsley", LSystem_draw_Barnsley)

