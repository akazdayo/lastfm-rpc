from pypresence import Presence
import httpx
from pprint import pprint
import time
import os


APIKEY = os.environ.get('LASTFM_APIKEY')
client_id = os.environ.get('DISCORD_CLIENTID')

old_track = None
RPC = Presence(client_id, pipe=0)  # Initialize the client class
RPC.connect()  # Start the handshake loop


def get_artist_image(track):
    response = httpx.get(
        f"http://ws.audioscrobbler.com/2.0/?method=artist.getInfo&api_key={APIKEY}&artist={track['artist']['#text']}&format=json")
    data = response.json()
    pprint(data)
    return data['artist']['image'][2]['#text']


while True:
    response = httpx.get(
        f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=akazdayo&api_key={APIKEY}&format=json")
    data = response.json()
    recent_tracks = data['recenttracks']['track']
    if recent_tracks:
        now_playing = recent_tracks[0]
        if '@attr' in now_playing and 'nowplaying' in now_playing['@attr'] and now_playing != old_track:
            # アーティストの画像取得できなくて泣いた笑
            # artist_image = get_artist_image(now_playing)
            old_track = now_playing
            message = f"{now_playing['name']} by {
                now_playing['artist']['#text']}"
            start = time.time()
            print(message)
            # Set the presence
            print(RPC.update(
                large_image=now_playing['image'][2]['#text'], details="Now playing:", state=message, start=start))

    else:
        print("No recent tracks found.")
        break
    time.sleep(10)
