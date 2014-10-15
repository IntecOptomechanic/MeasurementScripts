import numpy as np
import pylab as plt
from numpy import *
from intec.pymeasure.instruments import *
from pymeasure.units.unit import *
from pymeasure.instruments.instrument import VisaInstrument2
from pymeasure.units.unit import NANOMETER, DBM, GIGAHERTZ, SECOND
from time import localtime, strftime
import datetime


def test1():
    timestamp=strftime("h%Hm%Ms%S-%d%b%Y", localtime())

    ESA = VisaInstrument2(name='', address='GPIB0::18')
    ESA.timeout = 300*SECOND 
    
    span =  .001  # ESA span in GHz
    center = 5.32 # ESA center frequency in GHz
    avg = 1       # ESA video averaging

    filename = 'Filename_'+timestamp
    # Old HP ESA (to 22 GHz)
    
    # Set status
    ESA.write("CENTERWL "+str(center)+"GHz;")   # Set center frequency, in GHz
    ESA.write("SPANWL "+str(span)+"GHz;")       # Set span, in GHz 
    ESA.write("VB 3 Hz;")                       # Set Video Bandwidth
    ESA.write("RB 3 Hz;")                       # Set Resolution Bandwidth
    ESA.write("SNGLS;")                         # Set to single sweep mode
    ESA.write("VAVG "+str(avg)+";")             # Turn on video averaging
    
    # Read Status    
    center=float(ESA.ask("CENTERWL?;"))         # Get center frequency
    span=float(ESA.ask("SPANWL?;"))             # Get span
    OptPowerESA=ESA.ask("OPTPWR?")              # Get Optical Power
    ResolutionBW=ESA.ask("RB?")                 # Get Resolution Bandwidth
    VideoBW=ESA.ask("VB?")                      # Get Video Bandwidth
    SweepTime=ESA.ask("ST?")                    # Get Sweep Time
    
    ESA.write("TS;")                            # Sweep trace A
    ESA_spectrum = ESA.ask("TRA?")              # Get the spectrum
    #ESA.write("CONTS;") # Set to continuous sweep mode
    #ESA.write("VAVG 1;") # Turn on/off video averaging

    ESA_spectrum = [float(x) for x in ESA_spectrum.split(',')] # Convert strings to numbers 
    ESA_frequencies = np.linspace(center-span/2.0,center+span/2.0,len(ESA_spectrum))

    # save the data
    np.savetxt("%s.txt"%(filename), (ESA_frequencies,ESA_spectrum))

    plt.plot(ESA_frequencies, ESA_spectrum,'-g')
    plt.savefig("%s.png"%(filename))
    plt.close()
    
    #laser = SANTEC_TL()
    #LaserPower=laser.power.value
    #LaserWL=laser.wavelength.value
    
    #DAT='ResolutionBandwidth %s , VideoBandwidth %s , SweepTime %s , OpticalPower %s , LaserPower %s , LaserWavelength %s'%( ResolutionBW,VideoBW,SweepTime,OptPowerESA,LaserPower,LaserWL)
    DAT='ResolutionBandwidth %s , VideoBandwidth %s , SweepTime %s , OpticalPower %s '%( ResolutionBW,VideoBW,SweepTime,OptPowerESA)
    with open("%s_STATUS.txt"%(filename), "w") as text_file:
        text_file.write(DAT)

    
test1()