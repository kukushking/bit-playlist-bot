import boto3
import logging
import spotipy
from spotipy.oauth2 import SpotifyPKCE, CacheHandler
from typing import Any, Optional, List

from .config import Config


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


class DynamoDBTokenCacheHandler(CacheHandler):

    def __init__(self):
        self._token_info = boto3\
            .resource("dynamodb")\
            .Table("token_info")

    def get_cached_token(self):
        return self._token_info.get_item(
            Key={
                "name": "token_info"
            },
            AttributesToGet=[
                "value"
            ]
        )["Item"]["value"]

    def save_token_to_cache(self, token_info):
        self._token_info.put_item(
            Item={
                "name": "token_info",
                "value": token_info
            }
        )


class SpotifyClient:

    def __init__(self) -> None:
        self._client = spotipy.Spotify(
            auth_manager=SpotifyPKCE(
                client_id=Config.get_client_id(),
                redirect_uri=Config.get_redirect_uri(),
                scope=Config.get_scope(),
                open_browser=False,
                cache_handler=DynamoDBTokenCacheHandler(),
            ),
        )

    def create_playlist(self, name: str, description: str) -> Optional[Any]:
        return self._client.user_playlist_create(
            user=Config.get_user_id(),
            name=name,
            public=True,
            collaborative=False,
            description=description,
        )

    def add_to_playlist(self, playlist_id: str, track_ids: List[str]) -> Optional[Any]:
        return self._client.playlist_add_items(
            playlist_id=playlist_id,
            items=track_ids,
        )

    def get_album_track_ids(self, album_id: str) -> List[str]:
        return [item["id"] for item in self._client.album_tracks(
            album_id=album_id,
        )["items"]]
