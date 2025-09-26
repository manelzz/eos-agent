from flask import Flask, request, jsonify, send_file, send_from_directory
import json, csv, os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'eos_data.json')
CSV_FILE = os.path.join(BASE_DIR, 'data', 'eos_data.csv')
LAST_CHECK_FILE = os.path.join(BASE_DIR, 'data', 'last-check.json')

os.makedirs('data', exist_ok=True)

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    for entry in data:
        entry["last_checked"] = datetime.utcnow().isoformat() + "Z"
        entry["url_to_announcement"] = get_vendor_url(entry.get("vendor", ""))
        if "model" in entry:
            entry["part_number"] = entry.pop("model")
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    generate_csv(data)

def generate_csv(data):
    if not data:
        return
    with open(CSV_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def get_vendor_url(vendor):
    urls = {
        "Cisco": "https://www.cisco.com/c/en/us/products/eos-eol-policy.html",
        "Fortinet": "https://www.fortinet.com/support/product-life-cycle",
        "Check Point": "https://support.checkpoint.com/results/products/",
        "Bluecoat": "https://techdocs.broadcom.com/"
    }
    return urls.get(vendor, "")

@app.route('/eos', methods=['GET'])
def get_filtered():
    part_number = request.args.get('part-number', '').strip()
    data = load_data()
    if not part_number:
        return jsonify(data)
    filtered = [entry for entry in data if entry.get('part_number', '').lower() == part_number.lower()]
    return jsonify(filtered)

@app.route('/eos/csv', methods=['GET'])
def download_csv():
    if not os.path.exists(CSV_FILE):
        return "CSV file not found", 404
    return send_file(
        CSV_FILE,
        mimetype='text/csv',
        as_attachment=True,
        download_name='eos_data.csv'
    )

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

@app.route('/data/<path:filename>', methods=['GET'])
def serve_data_file(filename):
    allowed_files = ['eos_data.json', 'eos_data.csv', 'last-check.json']
    if filename not in allowed_files:
        return "Unauthorized", 403
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
