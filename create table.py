import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
host = "localhost"            # Adjust if necessary
database = "group_9_ballings_db"  # Replace with your actual database name
user = "postgres"              # Replace with your PostgreSQL username
password = "book"     # Replace with your PostgreSQL password
table_name = "group_9_ballings_datatable"      # Replace with your table name

# Connect to PostgreSQL and create table
try:
    # Connect to the database
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    
    # Define the SQL statement to create the table
    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {table} (
            column1 TEXT,
            column2 INTEGER,
            column3 DATE
        )
    """).format(table=sql.Identifier(table_name))
    
    # Execute the table creation query
    cursor.execute(create_table_query)
    conn.commit()
    print("Table created successfully if it didn’t already exist.")
    
except Exception as e:
    print("Error creating table:", e)
finally:
    # Close the database connection
    if conn:
        cursor.close()
        conn.close()
