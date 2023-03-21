#!/usr/bin/python3
import sys
import requests
import zipfile
import io

if (len(sys.argv) < 5):
    print("Usage: download-artifact.py <owner> <repo> <token> <n of artifacts>")
    exit()

owner, repos, token, nartifacts = [sys.argv[i] for i in range(1, 5)]

print("Requesting artifacts")
json_response = requests.get(f"https://api.github.com/repos/{owner}/{repos}/actions/artifacts",
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }).json()

for i in range(int(nartifacts)):
    artifact_url =  json_response["artifacts"][i]["archive_download_url"]
    artifact_name = json_response["artifacts"][i]["name"]

    print(f"Downloading {artifact_name}.zip from {artifact_url}")
    response = requests.get(artifact_url, 
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28"
            }, 
            allow_redirects=True)

    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall()
    z.close()

