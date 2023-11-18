import json
import logging
import requests
from typing import Any, Dict, Optional

from .config import Config
from .client import SpotifyClient
from .utils import (
    get_urls_from_message,
    get_id_from_url,
    is_track,
    is_album,
    is_url_shortener_link,
)


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
_spotify = SpotifyClient()
_playlist_id = Config.get_playlist_id()


def lambda_handler(event: Dict, context: Dict):
    _logger.info(f"Event: {event}, context: {context}")

    success_resp = {
        "statusCode": 200
    }

    try:
        message_text = json.loads(event["body"])["message"]["text"]
    except Exception as e:
        _logger.info(f"No message: '{e}'")
        return success_resp

    for url in get_urls_from_message(message_text):
        try:
            # Follow redirect if url shortener link
            if is_url_shortener_link(url):
                url = requests.get(url).url

            if is_track(url):
                track_id: str = get_id_from_url(url)
            elif is_album(url):
                album_id: str = get_id_from_url(url)
                # Get the first track of an album
                track_id: str = _spotify.get_album_track_ids(album_id=album_id)[0]
            else:
                _logger.info(f"Unknown URL '{url}'")
                return success_resp

            _logger.info(f"Track id: {track_id}")

            response: Optional[Any] = _spotify.add_to_playlist(
                Config.get_playlist_id(),
                [track_id],
            )
            _logger.info(f"Add to playlist response: '{response}'")
        except Exception as e:
            _logger.error(f"Failed to process '{url}': '{e}'")
            raise e
    return success_resp
