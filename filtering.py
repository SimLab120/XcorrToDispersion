import os
from obspy import read
from obspy.core import UTCDateTime

# Define the path to the folder containing your original .sac files
sac_folder_path = 'Data/cc/All_day_stack_GNCC_ts_pws'
# Define the path to the destination folder where filtered .sac files will be saved
filtered_sac_folder_path = 'Data/cc/Filtered_All_day_stack_GNCC_ts_pws_1_10'

# Ensure the destination folder exists
os.makedirs(filtered_sac_folder_path, exist_ok=True)

# Bandpass filter parameters
freqmin = 1
freqmax = 10
corners = 10
zerophase = True

# Loop through all .sac files in the sac_folder_path
for filename in os.listdir(sac_folder_path):
    if filename.endswith('.sac'):
        file_path = os.path.join(sac_folder_path, filename)
        
        # Read the .sac file using ObsPy
        st = read(file_path)
        
        # Apply the bandpass filter to the data
        st.filter("bandpass", freqmin=freqmin, freqmax=freqmax, corners=corners, zerophase=zerophase)
        
        # Construct the path for saving the filtered file
        filtered_file_path = os.path.join(filtered_sac_folder_path, filename)
        
        # Save the filtered data in .sac format
        st.write(filtered_file_path, format="SAC")
        
        print(f"Filtered and saved: {filtered_file_path}")

