#!/usr/bin/env python
"""
Generic example
===============
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
import opendrift
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.oceandrift2 import OceanDrift

o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information

test_data = Path(os.path.abspath(
            os.path.join(os.path.dirname(opendrift.__file__),
                        '..', 'tests', 'test_data')))
test_data = str(test_data) + '/'

# Arome atmospheric model
reader_arome = reader_netCDF_CF_generic.Reader(test_data + '16Nov2015_NorKyst_z_surface/arome_subset_16Nov2015.nc')
# Norkyst ocean model
reader_norkyst = reader_netCDF_CF_generic.Reader(test_data + '16Nov2015_NorKyst_z_surface/norkyst800_subset_16Nov2015.nc')

o.add_reader([reader_norkyst, reader_arome])

#%%
# Seeding some particles
#time = datetime(2015, 9, 22, 6, 0, 0)
time = [reader_arome.start_time,
        reader_arome.start_time + timedelta(hours=30)]
#time = reader_arome.start_time

# Seed oil elements at defined position and time
o.seed_elements(lon=4.6, lat=60.0, radius=50, number=3000, time=time,
                wind_drift_factor=.02)
#%%
# Running model
o.run(end_time=reader_norkyst.end_time, time_step=1800,
      time_step_output=3600, outfile='openoil.nc',
      export_variables=['mass_oil'])

#%%
# Print and plot results
o.plot(fast=True)

o.animation(fast=True)

#%%
# .. image:: /gallery/animations/example_generic_0.gif
