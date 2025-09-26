import json
import csv
import os

DATA_FILE = 'data/eos_data.json'
CSV_FILE = 'data/eos_data.csv'

def generate_csv():
    if not os.path.exists(DATA_FILE):
        print("eos_data.json does not exist.")
        exit(1)

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    if not data:
        print("eos_data.json is empty.")
        exit(1)

    with open(CSV_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ {CSV_FILE} generated.")

if __name__ == "__main__":
    generate_csv()


