from flask import Flask, request
import mysql.connector

# Initialize Flask app
app = Flask(__name__)

# Establish connection to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Himanshu@1234",
    database="mydb"
)
cursor = db.cursor()

# Define route to receive data from generate_function
@app.route('/generate_data', methods=['POST'])
def generate_data():
    # Receive data from the request
    data = request.json
    
    # Extract relevant data from the request
    prompt = data.get('prompt')
    generated_output = data.get('output')
    
    # Insert data into the database
    try:
        insert_query = "INSERT INTO generated_data (prompt, output) VALUES (%s, %s)"
        cursor.execute(insert_query, (prompt, generated_output))
        db.commit()
        return "Data inserted successfully"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
