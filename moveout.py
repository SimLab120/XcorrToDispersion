import pygmt
import numpy as np
import os
import glob
import obspy
from datetime import datetime, timedelta


def extract_substring(text, search_string, length=10):
    # Find the starting index of the search string
    start_index = text.find(search_string)
    
    if start_index == -1:
        return None  # Return None if the search string is not found
    
    # Extract the substring of the specified length starting from the search string
    return text[start_index:start_index + length]

'''
# Define the path to the folder containing your .sac files
r = "ts_pws"
sac_folder_path = f'Data/cc/Stacked_CC1b_{r}'
destination = f"Moveouts/Stacked_CC1b_{r}"
os.makedirs(destination,exist_ok=True)
t=np.arange(-59.9-0.04,59.9+0.04,0.04)

# Start and end dates
start_date = datetime.strptime("2024-09-20", "%Y-%m-%d")
end_date = datetime.strptime("2024-10-06", "%Y-%m-%d")

# Loop through each date in the range
current_date = start_date
sac_files_list = {}
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    sac_files_list[date_str] = []
    current_date += timedelta(days=1)
    #break
    
for filename in os.listdir(sac_folder_path):
	date = extract_substring(filename,"2024",10)
	if date in sac_files_list.keys():
		sac_files_list[date].append(os.path.join(sac_folder_path,filename))
	
    	

for date_str in sac_files_list.keys():
	fig = pygmt.Figure()
	fig.basemap(region=[-5, 5, 0, 4], projection="X10c", frame=["x2","y0.5"])
	for sac_file in sac_files_list[date_str]:
		st=obspy.read(sac_file)
		d=st[0].stats.sac.dist* np.ones(len(t))
		fig.wiggle(
		x=t,
		y=d,
		z=st[0].data, #*(5*10**3)
		# Set anomaly scale to 20 centimeters
		scale="20c",
		# Fill positive areas red
		fillpositive="red",
		# Fill negative areas gray
		fillnegative="gray",
		# Set the outline width to 1.0 point
		pen="0.01p",
		)
	fig.savefig(f"{destination}/moveout_{date_str}.png")
	#break
'''	
	
# Define the path to the folder containing your .sac files
r = "ts_pws_1_10"
sac_folder_path = f'Data/cc/Filtered_All_day_stack_PCC_{r}'
destination = f"Moveouts/Filtered_All_day_stack_PCC_{r}"
os.makedirs(destination,exist_ok=True)
t=np.arange(-59.9-0.04,59.9+0.04,0.04)
sac_files_list = glob.glob(sac_folder_path+"/*.sac")

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, 0, 4], projection="X10c", frame=["x2","y0.5"])
for sac_file in sac_files_list:
	st=obspy.read(sac_file)
	d=st[0].stats.sac.dist* np.ones(len(t))
	fig.wiggle(
	x=t,
	y=d,
	z=st[0].data*1000, #*(5*10**3)
	# Set anomaly scale to 20 centimeters
	scale="20c",
	# Fill positive areas red
	fillpositive="red",
	# Fill negative areas gray
	fillnegative="gray",
	# Set the outline width to 1.0 point
	pen="0.01p",
	)
fig.savefig(f"{destination}/moveout.png")

	   
   
