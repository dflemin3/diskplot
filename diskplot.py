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
from matplotlib.colors import LogNorm

def plot_polar_contour(z, angles, radius, num=30,
                       label='Number Density', cm='rainbow', **kwargs):
    """
    Plot a polar contour plot with 0 degrees at the x axis (y = 0)
    Based on the useful function found in the following link:
    http://blog.rtwilson.com/producing-polar-contour-plots-with-matplotlib/ 
 
    !!! Currently broken !!! 
 
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
 
    return fig, ax, cax, cb
    
#end function
    
def plot_polar_heatmap(radius, theta, bins=50, label='Number Density',
                       cm='rainbow', **kwargs):
    """
    Plot a polar heatmap (2d histogram in polar coordinates) of the given quantities.
    The supplied quantities, radius and theta, must be able to be represented in polar
    coordinates.
 
    !!! Currently broken: radial direction is weird !!! 
 
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
    assert len(x) == len(y), "x and y must have the same length."    
    
    #Create 2D histogram for heatmap
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)

    #Create mesh that is usable by plot_polar_contour, return figure
    angles = np.linspace(theta.min(),theta.max(),bins)
    radius = np.linspace(radius.min(),radius.max(),bins)
    return plot_polar_contour(heatmap,angles,radius,label=label,cm=cm,**kwargs)
    
#end function
    
def plot_heatmap(x,y,labels=[],bins=50,cm='hot',norm=None,vmin=None,vmax=None,hist_range=None,**kwags):
    """
    Plot a polar heatmap (2d histogram in polar coordinates) of the given quantities.
    The supplied quantities, radius and theta, must be able to be represented in polar
    coordinates.
 
    Parameters
    ----------
    x : array
    y : array
    label : list 
        list of len 3 containing [x label, y label, colorbar label]
    cm : string
        name of valid matplotlib colormap
    norm : string
        whether or not to 'log' colorbar. Default is no log (None)
    **kwargs : dict
        dict of parameters accepted by matplotlib
  
    Returns
    -------
    fig : matplotlib figure object
        figure to plot, save, etc
    ax : matplotlib axis object
        polar axis where things are plotted
    im : matplotlib plot object
        the plot itself
    """
    #Default labels if none or incorrect number suppled
    if labels == [] or len(labels) != 3:
        labels = ['x axis', 'y axis', 'Number']
    
    assert len(x) == len(y), "x and y must have the same length."        
    
    #Create figure, axis for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    #Make 2D histogram of data so it follows Cartesian convention
    #Switch up y and x so that it is plotted as expected
    H, xedges,yedges = np.histogram2d(x,y,bins=bins,range=hist_range)
   
    #Configure colorbar
    #No log, limits given
    if norm == None and vmin != None and vmax != None:
        norm = mpl.colors.Normalize(vmin=vmin,vmax=vmax)
   
    #Log colorbar? limits given?
    if norm == 'log' and vmin!= None and vmax != None:
        norm = LogNorm(vmin=vmin,vmax=vmax) #Can't have < 1 particles in logspace   
    elif norm == 'log': #set default limits
        norm = LogNorm(vmin=H.min(),vmax=H.max()) #Can't have < 1 particles in logspace   

   
    # Plot heatmap ensuring correct plot size
    if hist_range != None:
        x_min = hist_range[0][0]
        x_max = hist_range[0][1]
        y_min = hist_range[1][0]
        y_max = hist_range[1][1]
    else:
        x_min = x.min()
        x_max = x.max()
        y_min = y.min()
        y_max = y.max()
   
    extent = [x_min,x_max,y_min,y_max]   
    aspectratio = 1
    im = ax.imshow(H.T, extent=extent, cmap=cm,norm=norm,
                    interpolation='nearest', origin='lower', aspect=aspectratio,
                    **kwags)
    ax.set_aspect(np.fabs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspectratio)
                    
    #Format colorbar
    cb = fig.colorbar(im)
    cb.set_label(labels[2],rotation=270,labelpad=30)
    
    #Format axes
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_xlim(x.min(),x.max())
    ax.set_ylim(y.min(),y.max())    
 
    return fig, ax, im, cb
  
#end function