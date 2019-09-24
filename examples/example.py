#!/usr/bin/env python

from datetime import datetime, timedelta

from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.oceandrift import OceanDrift

o = OceanDrift(loglevel=0)  # Set loglevel to 0 for debug information

# Norkyst ocean model
#reader_norkyst = reader_netCDF_CF_generic.Reader(o.test_data_folder() + '16Nov2015_NorKyst_z_surface/norkyst800_subset_16Nov2015.nc')
#reader_arome = reader_netCDF_CF_generic.Reader(o.test_data_folder() + '16Nov2015_NorKyst_z_surface/arome_subset_16Nov2015.nc')
reader_arome = reader_netCDF_CF_generic.Reader('wam.nc')
print(reader_arome)
print(reader_arome.derived_variables)
#reader_arome.plot('x_wind')
#reader_arome.plot('y_wind')
reader_arome.plot('wind_speed')
stop

# Uncomment to use live data from thredds
#reader_arome = reader_netCDF_CF_generic.Reader('http://thredds.met.no/thredds/dodsC/meps25files/meps_det_extracted_2_5km_latest.nc')
#reader_norkyst = reader_netCDF_CF_generic.Reader('http://thredds.met.no/thredds/dodsC/sea/norkyst800m/1h/aggregate_be')

o.add_reader([reader_arome])
print(o)

# Seeding some particles
lon = 4.6; lat = 60.0; # Outside Bergen

#time = datetime(2015, 9, 22, 6, 0, 0)
time = [reader_arome.start_time,
        reader_arome.start_time + timedelta(hours=30)]
#time = reader_arome.start_time

# Seed oil elements at defined position and time
o.seed_elements(lon, lat, radius=50, number=100, time=time)

# Adjusting some configuration
o.set_config('general:use_basemap_landmask', False)
o.fallback_values['land_binary_mask'] = 0
o.fallback_values['x_sea_water_velocity'] = 0
o.fallback_values['y_sea_water_velocity'] = 0

# Running model
o.run(steps=4, time_step=1800, time_step_output=3600)

# Print and plot results
print(o)
#o.plot(background=['x_sea_water_velocity', 'y_sea_water_velocity'], buffer=.5)
o.animation()
o.plot()
