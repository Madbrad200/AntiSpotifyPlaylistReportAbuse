import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import time
from datetime import datetime

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
# we have now been authenticated

# enter the details of your playlist
preserved_playlist_name = "ENTER YOUR PLAYLIST TITLE HERE"
playlist_desc = "ENTER YOUR PLAYLIST DESCRIPTION HERE"

# note: you need to enter your playlists code
# the code can be found via the playlist url
# e.g https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si=xcPmLVHRQVutEp6HgynU1Q
# in this playlist, the playlist code is 37i9dQZEVXbMDoHDwVN2tF
playlist_code = "ENTER PLAYLIST CODE HERE"

# list of our tokens
# we will choose to use the last items in the list
access_tokens = [fetch_token["access_token"]]
refresh_tokens = [fetch_token["refresh_token"]]

# this function will allow us to refresh our token without re-logging in, after it expires
def refresh_token_func(token):

    while True:

        response = requests.post('https://accounts.spotify.com/api/token', 
                                 {"grant_type": "refresh_token", 
                                  "refresh_token": token},
                                 headers={"Authorization": f"Basic {base64_encoded}"})
        try:
            response_data = response.json()
        except Exception as e:
            print(f"{e}, {response_data}")
        try: 
            access_tokens.append(response_data["access_token"])
            print("Access Token refreshed!")
            if "refresh_token" in response_data.keys():
                refresh_tokens.append(response_data["refresh_token"])
                print("Refresh Token refreshed!")
            break
        except KeyError as e:
            # in-case there is a temporary error with Spotify
            time.sleep(31)
            print(f"{e}\n{response_data}")

count = 0
# loop will run indefinitely 
while True:
    
    # every 3600 seconds or so, we need to refresh the token
    # with time.sleep set at 31s, this roughly equals 116 complete loops
    if count == 116:
        refresh_token_func(refresh_tokens[-1])
        count -= 0  # reset count to 0

    # handle the playlist data
    get_playlist = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_code}',
                                headers={'Authorization': f'Bearer {access_tokens[-1]}'})
    playlist_data = get_playlist.json()

    try:
        current_playlist_name = playlist_data["name"]
    except KeyError as e:
        # if the name field is empty (happens when bots abuse reports)
        current_playlist_name = ""

    if current_playlist_name != preserved_playlist_name:

        # restore the removed data
        change_playlist_data = requests.put(f'https://api.spotify.com/v1/playlists/{playlist_code}',
                                            json={
                                                  "name": preserved_playlist_name,
                                                  "description": playlist_desc,
                                                  },
                                            headers={'Authorization': f'Bearer {access_tokens[-1]}'})
       
        if change_playlist_data.status_code == 429:
            print("You're sending too many requests and are being rate limited! Try changing the 'time.sleep()' (at the end of the while loop) value to a higher number.")
        elif change_playlist_data.status_code == 503:
            print("Service Unavailable: this is a temporary problem with Spotify and should fix itself.")
            time.sleep(60)
        else:
            print(f"({datetime.now().strftime('%H:%M:%S')}){change_playlist_data}\nThe playlist has been successfully restored.")

    else:
        print(f"({datetime.now().strftime('%H:%M:%S')}){playlist_data['name']}\nThe above playlist does not need to be fixed :)")

    time.sleep(31)
