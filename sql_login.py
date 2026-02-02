import mysql.connector

# Establish a connection to the MySQL database
#MUST CHANGE CREDENTIALS BELOW TO YOUR OWN MYSQL SERVER CREDENTIALS
#MUST HAVE SAME SQL TABLES AS IN THE DATABASE SCHEMA
#AS IT WILL NOT WORK WITHOUT THEM
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="local_server_storage"
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

