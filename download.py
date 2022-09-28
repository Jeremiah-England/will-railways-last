import os
import requests


DOWNLOAD_DIR = 'downloads'

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

with open('links-to-download.txt', "r") as f:
    links = [line for line in f.read().strip().split("\n") if line and line[0] != "#"]  # Allow '#' comment lines

links_by_file_name = {os.path.basename(link): link for link in links}
assert len(links) == len(links_by_file_name), "There is a collision in file names..."

for file_name, link in links_by_file_name.items():
    file_path = f"{DOWNLOAD_DIR}/{file_name}"
    if os.path.exists(file_path):
        print(f"File already exists at '{file_path}'.")
    else:
        print(f"Downloading '{link}' to '{file_path}'.")
        response = requests.get(link)
        if response.ok:
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            print(f"Download of '{link}' failed: {response}")
