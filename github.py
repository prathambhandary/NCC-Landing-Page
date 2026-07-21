import os
import json
import base64
import requests

OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")
TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_file(path):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.json()

def update_json(path, data, message):
    file = get_file(path)

    encoded = base64.b64encode(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ).encode("utf-8")
    ).decode()

    payload = {
        "message": message,
        "content": encoded,
        "sha": file["sha"]
    }

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"

    response = requests.put(
        url,
        headers=HEADERS,
        json=payload
    )

    response.raise_for_status()

    return response.json()

def get_json(path):

    file = get_file(path)

    return json.loads(
        base64.b64decode(
            file["content"]
        ).decode("utf-8")
    )