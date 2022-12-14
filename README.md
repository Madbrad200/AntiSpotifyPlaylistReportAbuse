# AntiSpotifyPlaylistReportAbuse

Are you a Spotify playlister? Is your playlist title/description often wiped by malicious reports, that Spotify refuses to deal with? This script will ensure your playlist will fix itself from any wave of malicious reporting on Spotify.

This is a simple script that will restore your Spotify playlists title and description. The script will check the playlist every 31 seconds (this is adjustable, though I wouldn't reduce it) to see if the title is in-tact. If the title has been removed (or changed), the script will restore the title and description as it is supposed to be.

It does not currently restore the cover art. It is currently optimised to protect one playlist, but that could be edited if necessary.

This script was mainly created for personal use, though I'm certain others will find it useful as well. Please [raise an Issue](https://github.com/Madbrad200/AntiSpotifyPlaylistReportAbuse/issues/new) if you have any questions on how to change, run, or expand the script.

## Installation:

You will need [Python](https://www.python.org/downloads/) installed on your device and accessible on your devices path. I'd recommend Python 3.9+, but it should work on earlier versions.

If you're on windows, I'd recommend setting up a virtual environment first:

```bash
python3 -m venv /path/to/new/virtual/environment
```

Entering your venv [depends on how you are accessing the terminal](https://docs.python.org/3/library/venv.html), in Powershell, simply type:
```bash
/path/to/new/virtual/environment/Scripts/Activate
```

Then, or if you skipped the venv process entirely, you can clone the github:

```bash
git clone https://github.com/Madbrad200/AntiSpotifyPlaylistReportAbuse
```

Done!

Keep in mind for optimal usage, you want this script to be running 24/7. So I'd recommend installing it on a device that will be kept online. I run it in [Tmux](https://github.com/tmux/tmux/wiki) on a Raspberry Pi.

## Setup:
Before using this program, you'll need to get credentials from [Spotify's API](https://developer.spotify.com/documentation/web-api/quick-start/).
An account on Spotify will provide two credentials: 'client id' and 'client secret.'

Modify the following fields:
```python
client_id = 'your_client_id'
client_secret = 'your_client_secret'
```

You will also need to change the `base64_encoded` field. Do to so, [go here](https://www.base64encode.org/) and paste in your client ID and client secret (for example, `thisisafakeid:andafakesecret`). Click `Encode`, then copy the result into the `base64_encoded` field in the python code.

You will also need to enter your playlist details in the `preserved_playlist_name`, `playlist_desc`, and `playlist_code` fields.

**Never publish your ID publicly**

Two prerequisites you'll need installed on your machine are [requests](https://requests.readthedocs.io/en/latest/) and [requests_oauthlib](https://requests-oauthlib.readthedocs.io/en/latest/).

You can easily get both of these from the `pip` repository.
If you aren't yet aware of the beauty of `pip`, go check out [it's website](https://pypi.org/project/pip/).
You're welcome.

Install manually:
```bash
python3 -m pip install requests
python3 -m pip install requests_oauthlib
```

# Usage:

To run the script, enter the following in your terminal:

`python3 antispotifyreports.py`

This may vary depending on your python version and installation (e.g you may need to write `python3.9` instead).

Upon running the script, you will be asked to navigate to a URL in your browser. Following this, you will be redirected to your specified `redirect_uri` (I use `https://localhost/`). You must copy/paste this redirected URL into the terminal (it will have been appended with a code, e.g `https://localhost/?code....`). The script will then run indefinitely. 
