import os
import glob
import obspy
from obspy.signal import PPSD
from datetime import datetime

folder="Data/day_wise"

paz = {'gain': 60077000.0,
       'poles': [-0.037004+0.037016j, -0.037004-0.037016j,
                 -251.33+0j, -131.04-467.29j, -131.04+467.29j],
       'sensitivity': 2516778400.0,
       'zeros': [0j, 0j]}

for i in range(1,15):
	files_path = list(glob.glob(folder+f"/rec_{i}_*.sac"))
	b_25,a_25 = [],[]
	for s in files_path:
		d = s.split("/")[-1].split("_")[2].split(".sac")[0]
		d1 = datetime.strptime(d, "%Y-%m-%d")
		d2 = datetime.strptime("2024-09-25", "%Y-%m-%d")
		if d1<=d2:
			b_25.append(s)
		else:
			a_25.append(s)
		# print(d)
	for f in b_25:
		st = obspy.read(f,format="SAC")
		tr = st[0]
		if b_25.index(f) == 0:
			ppsd = PPSD(tr.stats, paz)
		else:
			ppsd.add(st)
	ppsd.plot(f"./PPSD_img/rec_{i}_b_25")
	
	for f in a_25:
		st = obspy.read(f,format="SAC")
		tr = st[0]
		if a_25.index(f) == 0:
			ppsd = PPSD(tr.stats, paz)
		else:
			ppsd.add(st)
	ppsd.plot(f"./PPSD_img/rec_{i}_a_25")
	
	break
	
