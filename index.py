#imports of necessary modules
#DON@T REMOVE ANY OF THESE IMPORTS AS THEY ARE ALL NECESSARY FOR THE SCRIPT TO WORK
import psutil
import yaml
import datetime
#files in the folder 
#these are required for the script to work
#make sure these files are in the same folder as this script
import upload_it_database
import only_storage

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

#last check time list
last_check = []


#get current date and time
time = datetime.datetime.now()
Date = time.strftime("%y-%m-%d %H:%M:%S")

#flag to check if we need to check drives info
need_to_check = False


def getting_drivces_basic_info(is_full_scan):
    with open("yml_files/list_of_drives.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        for drive in cfg['drives']:     
            print("Checking drive: " + drive)   
            try:
                driveces_last_check.append(Date)
                drivecs_little.append(drive)
                drive_size = psutil.disk_usage(drive)
                drivces_size.append(str(round(drive_size[0] / (1024 ** 3))) +"GB")  # Convert bytes to gigabytes
                drive_Used.append(str(round(drive_size[1] / (1024 ** 3))) +"GB")
                drivces_free_space.append(str(round(drive_size[2] / (1024 ** 3))) +"GB")

            #this exception is raised when the drive is not accessible
            except PermissionError:
                print("Permission denied to access drive: " + drive)
            except FileNotFoundError:
                print("Drive not found: " + drive)
            except UnboundLocalError:
                print("Drive not found: " + drive)
            except Exception as e:
                print("An error occurred while accessing drive: " + drive)
                print(str(e))
        print("Drive information collected.")
        print(len(drivecs_little), len(drivces_size), len(drive_Used), len(drivces_free_space), len(driveces_last_check))
        #update last check date and time
        if is_full_scan:
            only_storage.get_drive_file_names(drivces_size, drive_Used, drivces_free_space, driveces_last_check, drivecs_little)
        else:
            upload_it_database.upload_drives_information(drivecs_little, drivces_size, drive_Used, drivces_free_space, driveces_last_check, [], [], [], [], [], [], [], [], [])
            print("Drive information updated in the database.")

with open("yml_files/what_type_of_scan.yml", 'r') as ymlfile:
    ctf = yaml.safe_load(ymlfile)
    for scan_type in ctf['types_of_scans']:
        items = scan_type
        if items == 'full_scan' and ctf['types_of_scans'][items]['booledan'] == True:
            print("Starting full scan...")
            getting_drivces_basic_info(True)
        elif items == 'drive_only_scan' and ctf['types_of_scans'][items]['booledan'] == True:
            print("Starting drive only scan...")
            getting_drivces_basic_info(False)
        elif items == 'Folder_file_only_scan' and ctf['types_of_scans'][items]['booledan'] == True:
            print("Starting folder and file only scan...")
            with open("yml_files/list_of_drives.yml", 'r') as ymlfile:
                cfg = yaml.safe_load(ymlfile)
                for drive in cfg['drives']:
                    drivecs_little.append(drive)
            only_storage.get_drive_file_names(drivecs_little, drivces_size, drive_Used, drivces_free_space,driveces_last_check)
      
        



