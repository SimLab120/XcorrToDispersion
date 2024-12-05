import obspy
import numpy as np
import os
import glob

data_folder = "Data/min_wise"

destination = "Data/min_wise_1bit"

def convert_array(arr):
    return np.array([1 if x > 0 else -1 if x < 0 else 0 for x in arr])

sac_files = glob.glob(data_folder+"/"+"rec_*.sac")

for sacname in sac_files:
	new_sacname = destination+"/"+sacname.split("/")[-1]
	st = obspy.read(sacname,format="SAC")
	tr = st[0]
	tr.data = convert_array(tr.data)
	st.write(new_sacname, format='SAC')
	#break
