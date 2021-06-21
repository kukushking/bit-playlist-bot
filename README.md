# bit-playlist-bot

I put all awful gen-z non-music your friends shared in tg into the playlist so you don't have to.

# deployment
1. Make sure Python 3.6+ & AWS CDK are installed.
2. `pip install -r requirements.txt`
3. `cdk bootstrap && cdk deploy --all`
4. Create `spotify/oauth2` secret in Secrets Manager:
```
{
  "client_id": "",
  "client_secret": "",
  "redirect_uri": "http://localhost:9090",
  "scope": "playlist-modify-public"
}
```
5. Create `/spotify/user_id` parameter in Parameter Store.
6. Create `/spotify/playlist_id` parameter in Parameter Store.
7. Test API locally in Python Console or run the lambda to get .cache file with the token. Put the contents of the file into `token_cache` DynamoDB table as DynamoDB JSON string: 
```
{
    "name": "token_info",
    "value": {
        'access_token': {'S': '<TOKEN>'},
        'expires_at': {'N': '<EXPIRES_AT>'},
        'expires_in': {'N': '3600'},
        'refresh_token': {'S': '<REFRESH_TOKEN'},
        'scope': {'S': 'playlist-modify-private playlist-modify-public'},
        'token_type': {'S': 'Bearer'}
    }
}
```
