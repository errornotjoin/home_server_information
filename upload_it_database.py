#import sql_login
import sql_login
import mysql.connector
import time
import datetime 



mysql_execution = sql_login.connection.cursor(buffered=True)
time = datetime.datetime.now()
is_in_database_folders = []


def upload_drives_information(drive_names, total_sizes, used_spaces, free_spaces,driveces_last_check, folder_name,folder_dates,folder_size,folder_paths,file_name,file_size,file_extension,file_paths,new_scan, Dates,):
    try: 
        for i in range(len(drive_names)):
            more = time.strftime("%Y-%m-%d %H:%M:%S")
            sql_Code = "SELECT drivecs_Name FROM drivces_ WHERE drivecs_Name = %s"
            mysql_execution.execute(sql_Code, (drive_names[i],))
            if mysql_execution.fetchone() is None and drive_names[i] != "":
                 is_in_database_folders.append("True")
                 print(is_in_database_folders[i])
            elif drive_names[i] != "":
                is_in_database_folders.append("False")
                print(is_in_database_folders[i])

            else:
                continue
    except mysql.connector.Error as err:
        pass
    except KeyboardInterrupt:
        exit()
    uploading_folder(folder_name,folder_dates,folder_size,folder_paths,file_name,file_size,file_extension,file_paths, Dates, new_scan)

def uploading_folder(folder_name,folder_dates,folder_size,folder_paths,file_name,file_size,file_extension,file_paths, Date, new_scan):
    y = 0 
    folder_name_not_in_db = []
    folder_dates_not_in_db = []
    folder_paths_not_in_db = []
    folder_size_not_in_db = []
    times = []

    folder_name_are_in_db = []
    folder_dates_are_in_db = []
    folder_paths_are_in_db = []
    folder_size_are_in_db = []

    try:
        sql_code = "SELECT folders_Name, Paths FROM folders "
        mysql_execution.execute(sql_code)
        #getting all the files from db in an set 
        all_folders_in_database = mysql_execution.fetchall()
        if all_folders_in_database is None:
            all_folders_in_database = []
        check_set = set(all_folders_in_database)
        #looping though the list
        for name, path, size, date in zip(folder_name, folder_paths,folder_size,folder_dates):
            print("Name:" +  name)
            times.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            #check if name and path in check_set
            if (name, path ) not in check_set:
                #is_in_database_folders.append("False")
                print(str(y) + name +  ": adding to database")

                folder_name_not_in_db.append(name)
                folder_dates_not_in_db.append(date)
                folder_paths_not_in_db.append(path)
                folder_size_not_in_db.append(size)

                y += 1 
            else:
                #is_in_database_folders.append("Ture")
                #print(str(y) + ": Update the database")
                folder_name_are_in_db.append(name)
                folder_dates_are_in_db.append(date)
                folder_paths_are_in_db.append(path)
                folder_size_are_in_db.append(size)
                y += 1 

        Folder_information_not_in_db = set(zip(
        folder_name_not_in_db,
        folder_paths_not_in_db,
        folder_size_not_in_db,
        folder_dates_not_in_db,
        ))
        Folder_information_is_in_db = set(zip(
            folder_size_are_in_db,
            folder_name_are_in_db,
            folder_paths_are_in_db,
        ))
        print(len(folder_name_not_in_db), len(folder_paths_not_in_db), len(folder_size_not_in_db), len(folder_dates_not_in_db))
        print(len(folder_name_are_in_db), len(folder_paths_are_in_db), len(folder_size_are_in_db), len(folder_dates_are_in_db))
        #sql = "INSERT INTO folders  VALUES (%s, %s, %s, %s)"
        mysql_execution.executemany("INSERT INTO folders (folders_Name, Paths, folder_size, When_added)VALUES (%s, %s, %s, %s)", Folder_information_not_in_db)
        sql_login.connection.commit()
        print("adding to data base done...")


        #sql_code = "UPDATE folders SET folder_size = %s WHERE folders_name = %s and Paths = %s"
        mysql_execution.executemany("UPDATE folders SET folder_size = %s WHERE folders_name = %s and Paths = %s", Folder_information_is_in_db)
        sql_login.connection.commit()
        print("Update the database done...")

        uploading_files(file_name,file_size,file_extension,file_paths,Date, new_scan)
    except KeyboardInterrupt:
        exit()
    

