import os
import datetime

class logfile():
    def __init__(self, filename, ext='txt'):
        self.filename_new = ''.join( [str(filename), '_', datetime.datetime.now().strftime("%Y.%m.%d-%Hh%Mm%Ss"), '.', ext] )
        self.fname = open( self.filename_new, 'wb+' )

    def newline(self, linetxt):
        self.fname.write( linetxt + os.linesep )

    def line(self, linetxt):
        self.fname.write( linetxt )

    def close(self):
        self.fname.close()

    def flush(self):
        self.fname.flush()

    def getname(self):
        return self.filename_new
