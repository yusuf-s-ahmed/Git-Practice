import mysql.connector
from pymongo import MongoClient
from django.conf import settings

def migrate_data(mysql_conn_str, mongo_conn_str):
    # Extract MySQL connection details
    mysql_user = mysql_conn_str['user']
    mysql_password = mysql_conn_str['password']
    mysql_host = mysql_conn_str['host']
    mysql_database = mysql_conn_str['database']

    # Connect to MySQL
    mysql_conn = mysql.connector.connect(
        user=mysql_user,
        password=mysql_password,
        host=mysql_host,
        database=mysql_database
    )
    mysql_cursor = mysql_conn.cursor()

    # Connect to MongoDB
    mongo_client = MongoClient(mongo_conn_str)
    mongo_db = mongo_client.get_database()  # Use the default database from the connection string
    mongo_collection = mongo_db.your_collection_name  # Replace with your collection name

    # Fetch data from MySQL
    mysql_cursor.execute("SELECT * FROM your_table_name")  # Replace with your table name
    rows = mysql_cursor.fetchall()

    # Migrate data to MongoDB
    for row in rows:
        # Convert MySQL row to a dictionary (you can customize this part based on your schema)
        data = {
            "column1": row[0],  # Replace with your actual column names
            "column2": row[1],
            # Add more columns as needed
        }
        # Insert data into MongoDB
        mongo_collection.insert_one(data)

    # Clean up
    mysql_cursor.close()
    mysql_conn.close()
    mongo_client.close()
