import os
import json
import requests


def load_client_only_mod_ids(path="client_only_mods.txt"):
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        return set(int(line.strip()) for line in f if line.strip().isdigit())


API_KEY = os.environ.get("CURSEFORGE_API_KEY")
if not API_KEY:
    print("Missing Curseforge API key! Define CURSEFORGE_API_KEY.")
    exit(1)

MODS_DIR = "mods"
MANIFEST_PATH = os.path.join(MODS_DIR, "manifest.json")

client_only_ids = load_client_only_mod_ids()

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

    if project_id in client_only_ids:
        print(f"Skipping client-only mod {project_id}")
        continue

    info_url = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}"
    info_response = requests.get(info_url, headers=headers)
    if info_response.status_code == 200:
        file_info = info_response.json()["data"]
        game_versions = file_info["gameVersions"]

        if "Forge" not in game_versions:
            print(f"Skipping non-mod file {project_id}:{file_id} (game_versions {game_versions})")
            continue
    else:
        print(f"Failed to fetch file info for {project_id}:{file_id}")
        continue

    url = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}/download-url"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        download_url = response.json()["data"]
        print(f"Downloading: {download_url}")

        mod_filename = download_url.split("/")[-1]
        dest_path = os.path.join(MODS_DIR, mod_filename)

        with requests.get(download_url, stream=True) as r:
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    else:
        print(f"Failure for {project_id}:{file_id}")
