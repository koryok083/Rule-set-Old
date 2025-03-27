import requests
import json
import os

# URL geosite.dat dari repo MetaCubeX
GEO_RULES_URL = "https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geosite.dat"

# Buat folder rules jika belum ada
os.makedirs("rules", exist_ok=True)

# Unduh file geosite.dat
print("Mengunduh geosite.dat...")
response = requests.get(GEO_RULES_URL)
if response.status_code != 200:
    print("Gagal mengunduh geosite.dat")
    exit(1)

geosite_data = response.text.splitlines()

# Load kategori dari JSON
with open("categories.json", "r") as f:
    categories = json.load(f)

# Proses filter per kategori
for category, keywords in categories.items():
    filtered_lines = [line for line in geosite_data if any(kw.lower() in line.lower() for kw in keywords)]
    
    if filtered_lines:
        with open(f"rules/{category}.yaml", "w") as f:
            f.write("\n".join(filtered_lines))
        print(f"✅ Rule-set '{category}' berhasil dibuat dengan {len(filtered_lines)} entri.")
    else:
        print(f"⚠️ Tidak ada data yang cocok untuk kategori '{category}'.")

print("Selesai!")
