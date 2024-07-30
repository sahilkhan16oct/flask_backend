from flask import Flask, request, jsonify
import json
import subprocess
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Hardcoded credentials for simplicity (in production, use a database and hashing)
USERNAME = "admin"
PASSWORD = "12345"

@app.route('/')
def home():
    return "Hello, Vercel!"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == USERNAME and data['password'] == PASSWORD:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failure'}), 401

# Define the paths based on your directory structure
BASE_DIR = 'C:\\Users\\sahil\\Desktop\\backend1'
INPUT_FILE = os.path.join(BASE_DIR, 'input.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'output.gds')
CONVERSION_SCRIPT = os.path.join(BASE_DIR, 'jsonToGds.py')

def convert_json_to_gds(json_data):
    # Save the received JSON data to a file
    with open(INPUT_FILE, 'w') as f:
        json.dump(json_data, f)

    # Execute the jsonToGds.py script with the input and output file paths
    process = subprocess.run(['python', CONVERSION_SCRIPT, INPUT_FILE, OUTPUT_FILE], capture_output=True, text=True)
    
    # Check if the process was successful
    if process.returncode != 0:
        return None, process.stderr

    # Read the generated GDS data from the output file
    with open(OUTPUT_FILE, 'rb') as f:
        gds_data = f.read()

    return gds_data, None

@app.route('/convert', methods=['POST'])
def convert():
    # Ensure the request content type is JSON
    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected"}), 400
    
    # Get the JSON data from the request
    json_data = request.get_json()
    print(json_data)


    # Convert the JSON data to GDS format
    gds_data, error = convert_json_to_gds(json_data)

    # If there was an error during conversion, return the error message
    if error:
        return jsonify({"error": error}), 500
    
    # Return the GDS data in a JSON response
    return jsonify({"gds_data": gds_data.decode('latin1')})


