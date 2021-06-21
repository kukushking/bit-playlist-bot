import json
import logging
from typing import Any, Dict, Optional

from .config import Config
from .client import SpotifyClient
from .utils import (
    get_urls_from_message,
    get_id_from_url,
    is_track,
    is_album,
)


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
_spotify = SpotifyClient()
_playlist_id = Config.get_playlist_id()


def lambda_handler(event: Dict, context: Dict):
    _logger.info(f"Event: {event}, context: {context}")

    for url in get_urls_from_message(json.loads(event["body"])["message"]["text"]):
        try:
            if is_track(url):
                track_id: str = get_id_from_url(url)
            elif is_album(url):
                album_id: str = get_id_from_url(url)
                _logger.info(f"Album id: {album_id}")
                track_id: str = _spotify.get_album_track_ids(album_id=album_id)[0]
            _logger.info(f"Track id: {track_id}")

            response: Optional[Any] = _spotify.add_to_playlist(
                Config.get_playlist_id(),
                [track_id],
            )
            _logger.info(f"Response: {response}")
        except Exception as e:
            _logger.error(f"Error processing '{url}': '{e}'")
            raise e

    return {
        "statusCode": 200,
    }
