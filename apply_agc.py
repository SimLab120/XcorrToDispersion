import os
import glob 
import obspy
import numpy as np
from agc import agc

home_folder = "Data/day_wise"
destination_folder = "Data/day_wise_agc"

sacfiles = list(glob.glob(home_folder+"/*.sac"))

for sacfile in sacfiles:
	
	n_sacfile = "day_wise_agc".join(sacfile.split("day_wise"))
	print(n_sacfile)
	
	st = obspy.read(sacfile,format="sac")
	tr = st[0]
	tr.data = agc(np.expand_dims(tr.data,axis=1),time=tr.times(),agc_type="rms",time_gate=10)[:,0]
	st.write(n_sacfile,format="sac")
	#break
