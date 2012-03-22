
# Parent class holding information about CSV outputs
class CSVOutput:
    
    def __init__(self, fname):
        self.delimiter = ","
        self.fname = fname
        
        # Arrays of header and line data for writing
        self.headerdata = []
        self.linedata = []
        
        # Open the file stream
        self.openCSV()
    
    # Opens a CSV and sets the stream object
    def openCSV(self):
        try:
            self.ostream = open(self.fname, 'w')
            print("compass: opened file {0} for output.".format(self.fname))
        except:
            print("compass: couldn't open file {0} for output.".format(self.fname))
    
    # Closes a CSV stream
    def closeCSV(self):
        try:
            self.ostream.close()
            print("compass: closed file {0}.".format(self.fname))
        except:
            print("compass: error trying to close file {0}.".format(self.fname))
    
    # Writes a CSV, provided header and line data is generated.
    def writeCSV(self):
        if (len(self.headerdata) > 0 and len(self.linedata) > 0):
            # Write the headers
            self.writeCSVLine(self.headerdata)
            
            # Now write the lines...
            for line in self.linedata:
                self.writeCSVLine(line)
        else:
            print("compass: no data found for writing!")
            raise
    
    # Writes a CSV line
    def writeCSVLine(self, line):
        i = 0
        outstr = ""
        for l in line:
            outstr += str("{0}".format(l)) 
            if (i != (len(line)-1)): outstr += self.delimiter
            i += 1
        outstr += "\n"
        
        self.ostream.write(outstr)
        

# Class to write PSDs
class CSV_PSD(CSVOutput):
    
    # Sets the psd as a KernelDensity object
    def setPSD(self, kde):
        self.psd = kde
    
    def generateHeaders(self):
        self.headerdata.append("d(nm)")
        self.headerdata.append("psd(1/nm)")
        self.headerdata.append("cum.psd(-)")
    
    # Takes a kernel density object and writes to a CSV
    def generateLines(self):
        for m, p, c in zip(self.psd.mesh, self.psd.psd, self.psd.cumulative_psd):
            self.linedata.append([m, p, c])
            