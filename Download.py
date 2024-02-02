import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Song_Recommendation import song_recommendations
import requests

CLIENT_ID = ''
CLIENT_SECRET = ''

def authenticate_spotify():
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def search_and_download_song(sp, query, song_name):
    try:

        results = sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']

            track = sp.track(track_id)

  
            audio_preview_url = track['preview_url']

            if audio_preview_url:

                response = requests.get(audio_preview_url)
                with open(f'Songs/{song_name.replace(" ", "_")}.mp3', 'wb') as f:
                    f.write(response.content)

                print(f"Downloaded: {song_name}")
            else:
                print(f"No audio preview available for: {song_name}")
        else:
            print(f"Could not find track for: {song_name}")

    except Exception as e:
        print(f"Error downloading {song_name}: {e}")

def download_songs_from_spotify():
    song_list = song_recommendations()
    sp = authenticate_spotify()

    for song_name in song_list[:10]:
        query = f"track:{song_name}"

        search_and_download_song(sp, query, song_name)

    return song_list

downloaded_songs = download_songs_from_spotify()

