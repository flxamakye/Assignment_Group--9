import psycopg2
from psycopg2 import sql
import pandas as pd

# PostgreSQL connection details
host = "localhost"            
database = "group_9_ballings_db"  
user = "postgres"              
password = "book"     
table_name = "group_9_ballings_table"      

# Define the path to your CSV file
csv_file_path = 'C:\\Users\\Noah\\Desktop\\BALLINGS\\sales_data.csv'

# Connect to PostgreSQL and create the table if it doesn’t exist
try:
    # Connect to the database
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    
    # Define the SQL statement to create the table
    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {table} (
            salesdate DATE,
            productid INTEGER,
            region TEXT,
            freeship INTEGER,
            discount FLOAT,
            itemssold INTEGER
        )
    """).format(table=sql.Identifier(table_name))
    
    # Execute the table creation query
    cursor.execute(create_table_query)
    conn.commit()
    print("Table created successfully if it didn’t already exist.")
    
    # Load CSV data
    data = pd.read_csv(csv_file_path)
    
    # Convert salesdate column to a date format recognized by PostgreSQL
    data['salesdate'] = pd.to_datetime(data['salesdate'], format='%m/%d/%Y').dt.date
    
    # Insert CSV data into PostgreSQL table
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
    print("Data from CSV loaded into PostgreSQL successfully.")
    
except Exception as e:
    print("Error:", e)
finally:
    # Close the database connection
    if conn:
        cursor.close()
        conn.close()
