# -*- coding: utf-8 -*-
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import _pybridge
from matplotlib import collections

class BouncingBall:
    posStart = 50
    pos = 50
    g = -9.8
    v = 0.0
    dt = 0.01
    t = 0.0
    timeList = []
    posList = []
    vList = []
    posLimit = 1e-3
    vlimit = 1e-3
    bounceEff = -0.99
    drawParam = 'x'
    @staticmethod
    def setup():
        BouncingBall.posStart = 50
        BouncingBall.pos = 50
        BouncingBall.g = -9.8
        BouncingBall.v = 0.0
        BouncingBall.dt = 0.01
        BouncingBall.t = 0.0
        BouncingBall.timeList = []
        BouncingBall.posList = []
        BouncingBall.vList = []
        BouncingBall.posLimit = 1e-8
        BouncingBall.vlimit = 1e-8
    @staticmethod
    def step():
        if nm.math.fabs(BouncingBall.v) < BouncingBall.vlimit and nm.math.fabs(BouncingBall.pos) < BouncingBall.posLimit:
            return
        BouncingBall.pos = BouncingBall.pos+ BouncingBall.v*BouncingBall.dt+0.5*BouncingBall.g*(BouncingBall.dt**2)
        BouncingBall.v = BouncingBall.v + BouncingBall.g*BouncingBall.dt
        BouncingBall.t += BouncingBall.dt
        BouncingBall.timeList.append(BouncingBall.t)
        BouncingBall.posList.append(BouncingBall.pos)
        BouncingBall.vList.append(BouncingBall.v)
        if BouncingBall.pos<0:
            BouncingBall.v = BouncingBall.bounceEff*BouncingBall.v
            BouncingBall.pos = -BouncingBall.pos
    @staticmethod
    def draw():
        fig = plt.gcf()
        fig.clf()
        fig.patch.set_facecolor("w")
        DPI = fig.get_dpi()
        fig.set_size_inches(700.0/float(DPI),600.0/float(DPI))
        plt.axis('off')
        ax = fig.add_subplot(121)
        ax.scatter(100,BouncingBall.pos+3,s=700,c='#0000ff',alpha=0.8)
        ax2 = fig.add_subplot(122)

        if BouncingBall.drawParam=='x':
            ax2.set_ylim(-10, 70)
            ax2.plot(BouncingBall.timeList,BouncingBall.posList)
            ax2.set_xlabel("t(s)")
            ax2.set_ylabel("pos(m)")
        else:
            ax2.plot(BouncingBall.timeList, BouncingBall.vList)
            ax2.set_xlabel("t(s)")
            ax2.set_ylabel("v(m/s)")
            ax2.set_xlim(ax2.dataLim.xmin, ax2.dataLim.xmax)
        ax.axis("equal")
        #ax.set_axis_off()
        ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
        ax.set_ylim(0,80)
        #ax.invert_yaxis()
        fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(fig.canvas.get_renderer()._renderer)
        fig.clf()

    @staticmethod
    def setb(b):
        BouncingBall.bounceEff = b

    @staticmethod
    def setDrawParam(drawParam):
        BouncingBall.drawParam = drawParam

def BouncingBall_draw(data):
    BouncingBall.draw()

def BouncingBall_step(data):
    for i in range(10):
        BouncingBall.step()

def BouncingBall_setb(data):
    b = data['b']
    BouncingBall.setb(b)

def BouncingBall_setDrawParam(data):
    drawParam = data['drawParam']
    BouncingBall.setDrawParam(drawParam)

def BouncingBall_setup(data):
    BouncingBall.setup()

PyBridge.registerHandler("BouncingBall_draw", BouncingBall_draw)
PyBridge.registerHandler("BouncingBall_step", BouncingBall_step)
PyBridge.registerHandler("BouncingBall_setb", BouncingBall_setb)
PyBridge.registerHandler("BouncingBall_setDrawParam",BouncingBall_setDrawParam)
PyBridge.registerHandler("BouncingBall_setup",BouncingBall_setup)
