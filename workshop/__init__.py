"""A module for interactions with the Steam Workshop."""

from os import rename
from environs import Env
from requests import get, post
from lzma import LZMADecompressor
from json import dumps

env = Env()
env.read_env()

with env.prefixed("STEAM_"):
    key = env.str("API_KEY")
    blacklist = set(env.list("BLACKLIST"))


def search(text="", app=4000, perpage=20, cursor="*"):
    while cursor:
        print("Cursor: {}".format(cursor))
        resp = get(url="https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/", params={
            "key": key,
            "input_json": dumps({
                "cursor": cursor,
                "numperpage": perpage,
                "creator_appid": app,
                "appid": app,
                "search_text": text,
                "return_children": True,
                "return_short_description": True,
                "requiredtags": "Addon",
                "required_flags": "Addon",
                "ids_only": False,
                "return_metadata": True
            })
        })

        try:
            resp = resp.json()['response']
        except Exception:
            print(resp.headers)
            print(resp.text)
            exit()

        if not 'publishedfiledetails' in resp:
            return

        files = [x for x in resp['publishedfiledetails'] if x['result'] == 1]
        for f in files:
            yield f

        cursor = resp['next_cursor']


def query(file):
    resp = post(url="https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data={
        "itemcount": 1,
        "publishedfileids[0]": file
    })

    try:
        resp = resp.json()['response']
    except Exception:
        print(resp.headers)
        print(resp.text)
        exit(1)

    return resp['publishedfiledetails'][0]


def download(url, fi):
    d = LZMADecompressor()

    with get(url) as r:
        with open(fi + ".tmp", 'wb') as f:
            for chunk in r.iter_content(128):
                if not d.eof:
                    f.write(d.decompress(chunk))
    rename(fi + ".tmp", fi)


def author(sid):
    resp = get(url="https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/", params={
        "key": key,
        "steamids": sid
    })

    try:
        resp = resp.json()['response']
    except Exception:
        print(resp.headers)
        print(resp.text)
        exit()

    return resp['players'][0]['personaname']
