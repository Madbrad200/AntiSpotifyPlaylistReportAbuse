import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import time
from datetime import datetime

# python3.9 antispotifyreports.py

client_id = "your_client_id"
client_secret = "your_client_secret"

# we need to convert the above into base64 https://www.base64encode.org/ so we can refresh the token
# format is client_id:client_secret, they must be encoded together
base64_encoded = "ENTER YOUR BASE64 ENCODED CLIENT_ID:CLIENT_SECRET HERE"


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
access_token = fetch_token["access_token"]  # expires in 3600 seconds
refresh_token = fetch_token["refresh_token"]  # allows us to refresh the token without re-logging in
# we have now been authenticated

# enter the details of your playlist
preserved_playlist_name = "ENTER YOUR PLAYLIST TITLE HERE"
playlist_desc = "ENTER YOUR PLAYLIST DESCRIPTION HERE"

# note: you need to enter your playlists code
# the code can be found via the playlist url
# e.g https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si=xcPmLVHRQVutEp6HgynU1Q
# in this playlist, the playlist code is 37i9dQZEVXbMDoHDwVN2tF
playlist_code = "ENTER PLAYLIST CODE HERE"

# this function will allow us to refresh our token without re-logging in, after it expires
def refresh_token_func():

    response = requests.post('https://accounts.spotify.com/api/token', 
                            {"grant_type": "refresh_token", 
                             "refresh_token": refresh_token},
                             headers={"Authorization": f"Basic {base64_encoded}"})
    response_data = response.json()
    return response_data["access_token"]

# loop will run indefinitely 
while True:

    # handle the playlist data
    get_playlist = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_code}',
                                headers={'Authorization': f'Bearer {access_token}'})
    playlist_data = get_playlist.json()

    try:
        current_playlist_name = playlist_data["name"]
    except KeyError as e:
        # if the name field is empty (happens when bots abuse reports)
        current_playlist_name = ""

    # enter the title your playlist is /supposed/ to be here
    if current_playlist_name != preserved_playlist_name:

        # restore the removed data
        change_playlist_data = requests.put(f'https://api.spotify.com/v1/playlists/{playlist_code}',
                                            json={
                                                  "name": preserved_playlist_name,
                                                  "description": playlist_desc,
                                                  },
                                            headers={'Authorization': f'Bearer {access_token}'})
        
        # token has expired and we need a new one
        if change_playlist_data.status_code == 401:
            print("Token reset!")
            get_new_token = refresh_token_func()
            
            change_playlist_data = requests.put(f'https://api.spotify.com/v1/playlists/{playlist_code}',
                                                json={
                                                      "name": preserved_playlist_name,
                                                      "description": playlist_desc,
                                                      },
                                                headers={'Authorization': f'Bearer {get_new_token}'})
        elif change_playlist_data.status_code == 429:
            print("You're sending too many requests and are being rate limited! Try changing the 'time.sleep()' (at the end of the while loop) value to a higher number.")
        elif change_playlist_data.status_code == 503:
            print("Service Unavailable: this is a temporary problem with Spotify and should fix itself.")
            time.sleep(60)
        else:
            print(f"({datetime.now().strftime('%H:%M:%S')}){change_playlist_data}\nThe playlist has been successfully restored.")

    else:
        print(f"({datetime.now().strftime('%H:%M:%S')}){playlist_data['name']}\nThe above playlist does not need to be fixed :)")

    time.sleep(31)
