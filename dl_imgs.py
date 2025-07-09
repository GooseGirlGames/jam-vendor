#!/usr/bin/env python3

import json
from hashlib import sha256


def download(im):
    ext = im.split(".")[-1]
    filename = sha256(im.encode()).hexdigest()[:32] + "." + ext
    print(f"curl -Lo img/{filename} '{im}'")


with open("./games.json", "r") as f:
    games = json.loads(f.read())
    for gamename, data in games.items():
        for im in data["images"]:
            if im.startswith("http"):
                download(im)