def uploading_files(file_name,file_size,file_extension,file_paths,Date, new_scan):
    print("Starting files now ")
    x = 0 
    file_name_not_in_db = []
    file_extension_not_in_db = []
    file_paths_not_in_db = []
    file_size_not_in_db = []

    times = []

    file_name_are_in_db = []
    file_extension_are_in_db = []
    file_paths_are_in_db = []
    file_size_are_in_db = []

    try:
        sql_code = "SELECT folders_Name, Paths FROM folders "
        mysql_execution.execute(sql_code)
        #getting all the files from db in an set 
        all_folders_in_database = mysql_execution.fetchall()
        if all_folders_in_database is None:
            all_folders_in_database = []
        check_set = set(all_folders_in_database)
        #looping though the list
        for name, path, size, extensions in zip(file_name, file_paths,file_size,file_extension):
            print("Name: " +  name)
            times.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            #check if name and path in check_set
            if (name, path ) not in check_set:
                #is_in_database_folders.append("False")
                print(str(x) + name +  ": adding to database")

                file_name_not_in_db.append(name)
                file_extension_not_in_db.append(extensions)
                file_paths_not_in_db.append(path)
                file_size_not_in_db.append(size)

                x += 1 
            else:
                #is_in_database_folders.append("Ture")
                #print(str(y) + ": Update the database")
                file_name_are_in_db.append(name)
                file_extension_are_in_db.append(extensions)
                file_paths_are_in_db.append(path)
                file_size_are_in_db.append(size)
                x += 1 

        Folder_information_not_in_db = set(zip(
        file_name_not_in_db,
        file_paths_not_in_db,
        file_size_not_in_db,
        file_extension_not_in_db,
        ))
        Folder_information_is_in_db = set(zip(
            file_name_are_in_db,
            file_paths_are_in_db,
            file_size_are_in_db,
            file_extension_are_in_db,
        ))
        print(len(file_name_not_in_db), len(file_paths_not_in_db), len(file_size_not_in_db), len(file_extension_not_in_db))
        print(len(file_name_are_in_db), len(file_paths_are_in_db), len(file_size_are_in_db), len(file_extension_are_in_db))
        #sql = "INSERT INTO folders  VALUES (%s, %s, %s, %s)"
        mysql_execution.executemany("INSERT INTO files (file_name, file_paths, file_size, file_extension)VALUES (%s, %s, %s, %s)", Folder_information_not_in_db)
        sql_login.connection.commit()
        print("adding files to data base done...")
        sql_code = "UPDATE files SET file_size = %s, file_extension = %s WHERE file_name = %s and file_paths = %s"
        mysql_execution.executemany(sql_code, Folder_information_is_in_db)
        sql_login.connection.commit()
        print("Update folders the database done...")

    #except mysql.connector.Error as err:
    #    pass
    except KeyboardInterrupt:
        exit()
    timelaps(Date, new_scan)

    
def timelaps(Date, new_scan):
    import time 
    times = time.perf_counter()
    more = time.strftime("%Y-%m-%d %H:%M:%S")
    #new_time = datetime.datetime.strptime(Date, time_format)
    #new_old_time = datetime.datetime.strptime(Datetime, time_format)
    total_time = times - Date; 
    print(total_time  )
    sql_code = "SELECT * FROM scans_times WHERE Type_of_Scans = %s  "
    values = (new_scan )
    mysql_execution.execute(sql_code, values)
    if mysql_execution.fetchone() is None:
        sql_code = "INSERT INTO scans_times (Type_of_Scans, Time, New_time,) VALUES (%s, %s, %s )"
        values = (new_scan, total_time,more )
        mysql_execution.execute(sql_code, values)
        sql_login.connection.commit()
    else:
        # File exists, perform UPDATE
        sql_code = f"UPDATE scans_times SET Type_of_Scans=%s, Time=%s, New_time=%s WHERE Type_of_Scans = '{new_scan[0]}'"
        values = (new_scan[0], total_time,more)
        mysql_execution.execute(sql_code, values)
        sql_login.connection.commit()
    #print()

