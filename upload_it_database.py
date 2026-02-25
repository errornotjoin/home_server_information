#import sql_login
import sql_login
import mysql.connector
import datetime


mysql_execution = sql_login.connection.cursor(buffered=True)

time = datetime.datetime.now()
more = time.strftime("%Y-%m-%d %H:%M:%S")

def upload_drives_information(drive_names, total_sizes, used_spaces, free_spaces,driveces_last_check, folder_name,folder_dates,folder_size,folder_paths,file_name,file_size,file_extension,file_paths):
    try: 
        for i in range(len(drive_names)):
            more = time.strftime("%Y-%m-%d %H:%M:%S")
            sql_Code = "SELECT drivecs_Name FROM drivces_ WHERE drivecs_Name = %s"
            mysql_execution.execute(sql_Code, (drive_names[i],))
            if mysql_execution.fetchone() is None and drive_names[i] != "":
                # Drive does not exist, perform INSERT
                sql_Code = "INSERT INTO drivces_ (drivecs_Name, drivces_size, drive_Used, drivces_free_space,last_check, When_added) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (drive_names[i], total_sizes[i], used_spaces[i], free_spaces[i], driveces_last_check[i], more)
                mysql_execution.execute(sql_Code, values)
                sql_login.connection.commit()
            elif drive_names[i] != "":
                # Drive exists, perform UPDATE
                sql_Code = "UPDATE drivces_ SET drivces_size = %s, drive_Used = %s, drivces_free_space = %s, last_check = %s WHERE drivecs_Name = %s"
                values = (total_sizes[i], used_spaces[i], free_spaces[i], driveces_last_check[i], drive_names[i])
                mysql_execution.execute(sql_Code, values)
                sql_login.connection.commit()
            else:
                continue
    except mysql.connector.Error as err:
        pass
    except KeyboardInterrupt:
        exit()
    uploading_folder(folder_name,folder_dates,folder_size,folder_paths,file_name,file_size,file_extension,file_paths)

def uploading_folder(folder_name,folder_dates,folder_size,folder_paths,file_name,file_size,file_extension,file_paths):
    try:
        for i in range(len(folder_name)):
            more = time.strftime("%Y-%m-%d %H:%M:%S")
            sql_code = "SELECT folders_Name FROM folders WHERE folders_Name = %s AND Paths = %s"
            mysql_execution.execute(sql_code, (folder_name[i], folder_paths[i]))
            if mysql_execution.fetchone() is None:
                sql_code = "INSERT INTO folders (folders_Name,  folder_size, Modified_dates, Paths, When_added) VALUES (%s, %s, %s, %s, %s)"
                values = (folder_name[i], folder_size[i], folder_dates[i], folder_paths[i], more)
                mysql_execution.execute(sql_code, values)
                sql_login.connection.commit()
            else:
                # Folder exists, perform UPDATE
                sql_code = "UPDATE folders SET folders_Name=%s, folder_size=%s, Modified_dates=%s, When_added=%s WHERE folders_Name = %s AND Paths = %s"
                values = (folder_name[i], folder_size[i], folder_dates[i], more, folder_name[i], folder_paths[i])
                mysql_execution.execute(sql_code, values)
                sql_login.connection.commit()
            print( "Uploaded/Updated folder: " + folder_name[i] + " at path: " + folder_paths[i],  flush=True)
    except mysql.connector.Error as err:
        pass
    except KeyboardInterrupt:
        exit()
    uploading_files(file_name,file_size,file_extension,file_paths,)

def uploading_files(file_name,file_size,file_extension,file_paths,):
    try:
        for i in range(len(file_name)):
            more = time.strftime("%Y-%m-%d %H:%M:%S")
            sql_code = "SELECT file_name FROM files WHERE file_name = %s AND file_paths = %s"
            mysql_execution.execute(sql_code, (file_name[i], file_paths[i]))
            if mysql_execution.fetchone() is None:
                sql_code = "INSERT INTO files (file_name, file_size, file_extension, file_paths, When_updated) VALUES (%s, %s, %s, %s, %s)"
                values = (file_name[i], file_size[i], file_extension[i], file_paths[i], more)
                mysql_execution.execute(sql_code, values)
                sql_login.connection.commit()
            else:
                # File exists, perform UPDATE
                sql_code = "UPDATE files SET file_size=%s, file_extension=%s, When_updated=%s WHERE file_name = %s AND file_paths = %s"
                values = (file_size[i], file_extension[i], more, file_name[i], file_paths[i])
                mysql_execution.execute(sql_code, values)
                sql_login.connection.commit()
            print( "Uploaded/Updated file: " + file_name[i] + " at path: " + file_paths[i],  flush=True)
    except mysql.connector.Error as err:
        pass
    except KeyboardInterrupt:
        exit()
    exit()