import boto3
import json
from typing import Dict


class Config:
    _ssm = boto3.client("ssm")
    _secrets = boto3.client('secretsmanager')

    @classmethod
    def get_spotify_creds(cls) -> Dict[str, str]:
        return json.loads(cls._secrets.get_secret_value(SecretId="spotify/oauth2")["SecretString"])

    @classmethod
    def get_client_id(cls) -> str:
        return cls.get_spotify_creds()["client_id"]

    @classmethod
    def get_client_secret(cls) -> str:
        return cls.get_spotify_creds()["client_secret"]

    @classmethod
    def get_redirect_uri(cls) -> str:
        return cls.get_spotify_creds()["redirect_uri"]

    @classmethod
    def get_scope(cls) -> str:
        return cls.get_spotify_creds()["scope"]

    @classmethod
    def get_user_id(cls) -> str:
        return cls._ssm.get_parameter(Name="/spotify/user_id")["Parameter"]["Value"]

    @classmethod
    def get_playlist_id(cls) -> str:
        return cls._ssm.get_parameter(Name="/spotify/playlist_id")["Parameter"]["Value"]
