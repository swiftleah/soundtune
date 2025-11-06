import requests
import base64

# --- Spotify API credentials ---
CLIENT_ID = "ba3894ea4f5e4fcb9cd0da47e56bbea8"
CLIENT_SECRET = "be423dccd5de44d98f1e7adc1a7eaafb"

def get_access_token():
    """Fetch a Spotify API access token."""
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {b64_auth_str}"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

    token = response.json()["access_token"]
    return token

def get_genre_seeds(token):
    """Fetch the available genre seeds from Spotify."""
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    genres = response.json()["genres"]
    return genres

if __name__ == "__main__":
    token = get_access_token()
    genres = get_genre_seeds(token)

    print("✅ Spotify Genres:")
    for genre in genres:
        print("-", genre)