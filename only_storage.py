import os
import psutil
import pathlib
import yaml
import datetime

import upload_it_database

file_paths = []
file_name = []
file_size = []
file_extension = []
#folderse info
folder_name = []
folder_paths = []
folder_dates = []
folder_size = []
creation_date = []
def get_drive_file_names(drive_names, total_sizes, used_spaces, free_spaces,driveces_last_check):
    #function to get file and folder names in the drives
    print("Collecting file and folder information from drives...", flush=True)
    with open("yml_files/list_of_drives.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        for drive in cfg['drives']:
            file = drive
            #walk through the drive (walk = go through all files and folders in the drive)
            for current_path, folder, files in os.walk(file):
                #print current path
                try:
                    #if there are no files or folders, raise an exception
                    #print("Current Path: " + str(current_path))
                    #file_paths.append(current_path)
                    #print folder and file names with creation date and time
                    for name in folder:
                        #print("Folder name: " + name)
                        #getting the folder path and size
                        folder_path = os.path.join(current_path, name)

                        new_folder_path = folder_path
                        new_folder_path = new_folder_path.replace("\\", "/")
                        folder_paths.append(new_folder_path)

                        folder_size_value = os.path.getsize(folder_path)
                        folder_name.append(name)
                        #print("Folder name added: " + name)
                        #get folder size in KB, MB, GB
                        if folder_size_value >= 1024 ** 3:
                            folder_size.append(str(round(folder_size_value / (1024 ** 3))) +"GB")
                            #print("Folder size in GB added." + str(round(folder_size_value / (1024 ** 3))) +"GB")
                        elif folder_size_value >= 1024 ** 2:
                            #print("Folder size in MB added." + str(round(folder_size_value / (1024 ** 2))) +"MB")
                            folder_size.append(str(round(folder_size_value / (1024 ** 2))) +"MB")
                        elif folder_size_value >= 1024:
                            #print("Folder size in KB added.")
                            folder_size.append(str(round(folder_size_value / (1024))) +"KB")
                        else:
                            folder_size.append("0KB")
                        folder_dates.append(datetime.datetime.fromtimestamp(os.path.getmtime(folder_path)).strftime("%y-%m-%d %H:%M:%S"))
                        #don't know why that is there but it is there in the original code, so I will keep it there
                        #folder_paths.append(folder_path)
                    for name in files:
                        #print file name and creation date and time
                        file_name.append(name)
                        #get file creation date and time
                        file_path = os.path.join(current_path, name)
                        creation_date.append(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%y-%m-%d %H:%M:%S"))
                        #getting the file path and size
                        #making it eastier for php to read the file path by replacing backslashes with forward slashes
                        new_file_path = os.path.join(current_path, name)
                        new_file_path = new_file_path.replace("\\", "/")
                        file_paths.append(new_file_path)
                        file_size_value = os.path.getsize(file_path)
                        #get file creation date and time
                        creation_date.append(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%y-%m-%d %H:%M:%S"))
                        #get file size in KB, MB, GB    
                        if file_size_value >= 1024 ** 3:
                            file_size.append(str(round(file_size_value / (1024 ** 3))) +"GB")
                        elif file_size_value >= 1024 ** 2:
                            file_size.append(str(round(file_size_value / (1024 ** 2))) +"MB")
                        elif file_size_value >= 1024:
                            file_size.append(str(round(file_size_value / (1024))) +"KB")
                        else:
                            file_size.append("0KB")
                        file_extension.append(pathlib.Path(name).suffix)
                        #print("File name added: " + name + " with extension: " + pathlib.Path(name).suffix)
                except PermissionError:
                    pass
                except FileNotFoundError:
                    pass
                except UnboundLocalError:
                    pass
                except NotADirectoryError:
                    pass
                except KeyboardInterrupt:
                    user_input = input("Process interrupted by user. Do you want to exit? (y/n): ")
                    if user_input.lower() == 'y':
                        print("Process interrupted by user.", flush=True)
                        exit()
                    else:
                        print("Continuing process...", flush=True)
                        continue
        print("File and folder information collected.", flush=True)
    with open("yml_files/what_type_of_scan.yml", 'r') as ymlfile:
        ctf = yaml.safe_load(ymlfile)
        for scan_type in ctf['types_of_scans']:
            items = scan_type
            print(items, flush=True)
            if items == 'full_scan' and  ctf['types_of_scans'][items]['booledan'] == "True":
                print("Starting full scan...", flush=True)
                upload_it_database.upload_drives_information(drive_names, total_sizes, used_spaces, free_spaces,driveces_last_check,folder_name,folder_dates,folder_size,folder_paths,file_name,file_size,file_extension,file_paths)
            elif items == 'Folder_file_only_scan' and ctf['types_of_scans'][items]['booledan'] == "True":
                upload_it_database.uploading_folder(folder_name,folder_dates,folder_size,folder_paths,file_name,file_size,file_extension,file_paths)