import datetime as dt
import requests
import pandas as pd
import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
host = "localhost"            
database = "group_9_ballings_db"  
user = "postgres"              
password = "book"     
table_name = "group_9_ballings_table"  # Updated to correct table name

# Logging the execution time
with open('C:\\Users\\Noah\\Desktop\\BALLINGS\\groupassignment.txt', 'a') as file_object:
    file_object.write('Executed on ' + str(dt.datetime.now()) + '\n')

# Fetch the script from the URL and execute it
url = 'http://ballings.co/data.py'
exec(requests.get(url).content)

# Convert salesdate column to date format compatible with PostgreSQL if needed
data['salesdate'] = pd.to_datetime(data['salesdate'], format='%m/%d/%Y').dt.date

# Connect to PostgreSQL and insert data
try:
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    
    # Insert data into the PostgreSQL table
    insert_query = sql.SQL("""
        INSERT INTO {table} (salesdate, productid, region, freeship, discount, itemssold)
        VALUES (%s, %s, %s, %s, %s, %s)
    """).format(table=sql.Identifier(table_name))
    
    for _, row in data.iterrows():
        cursor.execute(insert_query, (
            row['salesdate'],
            row['productid'],
            row['region'],
            row['freeship'],
            row['discount'],
            row['itemssold']
        ))

    conn.commit()
    print("Data from URL loaded into PostgreSQL successfully.")
    
except Exception as e:
    print("Error:", e)
finally:
    if conn:
        cursor.close()
        conn.close()
