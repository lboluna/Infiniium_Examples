# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:48:44 2020

@author: luboluna
"""

import visa
import time

VISA_ADDRESS = "TCPIP0::141.121.39.192::hislip0::INSTR"
VISA_TIMEOUT = 240000
VISA_LIBRARY = 'C:\\Program Files (x86)\\IVI Foundation\\VISA\\' \
                          'WinNT\\agvisa\\agbin\\visa32.dll'
FIRMWARE = 6.5

class Infiniium():
    """
    Infiniium Visa Instrument Class
    
    Basic intrument class one can customize. This example is geared towards
    Infiniium intruments. This is a stripped down version of classes I
    normally use. Visa error exceptions have been remove and a number of basic
    measurement setups as well. The intent is for instruction and an example.
    
    You will need to have PyVisa installed. To do so, 
    
    pip install -U pyvisa
    
    
    
    To use:
        
        uxr = Infiniium(VISA_ADDRESS,VISA_LIBRARY)
        
    Calls the __init__ of the class and attaches a VISA resource library to it.
    
    To do a default setup of scope:
        
        uxr.default_setup()
    
    """
    
    def __init__(self, visa_address, visa_library = ''):
        """
        __init__ of Infiniium class
    

        Parameters
        ----------
        visa_address : string
            DESCRIPTION : Visa address in instrument
                          example "TCPIP0::141.121.39.192::hislip0::INSTR"
        visa_library : string, optional
            DESCRIPTION. The default is ''.
                         Visa library being used. USe this if you have other
                         Visa versions installed, to remove any ambiguities
                         example "C:\\Program Files (x86)\\IVI Foundation\\VISA\\' \
                          'WinNT\\agvisa\\agbin\\visa32.dll"

        Returns
        -------
        None.

        """
        self._instID = ''
        try:
            # Create an instance of PyVISA's ResourceManager
            self._rm = visa.ResourceManager(visa_library)
            self._instrument = self._rm.open_resource(visa_address)
            self._instrument.timeout = VISA_TIMEOUT  # Set connection timeout to 20s
            self._instrument.read_termination = '\n'
            self._instrument.write_termination = '\n'
            self._instID = self._instrument.query('*IDN?')
            print('\nInfiniium connection established to:\n' + self._instID)
        except (visa.VisaIOError, visa.InvalidSession):
            print('\nVISA ERROR: Cannot open instrument address.\n')
        except Exception as other:
            print('\nVISA ERROR: Cannot connect to instrument:', other)
        return
    
    def write(self, scpi):
        """
        Basic write method for sending visa based SCPI commands

        Parameters
        ----------
        scpi : string
            DESCRIPTION : SCPI command string.
                          example "*IDN?"

        Returns
        -------
        None.

        """
        self._instrument.write(scpi)
        return
        
    def read(self, scpi):
        """
        Basic read method for sending visa based SCPI commands

        Parameters
        ----------
        scpi : string
            DESCRIPTION : SCPI command string.
                          example "*IDN?"

        Returns
        -------
        read returned value as string

        """
        self._instrument.read(scpi)
        return
    
    def query(self, scpi):
        """
        Basic query method for sending visa based SCPI commands

        Parameters
        ----------
        scpi : string
            DESCRIPTION : SCPI command string.
                          example "*IDN?"
            
            A query is actually a write followed by a read.

        Returns
        -------
        Read return value as string

        """
        self._instrument.query(scpi)
        return
    
    @property
    def model(self):
        """
        Returns
        -------
        TYPE str
            parses a *IDN? and returns the instrument model.

        """
        return self._instID.split(",")[1]
    
    @property
    def hostname(self):
        """
        Returns
        -------
        TYPE str
            parses a *IDN? and returns the hostname if offline.

        """
        return self._instID.split(",")[2]
    
    @property
    def serialnumber(self):
        """
        Returns
        -------
        TYPE str
            parses a *IDN? and returns the instrument serial number.

        """
        return self._instID.split(",")[2]
    
    @property
    def firmware(self):
        """
        Returns
        -------
        TYPE str
            parses a *IDN? and returns the firmware version.

        """
        return self._instID.split(",")[3].strip("\n")
    
    def setVerticalscale(self,vscale= 50):
        self.write(":SYSTem:CONTrol \"Chan1Scale -1 {}\"".format(str(vscale/1000)))
        #self.write(":CHANnel1:DISPlay:SCALe %s" %vscale)
        return

    def setTimescale(self, tscale = 100):
        self.write(":TIMebase:SCALe %s".format(str(tscale*1e-9)))
        return
    
    
    def check_firmware(self, firmware):
        """
        Parameters
        ----------
        firmware : TYPE str
            checks ot see if firmware is newer or older than instrument object
            of dca class
    
        Returns
        -------
        str
        will return either "older" or "newer"
    
        """
        _x = [firmware, self.firmware]
        _x.sort()
        if _x[0] == self.firmware:
            return "newer"
        else: 
            return "older"

    def default_setup(self):
        self.write(":SYSTem:PRESet DEFault")
    
    def opc(self):
        while True:
            _ = self.query("*OPC?")
            if '1' in _:
                break
        return


    
def s2num(string):
    return float(string.strip('\n'))

def get_period(instr, channel= 'CHANnel1', direction = 'RISing'):
    return instr.query(":MEASure:PERiod {}, {}".format(channel, direction))

def main():
    pass

if __name__ == '__main__':
    
    uxr = Infiniium(VISA_ADDRESS,VISA_LIBRARY)
    uxr.default_setup()
    uxr.setTimescale(100) #in ns/div
    uxr.setVerticalscale(50) # in mV/div
    period = get_period(uxr,channel = 'CHANnel1')
    time.sleep(10)
    
    print("Period is {}".format(period))

    
    
    
