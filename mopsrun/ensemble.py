# ensemble.py: (c) William Menz (wjm34) 2012
# Contains information on a particle ensemble. One run may have many ensembles
# output over a range of times. This object stores lists of particles. Each
# particle is described by a list of parameters. The parameters are stored in
# as an object which has a key and value. The dictionary to these keys is held
# by the ensemble in the form {key : [paramname, unit]}


# Global imports
import mopsparser

# Ensemble class contains information for particles and their properties
class Ensemble:
    def __init__(self, fname):
        # List of particles empty
        self.particles = []
        
        # Lists used to store the headers
        self.head_dict = dict()
        
        # Filename is the ensemble's name
        self.name = fname
        
        # Create a new parser for this PSL
        psl_parser = mopsparser.ParserPSL(fname)
        
        # Set the dictionary for the PSL
        self.head_dict = psl_parser.getParameterDictionary()
        
        # Get the time at which the ensemble was created
        self.time = psl_parser.getPSLTime()
        
        # Add particles from parsed datastream
        parsed_data = psl_parser.getEnsembleData()
        for line in parsed_data:
            self.particles.append(Particle(self.getKeys(), line))
        
        del psl_parser
        
    
    # Gets the keys from the dictionary
    def getKeys(self):
        keys = []
        for i in self.head_dict:
            keys.append(i)
        return keys
    
    # Gets the headers from the dictionary
    def getHeaders(self):
        headers = []
        i = 0
        while i < len(self.getKeys()):
            headers.append(self.head_dict[i])
            i += 1
        return headers
    
    # Returns the list of the instances of the given key's parameter
    def getParameterList(self, key):
        
        newlist = []
        
        for p in self.particles:
            newlist.append(p.getParameter(key))
        
        return newlist

# Particle class holds information about an individual particle
class Particle:
    
    def __init__(self, keys, values):
        self.m_param = []
        
        for k, v in zip(keys, values):
            self.m_param.append(Parameter(k, v))
    
    def printAllParameters(self):
        for p in self.m_param:
            p.printParameter()
    
    def getParameter(self, key):
        value = -1
        for p in self.m_param:
            if key == p.getKey():
                value = p.getValue()
                break
        
        if value < 0:
            print("compass: error, couldn't find {0}.".format(key))
            sys.exit(5)
        else:
            return value


# Parameter class holds information about the average parameter
class Parameter:
    # Default constructor
    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    # Print the data held in parameter
    def printParameter(self):
        print("{0}:\t{1}".format(self.key,self.value))
    
    # Set the value of the parameter
    def setValue(self, value):
        self.value = value
    
    # Return the value of the parameter
    def getValue(self):
        return self.value
    
    # Return the index of the key
    def getKey(self):
        return self.key

# Enum-like class for diameter types
class DiamType:
    col = 1
    pri = 2
    sph = 3
    mob = 4