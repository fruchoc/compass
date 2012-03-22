# mopsrun.py: (c) William Menz (wjm34) 2012

# Global imports
import ensemble
import trajectory
import postproc_particles
import postproc_plotting
import re


# Enum-like class for diameter types
class DiamType:
    def __init__(self, en_headers, trj_headers):
        # Default values
        self.psl_dcol = 2
        self.psl_dmob = 3
        self.psl_dsph = 1
        self.psl_dpri = 13
        
        self.trj_dcol = 3
        self.trj_dmob = 4
        self.trj_dsph = 2
        self.trj_dpri = 22
        
        # Double check headers to ensure proper values are found.
        i = 0
        while i < len(en_headers):
            if re.search("Collision Diameter", en_headers[i][0]): self.psl_dcol = i
            if re.search("Mobility Diameter", en_headers[i][0]): self.psl_dmob = i
            if re.search("Sphere Diameter", en_headers[i][0]): self.psl_dsph = i
            if re.search("Primary Diameter", en_headers[i][0]): self.psl_dpri = i
            i += 1
            
        i = 0
        while i < len(trj_headers):
            if re.search("Collision Diameter", trj_headers[i][0]): self.trj_dcol = i
            if re.search("Mobility Diameter", trj_headers[i][0]): self.trj_dmob = i
            if re.search("Sphere Diameter", trj_headers[i][0]): self.trj_dsph = i
            if (re.search("Diameter", trj_headers[i][0]) and re.search("Primary", trj_headers[i][0])): self.trj_dpri = i
            i += 1


# Class which contains all information pertaining to a particular MOPS output run
class MopsRun:
    # Default constructor
    def __init__(self):
        
        # Stores the information of all ensembles
        self.ensembles = []
        
        # Contains information of process rates
        self.allrates = []
        
        # Temporal evolution of particle properties
        self.allpartproperties = []
        
        # Gas-phase rates
        self.allgasphase = []
       
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
        if (self.hasChem or self.hasPart or self.hasPsl or self.hasRates):
            return True
        else:
            return False

    
    # Load the CSV files into the MopsRun object
    def initialise(self):
        
        # One MopsRun can have multiple PSLs. Loop over these.
        if self.hasPsl:
            for fname in self.listPsl:
                newensemble = ensemble.Ensemble(fname)
                if newensemble.checkIfParticles():
                    self.ensembles.append(newensemble)
                else:
                    print("compass: no particles found in file {0}.".format(fname))
                    del newensemble
        
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
        
        # Allocate diameter types
        if len(self.ensembles) >= 1:
            self.diamtypes = DiamType(self.ensembles[0].getHeaders(), self.allpartproperties.trajectory_names)
        
        # Now let's do some plotting
        self.plotAllPSDs()
        #self.plotAllRatesCI()
        self.plotAllChem()
    
    
    # Plots a PSD for every ensemble
    def plotAllPSDs(self):
        psdplot = postproc_plotting.Plotting()
        
        # Check there are ensembles to plot!
        if len(self.ensembles) >= 1:
            # GET THE PSD PLOTS
            stats = []
            names = []
            for en in self.ensembles:
                stats.append(postproc_particles.KernelDensity(en.getParameterList(self.diamtypes.psl_dpri), en.getParameterList(0)))
                names.append(en.name)
            
            meshes = []
            frequencies = []
            for s in stats:
                psd = s.returnPSD()
                meshes.append(psd[0])
                frequencies.append(psd[1])
                
            psdplot.plotPSDs(meshes, frequencies, names)
            
        else:
            print("compass: no ensembles found to plot.")
        
    
    # Plots the CIs for all rates
    def plotAllRatesCI(self):
        
        # GET THE RATES PLOT
        ratesplot = postproc_plotting.Plotting()
        
        times = []
        values = []
        rnames = []
        runits = []
        for rate in self.allrates.trajectories:
            times.append(rate.getTimes())
            values.append(rate.getValues())
            rnames.append(rate.getName())
            runits.append(rate.getUnit())
        
        ratesplot.plotTrajectoryCIs(times, values, rnames, runits)
    
        # Plots the CIs for all rates
    def plotAllChem(self):
        
        # GET THE RATES PLOT
        chemplot = postproc_plotting.Plotting()
        
        times = []
        values = []
        cnames = []
        cunits = []
        for chem in self.allgasphase.trajectories:
            times.append(chem.getTimes())
            values.append(chem.getValues())
            cnames.append(chem.getName())
            cunits.append(chem.getUnit())
        
        chemplot.plotTrajectoryCIs(times, values, cnames, cunits)
