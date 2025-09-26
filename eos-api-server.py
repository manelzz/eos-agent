from flask import Flask, request, jsonify, send_from_directory
import json, csv, os
from datetime import datetime

app = Flask(__name__)

# File paths inside the /data folder
DATA_FILE = 'data/eos_data.json'
CSV_FILE = 'data/eos_data.csv'
LAST_CHECK_FILE = 'data/last-check.json'

# Ensure /data exists
os.makedirs('data', exist_ok=True)


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/eos', methods=['GET'])
def get_all():
    return jsonify(load_data())


@app.route('/data/<path:filename>', methods=['GET'])
def serve_data_file(filename):
    allowed_files = ['eos_data.json', 'eos_data.csv', 'last-check.json']
    if filename not in allowed_files:
        return "Unauthorized", 403
    return send_from_directory('data', filename)


@app.route('/eos/csv', methods=['GET'])
def download_csv():
    if not os.path.exists(CSV_FILE):
        return "CSV file not found", 404
    return send_from_directory('data', 'eos_data.csv', as_attachment=True)


@app.route('/eos/update', methods=['POST'])
def update_data():
    try:
        new_data = request.get_json()
        if not isinstance(new_data, list):
            return "Expected a list of records", 400
        save_data(new_data)
        return "Data updated", 200
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)




