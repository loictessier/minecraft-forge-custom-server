import os
import json
import requests


API_KEY = "PASTE_YOUR_API_KEY_HERE"
MODS_DIR = "mods"
MANIFEST_PATH = MODS_DIR + "/manifest.json"

os.makedirs(MODS_DIR, exist_ok=True)

with open(MANIFEST_PATH, "r") as f:
    manifest = json.load(f)

files = manifest["files"]

headers = {
    "Accept": "application/json",
    "x-api-key": API_KEY
}

for mod in files:
    project_id = mod["projectID"]
    file_id = mod["fileID"]

    url = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}/download-url"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        download_url = response.json()["data"]
        print(f"Téléchargement : {download_url}")

        mod_filename = download_url.split("/")[-1]
        dest_path = os.path.join(MODS_DIR, mod_filename)

        with requests.get(download_url, stream=True) as r:
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    else:
        print(f"Échec pour {project_id}:{file_id}")
