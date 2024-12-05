import glob
import os
from joblib import Parallel, delayed

#sac_folder = "./Data/min_wise"
sac_folder = "./Data/day_wise_agc"
sac_files = list(glob.iglob(sac_folder+"/*.sac"))

dates = [i.split("/")[-1].split("_")[2].split(".sac")[0] for i in sac_files ]
dates = list(set(dates))

date_dict = {}
for date in dates:
	#if "2024-09-21" in date or "2024-09-22" in date or "2024-09-23" in date :
	date_dict[date]=[]
	
for sac_file in sac_files:
	date = sac_file.split("/")[-1].split("_")[2].split(".sac")[0]
	if date in date_dict.keys():
		date_dict[date].append(sac_file)
'''	
for k in date_dict.keys():
	l = len(date_dict[k])
	for i in range(l-1):
		f1 = date_dict[k][i]
		for j in range(i+1,l):
			print(date,i,j)
			f2 = date_dict[k][j]
			p1 = int(f1.split('_')[2])
			p2 = int(f2.split('_')[2])
			c1 = min(p1,p2)
			c2 = max(p1,p2)
			ccgn = f"cc_{c1}_{c2}_ccgn_{date}"
			pcc = f"cc_{c1}_{c2}_pcc_{date}"
			cmd = "pcc5iMP "+f1+" "+f2+" "+"isac,isac"+" "+"tl1=-59.9"+" "+"tl2=59.9"+" "+"ccgn="+ccgn+" "+"pcc="+pcc+" "+"osac nn"
			os.system(cmd)
			os.system(f"mv {ccgn}.sac Data/cc/GNCC/")
			os.system(f"mv {pcc}.sac Data/cc/PCC/")
			#break
		#break
	
	#break

'''
# Define a function to process each date key in parallel

def process_date(date, files):
    l = len(files)
    for i in range(l - 1):
        f1 = files[i]
        for j in range(i + 1, l):
            print(date,i,j)
            f2 = files[j]
            p1 = int(f1.split("/")[-1].split("_")[1])
            p2 = int(f2.split("/")[-1].split("_")[1])
            c1 = min(p1,p2)
            c2 = max(p1,p2)
            
            ccgn = f"cc_{c1}_{c2}_ccgn_{date}"
            pcc = f"cc_{c1}_{c2}_pcc_{date}"
            cc = f"cc_{c1}_{c2}_cc1b_{date}"
            #cmd = "pcc5iMP "+f1+" "+f2+" "+"isac,isac"+" "+"tl1=-59.9"+" "+"tl2=59.9"+" "+"ccgn="+ccgn+" "+"pcc="+pcc+" "+"osac nn"
            cmd = "pcc5iMP "+f1+" "+f2+" "+"isac,isac"+" "+"tl1=-59.9"+" "+"tl2=59.9"+" "+"ccgn="+ccgn+" "+"osac nn"
            #if not os.path.exists("Data/cc/GNCC/"+ccgn+".sac"):
            os.system(cmd)
            #os.system(f"mv {ccgn}.sac Data/cc/GNCC/")
            #os.system(f"mv {pcc}.sac Data/cc/PCC/")
            os.system(f"mv {ccgn}.sac Data/cc/GNCC_agc/")
            #break
        #break
    
    
Parallel(n_jobs=32)(delayed(process_date)(date, date_dict[date]) for date in date_dict.keys())



	


	
