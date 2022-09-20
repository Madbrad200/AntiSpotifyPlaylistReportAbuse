# AntiSpotifyPlaylistReportAbuse

Are you a Spotify playlister? Is your playlist title/description often wiped by malicious reports, that Spotify refuses to deal with? This script will ensure your playlist will fix itself from any wave of malicious reporting on Spotify.

This is a simple script that will restore your Spotify playlists title and description. The script will check the playlist every 31 seconds (this is adjustable, though I wouldn't reduce it) to see if the title is in-tact. If the title has been removed (or changed), the script will restore the title as it is supposed to be.

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

Modify the following two fields:
```python
client_id = 'your_client_id'
client_secret = 'your_client_secret'
```

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
