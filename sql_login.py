import mysql.connector
import yaml
# this code will be change to add yml configuration later
# Establish a connection to the MySQL database
with open("yml_files/sql_server_information.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    sql_info = cfg['sql_information']
    connection = mysql.connector.connect(
        host=sql_info['Server'],
        user=sql_info['UserName'],
        password=sql_info['Password'],
        database=sql_info['Database']
    )

# Create a cursor object to interact with the database
cursor = connection.cursor()

