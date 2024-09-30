# migration_tool/views.py

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import mysql.connector
from pymongo import MongoClient

# Index view to render the homepage
def index(request):
    return render(request, 'migration_tool/index.html')  # Update the template path accordingly

@api_view(['POST'])
def migrate_data(request):
    # Retrieve parameters from request data
    mysql_conn_str = request.data.get('mysql_conn')
    mongo_conn_str = request.data.get('mongo_conn')
    mysql_table = request.data.get('mysql_table')  # Table name to migrate from
    mongo_collection_name = request.data.get('mongo_collection')  # Collection name to migrate to
    mongo_db_name = request.data.get('mongo_db')  # MongoDB database name

    # Validate inputs
    if not all([mysql_conn_str, mongo_conn_str, mysql_table, mongo_collection_name, mongo_db_name]):
        return Response({"error": "All fields are required: mysql_conn, mongo_conn, mysql_table, mongo_collection, and mongo_db."}, status=400)

    try:
        # Connect to MySQL
        mysql_conn = mysql.connector.connect(**mysql_conn_str)  # Use unpacking for connection details
        cursor = mysql_conn.cursor()

        # Execute a query to fetch data from the specified MySQL table
        cursor.execute(f"SELECT * FROM {mysql_table}")
        rows = cursor.fetchall()

        # Get column names dynamically
        column_names = [desc[0] for desc in cursor.description]

        # Connect to MongoDB
        mongo_client = MongoClient(mongo_conn_str)
        mongo_db = mongo_client[mongo_db_name]  # Use the specified MongoDB database name
        mongo_collection = mongo_db[mongo_collection_name]  # Use the specified collection name

        # Prepare bulk insert for better performance
        documents = []
        for row in rows:
            document = {column_names[i]: row[i] for i in range(len(row))}
            documents.append(document)

        # Insert data into MongoDB using bulk insert
        if documents:  # Only insert if there are documents
            mongo_collection.insert_many(documents)

        # Clean up
        cursor.close()
        mysql_conn.close()
        mongo_client.close()

        return Response({"message": "Migration completed successfully."}, status=200)

    except mysql.connector.Error as mysql_err:
        return Response({"error": f"MySQL error: {str(mysql_err)}"}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
