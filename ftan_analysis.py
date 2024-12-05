import pandas as pd
import numpy as np
from obspy import read
import os
import glob
import sys
import pickle


def read_base_ftan(sacname):
    hdr=pd.read_table(sacname+'_1_AMP',  header=None, delim_whitespace=True, nrows=1)
    amp_data = pd.read_table(sacname+'_1_AMP', delim_whitespace=True, header=None, skiprows=1).to_numpy()
    nrow = hdr[0][0]
    ncol = hdr[1][0]
    dt = hdr[2][0]
    delta = hdr[3][0]
    disp = pd.read_table(sacname+'_1_DISP.1', delim_whitespace=True, header=None).to_numpy()
    per = disp[:, 2]
    gvel = disp[:, 3]
    pvel = disp[:,4]
    snr = disp[:,6]
    return delta, per, gvel, pvel, snr

def read_match_ftan(sacname):
    hdr=pd.read_table(sacname+'_2_AMP',  header=None, delim_whitespace=True, nrows=1)
    amp_data = pd.read_table(sacname+'_2_AMP', delim_whitespace=True, header=None, skiprows=1).to_numpy()
    nrow = hdr[0][0]
    ncol = hdr[1][0]
    dt = hdr[2][0]
    delta = hdr[3][0]
    disp = pd.read_table(sacname+'_2_DISP.1', delim_whitespace=True, header=None).to_numpy()
    per = disp[:, 2]
    gvel = disp[:, 3]
    pvel = disp[:,4]
    snr = disp[:,6]
    return delta, per, gvel, pvel, snr

#lags = np.linspace(-115.0, 115.0, 461)
workdir='/home/santosh/Pragyant/Work/SAC'

	
per_limits=np.loadtxt('paramc.dat', usecols=[3,4], dtype=float) # min and maximum periods used

path_base=[]
stn1_base = []
stn2_base = []
periods_base = []
distance_base = []
periods_base = []
group_velocity_base = []
phase_velocity_base = []
s_base = []

path_match=[]
stn1_match = []
stn2_match = []
periods_match = []
distance_match = []
periods_match = []
group_velocity_match = []
phase_velocity_match = []
s_match = []

for path in glob.glob(workdir+"/*"):
	print(path)
	
	
	disp_base="disp_table_base_"+path.split("/")[-1]+".txt"
	disp_match="disp_table_match_"+path.split("/")[-1]+".txt"
	param='paramc.dat'
	mod_param="param1_"+path.split("/")[-1]+".dat"
		
	if not os.path.isfile(disp_base):
		with open(disp_base,'w') as f:
			f.write("path\tsac\n")
		f.close()

	if not os.path.isfile(disp_match):
		with open(disp_match,'w') as f:
			f.write("path\tsac\n")
		f.close()
	
	for filename in glob.glob(path+"/*.sac"):
		sacfile=filename
		print(sacfile)
		
		df=pd.read_csv(disp_base,sep="\t")
				
		if path.split("/")[-1] in list(df['path']) and sacfile.split("/")[-1] in list(df['sac']):
			pass
		else:
		
			input_df = pd.read_table(param, header=None, delim_whitespace=True)
			output_df=input_df
			output_df[10][0] = sacfile
			output_df.to_csv(mod_param,index=False, header=False, sep=' ')

			try:
				tr = read(sacfile)
			except TypeError:
				print("Could not open/read file")
				continue
    		
			if tr:
				os.system('aftan_c_test '+mod_param)
				os.system('rm -f '+mod_param)

			if os.path.isfile(sacfile+'_1_DISP.1'):
				with open(disp_base,'a') as f:
					f.write(path.split("/")[-1]+"\t"+sacfile.split("/")[-1]+"\n")
				f.close()
				[dist_base, per_base, gvel_base, pvel_base, snr_base] = read_base_ftan(sacfile)
				s1b=int(filename.split("/")[-1].split("_")[1].split("-")[0])
				s2b=int(filename.split("/")[-1].split("_")[1].split("-")[1])

				path_base.append(sacfile)
				stn1_base.append(s1b)
				stn2_base.append(s2b)
				distance_base.append(dist_base)
				periods_base.append(per_base)
				group_velocity_base.append(gvel_base)
				phase_velocity_base.append(pvel_base)
				s_base.append(snr_base)
				
				
			if os.path.isfile(sacfile+'_2_DISP.1'):
				with open(disp_match,'a') as f:
					f.write(path.split("/")[-1]+"\t"+sacfile.split("/")[-1]+"\n")
				f.close()
				[dist_match, per_match, gvel_match, pvel_match, snr_match] = read_match_ftan(sacfile)
				s1m=int(filename.split("/")[-1].split("_")[1].split("-")[0])
				s2m=int(filename.split("/")[-1].split("_")[1].split("-")[1])
				
				path_match.append(sacfile)
				stn1_match.append(s1m)
				stn2_match.append(s2m)
				distance_match.append(dist_match)
				periods_match.append(per_match)
				group_velocity_match.append(gvel_match)
				phase_velocity_match.append(pvel_match)
				s_match.append(snr_match)
				
									
			for f in glob.glob(filename+"_*"):
				os.remove(f)		

		#break

	#break

disp_table_base={'path base':path_base,
		'station1 base': stn1_base,
                'station2 base': stn2_base,
                'distance base': distance_base,
                'periods base': periods_base,
                'group velocity base': group_velocity_base,
                'phase velocity base': phase_velocity_base,
                'snr base': s_base}

disp_table_match={'path match':path_match,
		 'station1 match': stn1_match,
                 'station2 match': stn2_match,
                 'distance match': distance_match,
                 'periods match': periods_match,
                 'group velocity match': group_velocity_match,
                 'phase velocity match': phase_velocity_match,
                 'snr match': s_match}

with open('disp_table_base.pickle', 'wb') as handle:
    pickle.dump(disp_table_base, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('disp_table_match.pickle', 'wb') as handle:
    pickle.dump(disp_table_match, handle, protocol=pickle.HIGHEST_PROTOCOL)

