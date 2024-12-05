import glob
from obspy import read
import obspy
import utm
import pandas as pd


data_folder = "./Data"
coord = pd.read_csv("Data/coordinates.csv",header=0)
sgy_files = list(glob.iglob(data_folder+"/*.sgy"))
for sgy_file in sgy_files:
	print(sgy_file)
	node = sgy_file.split("_")[7]
	lon,lat=coord[coord.NODE==node].LONGITUDE.iloc[0],coord[coord.NODE==node].LATITUDE.iloc[0]
	st = read(sgy_file,format="SEGY",unpack_trace_headers=True)
	rec_ind = sgy_files.index(sgy_file)
	start_dates = []
	for i in range(len(st)):
		tr = st[i]
		start_dates.append(tr.stats.starttime.date.strftime(format="%Y-%m-%d"))
	start_dates=set(start_dates)
	#start_dates.remove('2024-09-20')
	
	merge_dict = {}
	for start_date in start_dates:
		merge_dict[start_date] =  []
	'''	
	for i in range(len(st)):
		tr = st[i]
		tr.decimate(10, strict_length=False, no_filter=True)
		date = tr.stats.starttime.date.strftime(format="%Y-%m-%d")
		if date in merge_dict.keys():
			merge_dict[date].append(i)
		full_date_time = tr.stats.starttime.strftime(format="%Y-%m-%dT%H:%M:%S.%f")
		min_wise_sac_file = data_folder+"/min_wise/"+"rec_"+str(rec_ind+1)+"_"+full_date_time+".sac"
		tr.data = (10**4)*tr.data
		stream = obspy.core.stream.Stream(traces=tr)
		stream.write(min_wise_sac_file,format="SAC")
		stream = read(min_wise_sac_file,format="SAC")
		stream[0].stats.sac.stla,stream[0].stats.sac.stlo = lat,lon
		stream.detrend("demean")
		stream.detrend("linear")
		stream.taper(max_percentage=0.1,type="cosine")
		stream.write(min_wise_sac_file,format="SAC")
	'''	
		
		
	
	for i in range(len(st)):
		tr = st[i]
		#tr.decimate(10, strict_length=False, no_filter=True)
		date = tr.stats.starttime.date.strftime(format="%Y-%m-%d")
		if date in merge_dict.keys():
			merge_dict[date].append(i)	
	
	trs = []
	for start_date in merge_dict.keys():
		indices = merge_dict[start_date]
		tr = st[indices[0]]
		for i in range(1,len(indices)):
			tr += st[indices[i]]
		tr.decimate(10, strict_length=False, no_filter=True)
		trs.append(tr)
		
		print(tr)
		stream = obspy.core.stream.Stream(traces=tr)
		
		sac_file = data_folder+"/day_wise/"+"rec_"+str(rec_ind+1)+"_"+start_date+".sac"
		
		stream.write(sac_file, format='SAC')
		stream = read(sac_file,format="SAC")
		stream[0].stats.sac.stla,stream[0].stats.sac.stlo = lat,lon
		stream.detrend("demean")
		stream.detrend("linear")
		stream.taper(max_percentage=0.1,type="cosine")
		stream.write(sac_file,format="SAC")
	#new_tr = trs[0]	
	#for j in range(1,len(trs)):
	#	new_tr = new_tr + trs[j]
	#combined_stream = obspy.core.stream.Stream(traces=new_tr)
	#combined_sac_name = data_folder+"/"+"rec_"+str(rec_ind+1)+".sac"
	#combined_stream.write(combined_sac_name, format='SAC')
	
	
	#break
	

