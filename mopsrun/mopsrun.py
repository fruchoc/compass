# mopsrun.py: (c) William Menz (wjm34) 2012

# Global imports
import ensemble
import trajectory
import postproc_particles

# Class which contains all information pertaining to a particular MOPS output run
class MopsRun:
    # Default constructor
    def __init__(self):
        
        # Stores the information of all ensembles
        self.ensembles = []
        
        # Contains information of process rates
        self.allrates = 0
        
        # Temporal evolution of particle properties
        self.allpartproperties = 0
        
        # Gas-phase rates
        self.allgasphase = 0
       
        # Switches to indicate what data are present
        self.hasPsl = False
        self.hasPart = False
        self.hasChem = False
        self.hasRates = False
        
        # Filenames for the run
        self.listPsl = []
        self.listPart = []
        self.listChem = []
        self.listRates = []
    
    # Search the current path for a MOPS output run
    #   look for -psl, -part, -chem
    def findMopsRun(self):
        # Get lists of potential files in directory
        list_psl = self.findFiles("*-psl*.csv")
        list_part = self.findFiles("*-part.csv")
        list_rates = self.findFiles("*-part-rates.csv")
        list_chem = self.findFiles("*-chem.csv")
        
        # Now inform the object of which data are present
        self.hasPsl = self.checkFiles(list_psl) 
        if self.hasPsl:
            self.listPsl = list_psl
        self.hasPart = self.checkFiles(list_part) 
        if self.hasPart:
            self.listPart = list_part
        self.hasRates = self.checkFiles(list_rates) 
        if self.hasRates:
            self.listRates = list_rates
        self.hasChem = self.checkFiles(list_chem) 
        if self.hasChem:
            self.listChem = list_chem

    # Helper function to search for searchtext, and return lists of files
    def findFiles(self, searchtext):
        # Need for filename matching
        import glob
        
        filelist = glob.glob(searchtext)
        if len(filelist) == 0:
            return []
        else:
            return filelist
    
    # Helper function to inform the object of which data are present
    def checkFiles(self, searchresults):
        if (len(searchresults) < 1):
            return False
        else:
            return True
    
    # Helper function to identify whether there is enough information to proceed with calculation
    def enoughInfo(self):
        if (self.hasPsl and self.hasPart and self.hasRates and self.hasChem == False):
            return False
        else:
            return True
    
    # Load the CSV files into the MopsRun object
    def initialise(self):
        
        # One MopsRun can have multiple PSLs. Loop over these.
        if self.hasPsl:
            for fname in self.listPsl:
                newensemble = ensemble.Ensemble(fname)
                self.ensembles.append(newensemble)
        
        # Now load the particle properties (-part.csv) file
        if self.hasPart:
            for fname in self.listPart:
                self.allpartproperties = trajectory.ParticleStats(fname)
        
        # Import the rates
        if self.hasRates:
            for fname in self.listRates:
                self.allrates = trajectory.Rates(fname)
        
        # ..and get the chemistry
        if self.hasChem:
            for fname in self.listChem:
                self.allgasphase = trajectory.ChemProfile(fname)
        
        # Create a PSD
        en1 = self.ensembles[0]
        diam = en1.getParameterList(3)
        wt   = en1.getParameterList(0)
        
        stats = postproc_particles.KernelDensity(diam, wt)
        stats.getCumulativePSD()
        stats.printPSDStats()
