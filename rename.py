import os

# Define the path to the main folder containing the pair_identity folders
main_folder_path = './Data/cc/Stacked_GNCC'

# Loop through all pair_identity folders
for pair_identity in os.listdir(main_folder_path):
    pair_identity_path = os.path.join(main_folder_path, pair_identity)
    
    # Check if it is a directory
    if os.path.isdir(pair_identity_path):
        # Loop through all date folders within the pair_identity folder
        for date_folder in os.listdir(pair_identity_path):
            date_folder_path = os.path.join(pair_identity_path, date_folder)
            
            sac_file_1 = os.path.join(date_folder_path,f"tl_cc_{date_folder}.sac")
            sac_file_1_re = os.path.join(date_folder_path,f"tl_cc_{pair_identity}_{date_folder}.sac")
            os.rename(sac_file_1, sac_file_1_re)
            
            sac_file_2 = os.path.join(date_folder_path,f"ts_pws_cc_{date_folder}.sac")
            sac_file_2_re = os.path.join(date_folder_path,f"ts_pws_cc_{pair_identity}_{date_folder}.sac")
            os.rename(sac_file_2, sac_file_2_re)
            

