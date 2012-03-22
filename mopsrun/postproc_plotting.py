# postproc_plotting.py: (c) William Menz (wjm34) 2012

# Global imports
import matplotlib.pyplot as plt
import math

class Plotting:
    def __init__(self):
        
        # The terminal defines to which format the graphs are written.
        self.terminal = "png"
    
    # Given an ID 'i', return a particular line style.
    def getLineStyles(self, i):
        
        styles = ['-', '--', '-.', ':']
        return styles[i % len(styles)]
    
    # Plots the PSDs given as a list of diameters and ranges
    # Expects the form diameters = [[d1], [d2]] where d1, d2 are lists
    # Doesn't take ensemble objects directly as this allows easier comparison
    # with PSDs of other type
    def plotPSDs(self, diameters, ranges, names):
        
        if len(diameters) != len(ranges):
            print("compass: bad PSD input")
            raise
        
        
        # Use maxima and minima for autoscaling
        maxima_r = []     # list of range maxima
        minima_r = []
        maxima_d = []     # list of mesh maxima
        minima_d = []
        
        # List holding lines
        lines = []
        
        i = 0
        # Plot the curves!
        for d, r, n in zip(diameters, ranges, names):
            lines.append(plt.plot(d, r, self.getLineStyles(i), linewidth=2.0, label=n))
            i += 1
            # Collect some useful data...
            maxima_r.append(max(r))
            minima_r.append(min(r))
            maxima_d.append(max(d))
            minima_d.append(min(d))
        
        # Set up the titles, etc
        plt.xlabel("diameter, nm")
        plt.ylabel("kernel density, 1/nm")
        
        # Auto-on for logscale x
        if self.autoLogScale(maxima_d):
            plt.axes().set_xscale('log')
        # Auto-on for logscale y
        if self.autoLogScale(maxima_r):
            plt.axes().set_yscale('log')
            if min(minima_r) < 1.0e-6:
                plt.ylim(1.0e-6)
        
        plt.legend()
        
        plt.show()
    
    # Takes a list of maxima of series and automatically activates logscale
    # based on an empirical rule
    def autoLogScale(self, maxlist):
        
        if len(maxlist) < 2:
            return False
        else:
            ratios = []
            i = 1
            while i < len(maxlist):
                if maxlist[i-1] == 0.0:
                    ratio = 1.0
                else:
                    ratio = maxlist[i]/maxlist[i-1]
                if ratio < 1:
                    ratio = 1/ratio
                ratios.append(math.log10(ratio))
                i += 1
            
            for r in ratios:
                if r > 1.5:
                    return True
                else:
                    return False
    
    # Plots trajectories in the format [[t1], [t2]..] as for plotPSD
    def plotTrajectoryCIs(self, times, values, names, units):
        
        # List holding lines
        lines = []
        
        if not self.checkUnits(units):
            print("compass: poor units specified for {0}".format)
        self.checkNumSeries(names)
        
        # Plot the curves!
        i = 0
        for t, v, n in zip(times, values, names):
            lines.append(plt.plot(t, v, self.getLineStyles(i), linewidth=2.0, label=n))
            i += 1
        
        plt.legend(loc=0)
        
        plt.axes().set_yscale('log')
        plt.ylabel(units[0])
        plt.axes().set_xscale('log')
        plt.xlabel("time, s")
        
        plt.show()
        
    # Checks if there are too many series
    def checkNumSeries(self, names):
        if len(names) > 7:
            print("compass: too many series!")
            
    
    # Takes a list of trajectory names, checks for identical units    
    def checkUnits(self, units):
        i = 1
        while i < len(units):
            if units[i] != units[i-1]:
                print("compass: poor units specified: {0} vs {1}.".format(units[i-1], units[i]))
                return False
            else:
                return True
            i += 1

