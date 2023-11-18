from re import findall
from urllib.parse import urlparse


def is_track(url) -> bool:
    parsed_url = urlparse(url).path.split("/")
    if parsed_url[-2] == "track":
        return True
    return False


def is_album(url) -> bool:
    parsed_url = urlparse(url).path.split("/")
    if parsed_url[-2] == "album":
        return True
    return False


def is_url_shortener_link(url) -> bool:
    return url.startswith("https://spotify.link")


def get_id_from_url(url) -> str:
    parsed_url = urlparse(url).path.split("/")
    return parsed_url[-1]


def get_urls_from_message(msg) -> str:
    return findall("(?P<url>https?://[^\s]+)", msg)
