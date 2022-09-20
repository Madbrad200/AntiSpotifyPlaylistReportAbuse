import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import time

# python3.9 antispotifyreports.py

client_id = "your_client_id"
client_secret = "your_client_secret"
redirect_uri = "https://localhost/"  # must use https, doesn't have to be a live url
# scopes allow us to edit playlist images, edit playlists that're public/priv
scope = ["ugc-image-upload", "playlist-modify-public", "playlist-modify-private"]
spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

# authorise login
# will need to manully enter terminal and copy/paste url into browser to authorise
authorisation_url = spotify.authorization_url("https://accounts.spotify.com/authorize")
print("Manually enter URL into browser", authorisation_url[0])

# paste in the localhost url you get redirected to
redirect_response = input("\n\nPlease paste the full redirect URL here: ")
auth = HTTPBasicAuth(client_id, client_secret)

fetch_token = spotify.fetch_token("https://accounts.spotify.com/api/token", auth=auth, authorization_response=redirect_response)
access_token = fetch_token["access_token"]
# we have now been authenticated

# loop will run indefinitely 
while True:

    # handle the playlist data
    # note: you need to enter your playlists code
    # the code can be found via the playlist url
    # e.g https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si=xcPmLVHRQVutEp6HgynU1Q
    # in this playlist, the playlist code is 37i9dQZEVXbMDoHDwVN2tF
    get_playlist = requests.get('https://api.spotify.com/v1/playlists/ENTER_PLAYLIST_CODE_HERE',
                                headers={'Authorization': f'Bearer {access_token}'})
    playlist_data = get_playlist.json()

    try:
        playlist_name = playlist_data["name"]
    except KeyError as e:
        # if the name field is empty (happens when bots abuse reports)
        playlist_name = ""

    # enter the title your playlist is /supposed/ to be here
    if playlist_name != "ENTER YOUR PLAYLIST TITLE HERE":

        # restore the removed data
        change_playlist_data = requests.put('https://api.spotify.com/v1/playlists/ENTER_PLAYLIST_CODE_HERE',
                                            json={
                                                  "name": "ENTER YOUR PLAYLIST TITLE HERE",
                                                  "description": "ENTER YOUR PLAYLIST DESCRIPTION HERE",
                                                  },
                                            headers={'Authorization': f'Bearer {access_token}'})
        print(f"{change_playlist_data}\nThe playlist has been successfully restored.")

    else:
        print(f"{playlist_data['name']}\nThe above playlist does not need to be fixed :)")

    time.sleep(31)
