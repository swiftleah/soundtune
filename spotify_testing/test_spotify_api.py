import base64
import os
import requests
from dotenv import load_dotenv
from requests import post, get
import json
import random
from non_english_words import non_english_keywords # non_english_keywords

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# ---- spotify credentials ---- 
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_token():
    client_string = client_id + ":" + client_secret
    auth_bytes = client_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#  ---- auth header ----
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# ---- generate 5 random songs for specified genre ----
def get_random_songs(limit=5):
    token = get_token()
    headers = get_auth_header(token)
    
    all_english_songs = []
    attempts = 0
    max_attempts = 20  # limit attempts
    
    while len(all_english_songs) < limit and attempts < max_attempts:
        random_offset = random.randint(0, 800)
        
        search_url = "https://api.spotify.com/v1/search"
        params = {
            "q": "genre:hiphop",           # Base genre
            "type": "track",
            "market": "US",              # more likely to be english music
            "limit": 25,                
            "offset": random_offset
        }
        
        response = get(search_url, headers=headers, params=params)
        
        if response.status_code != 200:
            attempts += 1
            continue
            
        tracks = response.json()['tracks']['items']
        
        for track in tracks:
            if len(all_english_songs) >= limit:
                break
                
            # skip if duplicate
            if any(track['id'] == existing['id'] for existing in all_english_songs):
                continue
                
            artist_name = track['artists'][0]['name'].lower()
            song_name = track['name'].lower()
            
            # strong English indicators
            is_english = True
            
            # 2. skip songs with obvious non-Latin characters
            if any(ord(char) > 127 for char in track['name'] + artist_name):
                non_latin_count = sum(1 for c in (track['name'] + artist_name) if ord(c) > 127)
                if non_latin_count > 8:  # reject heavy CJK/Korean/Arabic
                    is_english = False
            
            # 3. block songs with known non-English words/phrases
            for keyword in non_english_keywords:
                if keyword in song_name or keyword in artist_name:
                    is_english = False
                    break
            
            # 4. prefer tracks popular in English-speaking markets
            if track['popularity'] < 30:  # low popularity often regional non-English
                continue
                
            if is_english:
                song = {
                    "id": track['id'],
                    "name": track['name'],
                    "artist": track['artists'][0]['name'],
                    "album": track['album']['name'],
                    "release_year": track['album']['release_date'][:4],
                    "popularity": track['popularity'],
                    "spotify_url": track['external_urls']['spotify'],
                    "preview_url": track.get('preview_url')
                }
                all_english_songs.append(song)
        
        attempts += 1
    
    return all_english_songs[:limit]


if __name__ == "__main__":
    songs = get_random_songs(5)
    if songs:
        print("Here are 5 random pop songs:\n")
        for i, song in enumerate(songs, 1):
            print(f"{i}. {song['name']} by {song['artist']} ({song['release_year']})")
            print(f"   Album: {song['album']} | Popularity: {song['popularity']}")
            print(f"   Listen: {song['spotify_url']}\n")