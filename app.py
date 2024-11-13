from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# PostgreSQL connection details
def get_db_connection():
    return psycopg2.connect(
        host="108.238.181.112",        # Public IP of your PostgreSQL server
        database="group_9_ballings_db", # Database name
        user="postgres",          # PostgreSQL username
        password="book",      # PostgreSQL password
        port=5432                      # Port PostgreSQL is running on (default is 5432)
    )

# Endpoint to fetch data
@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM group_9_ballings_table;")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to add new data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO group_9_ballings_table (salesdate, productid, region, freeship, discount, itemssold)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                new_data['salesdate'],
                new_data['productid'],
                new_data['region'],
                new_data['freeship'],
                new_data['discount'],
                new_data['itemssold']
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app on all network interfaces, allowing remote access
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
