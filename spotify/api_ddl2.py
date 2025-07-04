import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# 개인 정보
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="",
    client_secret=""
))

def sql_escape(value):
    if value is None:
        return ''
    return str(value).replace("'", "''")

# 여러 아티스트 ID 리스트
artist_ids = [
    '3hvinNZRzTLoREmqFiKr1b',
    '6GwM5CHqhWXzG3l5kzRSAS',
    '6OwKE9Ez6ALxpTaKcT5ayv',
    '7IrDIIq3j04exsiF3Z7CPg',
    '5HenzRvMtSrgtvU16XAoby',
]

for artist_id in artist_ids:
    artist = sp.artist(artist_id)

    # 아래쪽 기존 코드를 전부 이 for문 안으로 들여쓰기 하면 됨
    albums = sp.artist_albums(
        artist_id,
        country='KR',
        limit=50,
        include_groups='album,single,appears_on'
    )

    artist_name = sql_escape(artist['name'])

    with open("spotify/DDL/artist_insert.sql", "a", encoding="utf-8") as fa, \
         open("spotify/DDL/album_insert.sql", "a", encoding="utf-8") as fb, \
         open("spotify/DDL/track_insert.sql", "a", encoding="utf-8") as fc:

        # 아티스트 주석
        fa.write(f"\n-- 아티스트: {artist_name}\n")
        fb.write(f"\n-- 아티스트: {artist_name}\n")
        fc.write(f"\n-- 아티스트: {artist_name}\n")

        # 아티스트 INSERT
        profile_image = artist['images'][0]['url'] if artist['images'] else ''
        genres = ', '.join(artist['genres'])
        fa.write(f"INSERT INTO artist (id, name, profile_image, genres) VALUES ('{artist_id}', '{artist_name}', '{profile_image}', '{sql_escape(genres)}');\n")

        for album in albums['items']:
            album_id = album['id']
            # 지연
            time.sleep(0.2)
``            album_detail = sp.album(album_id)
            title = sql_escape(album_detail['name'])
            cover = album_detail['images'][0]['url'] if album_detail['images'] else ''
            release_date = album_detail['release_date']
            genre = ', '.join(album_detail.get('genres', [])) or ''
            label = sql_escape(album_detail.get('label', ''))
            description = ''

            fb.write(f"INSERT INTO album (id, title, cover_image, release_date, genre, label, description, artist_id) VALUES ('{album_id}', '{title}', '{cover}', '{release_date}', '{sql_escape(genre)}', '{label}', '{description}', '{artist_id}');\n")

            tracks = sp.album_tracks(album_id)
            for track in tracks['items']:
                track_id = track['id']
                # 지연
                time.sleep(0.2)
                track_detail = sp.track(track_id)
                title = sql_escape(track['name'])
                duration = track['duration_ms'] // 1000
                streaming_url = track_detail['preview_url']
                mv_url = ''
                track_genre = genre
                popularity = track_detail['popularity']
                track_no = track['track_number']

                fc.write(f"INSERT INTO track (id, title, duration, genre, streaming_url, mv_url, album_id, artist_id, popularity, track_no) "
                         f"VALUES ('{track_id}', '{title}', {duration}, '{sql_escape(track_genre)}', '{streaming_url}', '{mv_url}', '{album_id}', '{artist_id}', {popularity}, {track_no});\n")

        separator = "\n-- ==============================================\n\n"
        fa.write(separator)
        fb.write(separator)
        fc.write(separator)

print("✅ 모든 아티스트 저장 완료!")
