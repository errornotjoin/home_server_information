import mysql.connector

# this code will be change to add yml configuration later
# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="local_server_storage"
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

