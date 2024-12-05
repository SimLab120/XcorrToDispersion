import os
import shutil
from datetime import datetime
from joblib import Parallel, delayed

# Define the path to the folder containing your .sac files
sac_folder_path = './Data/cc/CC1b'
# Define the path to the destination folder where pair folders will be created
destination_folder_path = './Data/cc/Stacked_CC1b'

# Function to convert a date to Julian day
def to_julian_day(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%Y.%j")

# Function to process each file
def process_file(filename):
    if filename.endswith('.sac'):
        print(filename)
        # Split the filename to get pair identity and date-time information
        parts = filename.split('_')
        pair_identity = '_'.join([parts[1], parts[2]])  # Sorting for symmetric pair identities like 12_9 and 9_12
        datetime_str = parts[4].replace(".sac", "")
        
        # Parse date and time from the filename
        date_str, time_str = datetime_str.split('T')
        julian_day = to_julian_day(date_str)
        time_str = time_str.replace(":", ".")
        
        # Create the new filename in the desired format
        new_filename = f"cc_{pair_identity}_cc1b_{julian_day}.{time_str}.sac"
        
        # Create directories inside the destination folder
        pair_dir = os.path.join(destination_folder_path, pair_identity)
        date_dir = os.path.join(pair_dir, date_str)
        os.makedirs(date_dir, exist_ok=True)
        
        # Move and rename the file
        old_filepath = os.path.join(sac_folder_path, filename)
        new_filepath = os.path.join(date_dir, new_filename)
        shutil.copy(old_filepath, new_filepath)

        print(f"Copied and renamed: {filename} -> {new_filepath}")

# Ensure the destination folder exists
os.makedirs(destination_folder_path, exist_ok=True)

# Get the list of all .sac files
all_files = os.listdir(sac_folder_path)

# Use joblib to parallelize the processing
Parallel(n_jobs=64)(delayed(process_file)(filename) for filename in all_files)


'''
# Iterate over each pair folder
for pair_folder_name in os.listdir(destination_folder_path):
    pair_folder_path = os.path.join(destination_folder_path, pair_folder_name)
    
    # Check if it's a directory
    if os.path.isdir(pair_folder_path):
        
        # Iterate over each date subfolder within the pair folder
        for date_folder_name in os.listdir(pair_folder_path):
            date_folder_path = os.path.join(pair_folder_path, date_folder_name)
            
            # Check if it's a directory
            if os.path.isdir(date_folder_path):
                
                # Generate a unique name for this date subfolder based on pair and date
                unique_name = "cc_"+f"{pair_folder_name}_{date_folder_name}"
                #unique_name_path = os.path.join(date_folder_path, unique_name)
                
                # List all .sac files in the current date folder
                sac_files = [date_folder_path+"/"+f for f in os.listdir(date_folder_path) if f.endswith(".sac")]
                
                # Create a file to list all .sac filenames in this date folder
                list_file_path = os.path.join(date_folder_path, "file_list.txt")
                with open(list_file_path, "w") as list_file:
                    list_file.write(f"# File list for {unique_name}\n")
                    for sac_file in sac_files:
                        list_file.write(sac_file + "\n")
              
                
                cmd = "ts_pws"+" "+list_file_path+" rm unbiased "#+"osac="+unique_name                
                os.system(cmd)
                
                s_path = os.path.join("./", "tl_"+unique_name+".sac")
                d_path = os.path.join(date_folder_path, "tl_"+unique_name+".sac")
                shutil.copy(s_path, d_path)
                
                s_path = os.path.join("./", "ts_pws_"+unique_name+".sac")
                d_path = os.path.join(date_folder_path, "ts_pws_"+unique_name+".sac")
                shutil.copy(s_path, d_path)
                
                break
'''

