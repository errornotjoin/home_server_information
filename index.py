#imports of necessary modules
#DON@T REMOVE ANY OF THESE IMPORTS AS THEY ARE ALL NECESSARY FOR THE SCRIPT TO WORK
import os

import psutil
import pathlib
import yaml
import datetime
import upload_it_database

#lists to store drive information
drivces_size = []
drive_Used = []
drivces_free_space = []
drivecs_little = []
driveces_last_check = []
#items that won't be scanned
#note this feature is not yet implemented
#you can remove the drives from the yml file (list_of_drives.yml)
blacklisted_files = []
#lists to store file  information
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
#last check time list
last_check = []

def get_drive_file_names():
    #function to get file and folder names in the drives
    for file in drivecs_little:
        #walk through the drive (walk = go through all files and folders in the drive)
        for current_path, folder, files in os.walk(file):
            #print current path
            try:
                #if there are no files or folders, raise an exception
                #print("Current Path: " + str(current_path))
                file_paths.append(current_path)
                #print folder and file names with creation date and time
                for name in folder:
                    #print("Folder name: " + name)
                    folder_path = os.path.join(current_path, name)
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
                    folder_dates.append(datetime.datetime.fromtimestamp(os.path.getmtime(current_path + "\\" + name)).strftime("%y-%m-%d %H:%M:%S"))
                    folder_paths.append(current_path + "\\" + name)
                for name in files:
                    #print file name and creation date and time
                    file_name.append(name)
                    creation_date.append(datetime.datetime.fromtimestamp(os.path.getmtime(current_path + "\\" + name)).strftime("%y-%m-%d %H:%M:%S"))
                    file_path = os.path.join(current_path, name)
                    file_paths.append(current_path + "\\" + name)
                    file_size_value = os.path.getsize(file_path)    
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
        upload_it_database.upload_drives_information(drivecs_little, drivces_size, drive_Used, drivces_free_space,driveces_last_check, folder_name,folder_dates,folder_size,folder_paths,file_name,file_size,file_extension,file_paths,creation_date)

    
    
    
    
#get current date and time
time = datetime.datetime.now()
Date = time.strftime("%y-%m-%d %H:%M:%S")

#flag to check if we need to check drives info
need_to_check = False


def getting_drivces_basic_info():
    with open("yml_files/list_of_drives.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        last_check = open("txt_files/last_check.txt", 'r') 
        user_manual_scan = open("txt_files/User_what_to_check.txt", 'r')
        last_check_value = last_check.read()
        user_manual_scan_value = user_manual_scan.read()
        #check if last check date and time was different from today or user manual scan is true
        if last_check_value != Date or user_manual_scan_value == "User_manual_scan = true" :
            #we do need to check because either last check was different from today or user manual scan is true
            need_to_check = True
            last_check.close()
            user_manual_scan.close()
        else:
            #we don't need to check anything
            need_to_check = False
            last_check.close()
            user_manual_scan.close()
        if need_to_check == True:
            #asking user if they want to see drive information 
            #only if the user is in visual code or terminal 
            #as php can't handle input function like this
            #this just been removed for now to make it work with php
            #you can add it back if you are only using terminal or visual code
            #user_input = input("Do you want to see drive information while scanning? (y/n): ")
            user_input = 'n'  #default to no if manual scan
            for drive in cfg['drives']:        
                try:
                    # Get drive usage statistics
                    drive_size = psutil.disk_usage(drive)
                    drivces_size.append(str(round(drive_size[0] / (1024 ** 3))) +"GB")  # Convert bytes to gigabytes
                    drive_Used.append(str(round(drive_size[1] / (1024 ** 3))) +"GB")
                    drivces_free_space.append(str(round(drive_size[2] / (1024 ** 3))) +"GB")
                    driveces_last_check.append(Date)
                    
                    drivecs_little.append(drive)


                #this exception is raised when the drive is not accessible
                except PermissionError:
                    pass
                except FileNotFoundError:
                    pass
                except UnboundLocalError:
                    pass
        else:
            exit()
        #update last check date and time
        last_check = open("txt_files/last_check.txt", 'w') 
        user_manual_scan = open("txt_files/User_what_to_check.txt", 'w')
        last_check.write(f"{Date}")
        #reset user manual scan to false
        #as we have already done the manual scan
        user_manual_scan.write("User_manual_scan = false")
        #reclose files
        last_check.close()
        user_manual_scan.close()
        get_drive_file_names()



getting_drivces_basic_info()