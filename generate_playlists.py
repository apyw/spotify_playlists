import json

import requests

from exceptions import ResponseException
from secret import spotify_token, spotify_user_id
from track import Track


class GeneratePlaylist:
    def recent_tracks(self):
        query = "https://api.spotify.com/v1/me/player/recently-played?limit=10"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["items"]

        ids = [(track["track"]["id"]) for track in songs]

        return ids

    def recommended_tracks(self):
        seed_tracks = self.recent_tracks()
        seed_tracks = seed_tracks[0]
        query = "https://api.spotify.com/v1/recommendations?limit=10&seed_tracks={}".format(
            seed_tracks
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]

        ids = [(track["album"]["id"]) for track in songs]
        return ids

    def create_playlist(self):
        request_body = json.dumps({
            "name": "Test",
            "description": "Generated Playlist",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()

        # playlist id
        return response_json["id"]

    def add_to_playlist(self):
        # collect all of uri
        uris = [f"spotify:track:{track}" for track in self.recommended_tracks()]

        # create a new playlist
        playlist_id = self.create_playlist()

        # add all songs into new playlist
        request_body = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    cp = GeneratePlaylist()
    cp.add_to_playlist()
