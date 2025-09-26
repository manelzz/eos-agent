import json
from datetime import datetime

output_file = "/home/mannel/eos-agent/data/last-check.json"

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(output_file, "w") as f:
    json.dump({ "lastCheck": now }, f, indent=2)

print(f"✅ last-check.json updated: {now}")
