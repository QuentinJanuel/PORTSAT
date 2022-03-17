import sys
import requests
from pathlib import Path


def download(file: Path, url: str):
    print(f"Downloading {file.name}...")
    if not file.parent.exists():
        file.parent.mkdir()
    with open(file, "wb") as f:
        response = requests.get(url, stream=True)
        total_length = response\
            .headers\
            .get("content-length")
        if total_length is None:
            f.write(response.content)
            return
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[{}{}]".format(
                "=" * done,
                " " * (50 - done),
            ))
            sys.stdout.flush()
