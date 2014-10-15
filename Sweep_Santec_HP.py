from intec.pymeasure.instruments import *
from pymeasure.units.unit import *
from numpy import *
from time import gmtime, strftime
import pylab as plt

#defining your instruments
laser = SANTEC_TL()
#laser = TUNICS_TL()
power_meter = HP_PM()
laser.initialize()
power_meter.initialize()
power_meter.range = 'AUTO'
power_meter.power_unit = DBM

#initialize the instruments
#start_wl=laser.wavelength.value


# open a file to save your data
timestamp=strftime("h%Hm%Ms%S-%d%b%Y", gmtime())
filename = 'Spectr_2_wide.txt'
outfile = open(filename,'w')

# (optionally: changing the settings of your instruments)
power_meter.channel = 'A'
#power_meter.instrument_power_unit = DBM
laser.power = 10 * DBM

# lasPOW=laser.power

# set your measurement parameters:
wl_start = 1539.0
wl_stop = 1541.0
wl_step = .01

wl_range = arange(wl_start, wl_stop+wl_step,wl_step)
#wl_range = arange(wl_stop, wl_start-wl_step,-wl_step)

# create a list to store the power
power_values = []

# perform the sweep
for wl in wl_range:
    # change the wavelength of laser and power meter
    laser.wavelength = wl * NANOMETER
    power_meter.wavelength = wl * NANOMETER
    # read out the power
    P = power_meter.get_power(unit=DBM).value
    power_values.append(P)
    print wl
    # save to a file
    print >> outfile, wl, P
    outfile.flush()
outfile.close()

#laser.wavelength=start_wl* NANOMETER

# make the plot
plt.plot(wl_range,power_values)
plt.savefig("%s.png"%(filename))
plt.show()