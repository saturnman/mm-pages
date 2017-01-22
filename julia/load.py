# -*- coding: utf-8 -*-
import numpy as nm
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import _pybridge
from matplotlib import collections

class Julia:
    z = []
    fractal = []
    c = []
    SIZE = 1000
    MAX_COLOR = 255.
    ITERATIONS = 10
    totalIter = 10
    @staticmethod
    def setup(x_min,x_max,y_min,y_max,c):
        x, y = nm.meshgrid(nm.linspace(x_min, x_max, 2 * Julia.SIZE), nm.linspace(y_min, y_max, Julia.SIZE));
        Julia.c = x + 1j * y
        #Julia.c = c[0]+1j*c[1]
        Julia.z = Julia.c.copy()
        Julia.fractal = nm.zeros(Julia.z.shape, dtype=nm.uint8) + Julia.MAX_COLOR
        Julia.CPoint = c[0]+1j*c[1]
    @staticmethod
    def draw():
        fig = plt.gcf()
        #SIZE = lena.shape[0]
        #注意:此参数会极大影响计算过程的内存消耗，对于小内存机器可以会让计算进程因内存不够而出错，请自行调节计算

        #x_min, x_max = -2.5, 1
        #y_min, y_max = -1.2, 1.2
        #x,y = nm.meshgrid(nm.linspace(x_min,x_max,2*Julia.SIZE),nm.linspace(y_min,y_max,Julia.SIZE));
        #c = x + 1j*y
        #z = c.copy()
        #fractal = nm.zeros(z.shape,dtype=nm.uint8)+Julia.MAX_COLOR
        #for n in range(Julia.ITERATIONS):
        #    mask = nm.abs(z) <=10
        #    z[mask] = z[mask]**2+c[mask]
        #    fractal[(fractal==Julia.MAX_COLOR) & (~mask)] = (Julia.MAX_COLOR-1)*n/ITERATIONS
        # Display the fractal
        DPI = fig.get_dpi()
        fig.set_size_inches(1500.0 / float(DPI), 800.0 / float(DPI))
        #print Julia.fractal
        im = plt.imshow(Julia.fractal,cmap=plt.get_cmap('flag'))
        #plt.title('Mandelbrot')
        plt.axis('off')
        im.figure.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(im.figure.canvas.get_renderer()._renderer)
        fig.clf()
    @staticmethod
    def improve():
        if Julia.CPoint != 0+1j*0:
            for n in range(Julia.ITERATIONS):
                mask = nm.abs(Julia.z) <= 20
                Julia.z[mask] = Julia.z[mask]**2+Julia.CPoint
                Julia.fractal[(Julia.fractal==Julia.MAX_COLOR) & (~mask)] = (Julia.MAX_COLOR-1)*(Julia.totalIter-Julia.ITERATIONS+n)/(Julia.totalIter)
        else:
            for n in range(Julia.ITERATIONS):
                mask = nm.abs(Julia.z) <= 20
                Julia.z[mask] = Julia.z[mask] ** 2 + Julia.c[mask]
                Julia.fractal[(Julia.fractal == Julia.MAX_COLOR) & (~mask)] = (Julia.MAX_COLOR - 1) * (
                Julia.totalIter - Julia.ITERATIONS + n) / (Julia.totalIter)
        Julia.totalIter += Julia.ITERATIONS
def Julia_draw(data):
    print data
    Julia.draw()

def Julia_improve(data):
    print data
    Julia.improve()

def Julia_setup(data):
    print data
    x_min = data['x_min']
    x_max = data['x_max']
    y_min = data['y_min']
    y_max = data['y_max']
    c = data['c']
    Julia.setup(x_min,x_max,y_min,y_max,c)

PyBridge.registerHandler("Julia_draw", Julia_draw)
PyBridge.registerHandler("Julia_improve",Julia_improve)
PyBridge.registerHandler("Julia_setup",Julia_setup)
