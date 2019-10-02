"""A module for interactions with the Steam Workshop."""

from os import rename
from environs import Env
from requests import get, post
from lzma import LZMADecompressor
from json import dumps, JSONDecodeError

env = Env()
env.read_env()


def api_url(service: str = "IPublishedFileService",
            function: str = "QueryFiles",
            version: str = "v1") -> str:
    """
    Builds a steam web API url.
    :param service: The steam service to attach to.
    :param function: The function to call.
    :param version: The API version.
    :return: The built URL.
    """
    return "https://api.steampowered.com/%s/%s/%s/" % (
        service, function, version
    )


with env.prefixed("STEAM_"):
    key = env.str("API_KEY")
    blacklist = set(env.list("BLACKLIST"))


def search(text="", app=4000, perpage=20, cursor="*"):
    """
    Search the workshop with a given search text and app,
    returning X results per page, after cursor.
    :param text: The text to search for.
    :param app: The AppID to search for.
    :param perpage: Number of results per page, defaults to 20.
    :param cursor: The active cursor. Returned from results.
    :return: Iterator
    """
    while cursor:
        print("Cursor: {}".format(cursor))
        resp = get(
            url=api_url(),
            params={
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
        except JSONDecodeError:
            print(resp.headers)
            print(resp.text)
            exit(1)

        if 'publishedfiledetails' not in resp:
            return

        files = [x for x in resp['publishedfiledetails'] if x['result'] == 1]
        for f in files:
            yield f

        cursor = resp['next_cursor']


def query(file):
    """
    Query a single file from the workshop.
    :param file: string The FileID to query.
    :return: object
    """
    resp = post(
        url=api_url('ISteamRemoteStorage', 'GetPublishedFileDetails'),
        data={
            "itemcount": 1,
            "publishedfileids[0]": file
        })

    try:
        resp = resp.json()['response']
    except JSONDecodeError:
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
    """
    Fetch a user's steam summary by 64bit steamid.
    :param sid:
    :return:
    """
    resp = get(
        url=api_url('ISteamUser', 'GetPlayerSummaries', 'v2'),
        params={
            "key": key,
            "steamids": sid
        })

    try:
        resp = resp.json()['response']
    except JSONDecodeError:
        print(resp.headers)
        print(resp.text)
        exit()

    return resp['players'][0]['personaname']
