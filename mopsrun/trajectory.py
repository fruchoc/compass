# trajectory.py: (c) William Menz (wjm34) 2012
# The trajectory class holds information about the temporal evolution
# of a given functional. This is the data format for -part.csv, -chem.csv
# and other similar output files.

# Global imports
import mopsparser

# Describes a temporal evolution trajectory
class Trajectory:
    # Default constructor
    def __init__(self, name, times, values, errors):
        self.name = name       # Name of the parameter [parametername, unit]
        self.times = times     # List describing the output timesteps
        self.values = values   # List describing the value at time
        self.errors = errors   # List describing the errors of those values
        
        # Determine the CI vectors
        self.getConfIntervals()
    
    def getName(self):
        return self.name[0]
    
    def getUnit(self):
        return self.name[1]
    
    # Generates the upper and lower confidence intervals
    def getConfIntervals(self):
        self.lower_ci = []
        self.upper_ci = []
        
        # Loop over the values and errors, set lower limit at zero
        for v, e in zip(self.values, self.errors):
            self.lower_ci.append(max(v - e, 0.0))
            self.upper_ci.append(v + e)
    
    # Print a trajectory to console
    def printTrajectory(self):
        for t, v, e in zip(self.times, self.values, self.errors):
            print("{0:.3e}\t{1:.3e}\t{2:.3e}".format(t, v, e))
    
    # Return the times vector
    def getTimes(self):
        return self.times
    
    # Return the values vector of a trajectory
    def getValues(self):
        return self.values
    
    # Return the upper CI
    def getUpperCI(self):
        return self.upper_ci
    
    # Return the lower CI
    def getLowerCI(self):
        return self.lower_ci
    
    # Return the errors vector
    def getError(self):
        return self.errors

# Dummy class which describes a type of trajectory file, e.g. a -part.csv
class TrajectoryContainer:
    # Default constructor
    def __init__(self, fname):
        # Filename is trajectory's name
        self.name = fname
        
        # List of trajectories is empty
        self.trajectories = []
        
        # List of trajectory names is empty
        self.trajectory_names = []
        
        # Create a new parser for the rates
        parser = mopsparser.ParserTrajectory(self.name)
        
        # Read the headers
        self.trajectory_names = parser.getTrajectoryNames()
        
        # Load the trajectory data and sort it
        self.trajectories = parser.getAllTrajectories(self.trajectory_names)
        
        # Done with parser now
        del parser
        
        self.initialise()
    
    # Don't initialise the generic object
    def initialise(self):
        # Further initialisations for other classes
        print("compass: trajectory initialised.")
    
    # Add a trajectory to the list
    def addTrajectory(self, new_trajectory):
        self.trajectories.append(new_trajectory)
    
    

# Derived class to hold the information on all rates
class Rates(TrajectoryContainer):
    
    # Dummy function
    def dummy(self):
        print "test"

# Derived class to hold the information on all particle stats
class ParticleStats(TrajectoryContainer):
    
    # Dummy function
    def dummy(self):
        print "test"

# Derived class to hold the information on all chemical species
class ChemProfile(TrajectoryContainer):
    
    # Chem-specific initialisations
    def initialise(self):
        
        # Separate out the T,P,rho
        self.splitMixtureProperties()
        
    
    # By default, T, P and rho are loaded as chemical species. Split them!
    def splitMixtureProperties(self):
        
        # Get the indices of trajectories.
        i = 0
        i_t = -1
        i_r = -1
        i_p = -1
        for name in self.trajectory_names:
            if (name[0] == 'T'): i_t = i
            if (name[0] == 'Density'): i_r = i
            if (name[0] == 'Pressure'): i_p = i
            i += 1
        
        if (i_t < 0 or i_r < 0 or i_p < 0):
            print("compass: couldn't find indices for T/rho/P!")
        else:
            self.pressure_profile = self.trajectories.pop(i_p)
            self.density_profile = self.trajectories.pop(i_r)
            self.temp_profile = self.trajectories.pop(i_t)
            
            self.trajectory_names.pop(i_p)
            self.trajectory_names.pop(i_r)
            self.trajectory_names.pop(i_t)
