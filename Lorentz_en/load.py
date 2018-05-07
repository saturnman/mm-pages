# -*- coding: utf-8 -*-
from math import sin, cos, pi
import matplotlib
matplotlib.use("agg")
import _pybridge
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import collections
import numpy as np
class Lorentz_System(object):
    instance = None

    @staticmethod
    def _setup(data):
        Lorentz_System.instance = Lorentz_System()

    @staticmethod
    def _draw(data):
        Lorentz_System.instance.draw()

    @staticmethod
    def _step(data):
        #print Lorentz_System.instance
        Lorentz_System.instance.step()

    @staticmethod
    def setParams(data):
        print data
        rho = float(data['rho'])
        sigma = float(data['sigma'])
        beta = float(data['beta'])
        Lorentz_System.instance = Lorentz_System()
        Lorentz_System.instance.rho = rho
        Lorentz_System.instance.sigma = sigma
        Lorentz_System.beta = beta


    def __init__(self):
        N_trajectories = 20
        self.rho = 28.0
        self.beta = 8.0/3
        self.sigma = 10.0

        self.N_trajectories = N_trajectories
        # Choose random starting points, uniformly distributed from -15 to 15
        np.random.seed(1)
        x0 = -15 + 30 * np.random.random((N_trajectories, 3))

        # Solve for the trajectories
        t = np.linspace(0, 4, 1500-1)
        dt = (4-0.0)/1000
        self.x_t = [[x0_t0] for x0_t0 in x0]
        for trajectory_index in range(N_trajectories):
            for _ in t:
                prev_x_t = self.x_t[trajectory_index][-1]
                self.x_t[trajectory_index].append(prev_x_t+Lorentz_System.lorentz_deriv_dt((prev_x_t[0],prev_x_t[1],prev_x_t[2]),dt,self.sigma,self.beta,self.rho))
        self.x_t = np.asarray(self.x_t)
        #self.x_t = np.asarray([integrate.odeint(Lorentz_System.lorentz_deriv, x0i, t)
        #                  for x0i in x0])

        # model run step
        self.steps = 1
        self.draw()

    def step(self):
        self.steps += 2
        self.steps %= (self.steps + 2) % self.x_t.shape[1]

    def draw(self):
        # Set up figure & 3D axis for animation
        self.fig = plt.gcf()
        self.fig.patch.set_facecolor("w")
        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(1200.0 / float(DPI), 1200.0 / float(DPI))

        self.ax = self.fig.add_axes([0, 0, 1, 1], projection='3d')
        self.ax.axis('off')
        self.ax.axis("equal")
        self.ax.set_axis_off()
        # choose a different color for each trajectory
        self.colors = plt.cm.jet(np.linspace(0, 1, self.N_trajectories))

        # set up lines and points
        self.lines = sum([self.ax.plot([], [], [], '-', c=c)
                          for c in self.colors], [])
        self.pts = sum([self.ax.plot([], [], [], 'o', c=c)
                        for c in self.colors], [])

        # prepare the axes limits
        self.ax.set_xlim((-30, 30))
        self.ax.set_ylim((-35, 35))
        self.ax.set_zlim((0, 60))

        # set point-of-view: specified by (altitude degrees, azimuth degrees)
        self.ax.view_init(30, 0.3 * self.steps)
        for line, pt, xi in zip(self.lines, self.pts, self.x_t):
            x, y, z = xi[:self.steps].T
            line.set_data(x, y)
            line.set_3d_properties(z)

            pt.set_data(x[-1:], y[-1:])
            pt.set_3d_properties(z[-1:])

        self.fig.canvas.draw()
        _pybridge.PyRendererAggBufferRGBA(self.fig.canvas.get_renderer()._renderer)
        self.fig.clf()

    @staticmethod
    def lorentz_deriv_dt((x, y, z), dt, sigma=10., beta=8. / 3, rho=28.0):
        """Compute the time-derivative of a Lorentz system."""
        return [sigma * (y - x)*dt, (x * (rho - z) - y)*dt, (x * y - beta * z)*dt]
    @staticmethod
    def lorentz_deriv((x, y, z), t0, sigma=10., beta=8. / 3, rho=28.0):
        """Compute the time-derivative of a Lorentz system."""
        return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


def Lorentz_System_draw(data):
    Lorentz_System._draw(data)

def Lorentz_System_setup(data):
    Lorentz_System._setup(data)

def Lorentz_System_step(data):
    Lorentz_System._step(data)

def Lorentz_System_setParams(data):
    Lorentz_System.setParams(data)

PyBridge.registerHandler("Lorentz_System_draw", Lorentz_System_draw)
PyBridge.registerHandler("Lorentz_System_setup", Lorentz_System_setup)
PyBridge.registerHandler("Lorentz_System_step", Lorentz_System_step)
PyBridge.registerHandler("Lorentz_System_setParams",Lorentz_System_setParams)
