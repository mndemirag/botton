# Botton GHE proxy

To run this, you need a `Personal Access Token` from GHE, stored in the env var `AUTHTOKEN`.

You can get one from https://ghe.spotify.net/settings/tokens<br>(it needs the `repo - Full control of private repositories` permission) 

## Endpoint overview

**Get all repos:**<br>
`GET http://localhost:5050/repos`

Example response (display names should be max 16 chars):
```json
{
  "repos": [
    {
      "display_name": "support-site",
      "id": "support-site"
    },
    {
      "display_name": "susi-frontend",
      "id": "support-site-frontend"
    }
  ]
}
```

**Get all mergable & open & unlocked & approved PRs for a repo:**<br>
`GET http://localhost:5050/repos/:REPO_NAME/pulls`

Example response:
```json
{
  "repo": "botton",
  "pull_requests": [
    {
      "id": 3,
      "title": "Third PR"
    }
  ]
}
```

**Merge a PR:**<br>
`PUT http://localhost:5050/repos/:REPO_NAME/pulls/:PR_NUMBER/merge`

Example response, success:
```json
{
  "message": "Success: all done"
}
```

Example response, failure (ie clicking button twice):
```json
{
  "message": "-- error --"
}
```
