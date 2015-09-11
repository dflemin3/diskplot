# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:55:42 2015

@author: dflemin3

Useful plotting functions for working with disks, specifically those of the
circumbinary nature.
"""

import numpy as np
from matplotlib.pylab import *
import matplotlib.pylab as plt

def plot_polar_contour(z, angles, radius, num=30,
                       label='Number Density', cm='rainbow', **kwargs):
    """
    Plot a polar contour plot with 0 degrees at the x axis (y = 0)
    Based on the useful function found in the following link:
    http://blog.rtwilson.com/producing-polar-contour-plots-with-matplotlib/ 
 
    Parameters
    ----------
 
    z : iterable 
        of the values to plot on the contour plot
    angles : array
        angles (in degrees)
    radius : array 
        of radii
    num : int
        number of contours to plot
    label : string
        colorbar label
    cm : string
        name of valid matplotlib colormap
    **kwargs : dict
        dict of arguments accepted by matplotlib
    
    Note: values must be len(angles) x len(radius)
 
    This function also works well with the output of numpy's histogram2d
    as follows:
        x = something in polar coords
        y = something in polar coords
        heatmap, xedges, yedges = np.histogram2d(x,y,bins)
        az = np.linspace(x.min(),x.max(),bins)
        zen = np.linspace(y.min(),y.max(),bins)
        fig, ax, cax = plot_polar_contour(heatmap,az,zen)
  
    Returns
    -------
    fig : matplotlib figure object
        figure to plot, save, etc
    ax : matplotlib axis object
        polar axis where things are plotted
    cax : matplotlib contourf object
        the plot itself
    """
    #Convert from degrees to radians, ensure both are numpy arrays 
    theta = np.array(angles)*np.pi/180.
    radii = np.array(radius)
 
    #Craft array of values to color by
    z = np.array(z)
    z = z.reshape(len(angles), len(radii))
 
    radii, theta = np.meshgrid(radii,theta)
    fig, ax = subplots(subplot_kw=dict(projection='polar'))
    
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    ax.set_rlabel_position(210)
    cax = ax.contourf(theta, radii, z, num ,cmap=cm,**kwargs)
    cb = fig.colorbar(cax)
    cb.set_label(label)
 
    return fig, ax, cax
    
#end function
    
def plot_polar_heatmap(radius, theta, bins=50, label='Number Density',
                       cm='rainbow', **kwargs):
    """
    Plot a polar heatmap (2d histogram in polar coordinates) of the given quantities.
    The supplied quantities, radius and theta, must be able to be represented in polar
    coordinates.
 
    Parameters
    ----------
 
    z : iterable 
        of the values to plot on the contour plot
    angles : array
        angles (in degrees)
    radius : array 
        of radii
    label : string
        colorbar label
    cm : string
        name of valid matplotlib colormap
    **kwargs : dict
        dict of parameters accepted by matplotlib
    
    Note: values must be len(angles) x len(radius)
 
    This function also works super well with the output of numpy's histogram2d
    as follows:
        x = something in polar coords
        y = something in polar coords
        heatmap, xedges, yedges = np.histogram2d(x,y,bins)
        az = np.linspace(x.min(),x.max(),bins)
        zen = np.linspace(y.min(),y.max(),bins)
        fig, ax, cax = plot_polar_contour(heatmap,az,zen)
  
    Returns
    -------
    fig : matplotlib figure object
        figure to plot, save, etc
    ax : matplotlib axis object
        polar axis where things are plotted
    cax : matplotlib contourf object
        the plot itself
    """
    #Map coordinates    
    conv = np.pi/180.    
    x = radius*np.cos(theta*conv)
    y = radius*np.sin(theta*conv)
    
    #Create 2D histogram for heatmap
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)

    #Create mesh that is usable by plot_polar_contour, return figure
    angles = np.linspace(theta.min(),theta.max(),bins)
    radius = np.linspace(radius.min(),radius.max(),bins)
    return plot_polar_contour(heatmap,angles,radius,label=label,cm=cm,**kwargs)
    
#end function