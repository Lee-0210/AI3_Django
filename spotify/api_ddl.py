import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# .env에서 환경변수 불러오기
load_dotenv()

# 개인 정보
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="SPOTIFY_CLIENT_ID",
    client_secret="SPOTIFY_CLIENT_SECRET"
))

# 아티스트 아이디
artist_id = "6qqNVTkY8uBg9cP3Jd7DAH"
artist = sp.artist(artist_id)

albums = sp.artist_albums(
    artist_id,
    country='KR',
    limit=50,
    include_groups='album,single,appears_on'  # 컴필레이션 제외
)

def sql_escape(value):
    if value is None:
        return ''
    return str(value).replace("'", "''")



# 아티스트명
artist_name = sql_escape(artist['name'])

with open("spotify/DDL/artist_insert.sql", "a", encoding="utf-8") as fa, \
     open("spotify/DDL/album_insert.sql", "a", encoding="utf-8") as fb, \
     open("spotify/DDL/track_insert.sql", "a", encoding="utf-8") as fc:

    # 아티스트 구분 주석 + 빈 줄
    fa.write(f"\n-- 아티스트: {artist_name}\n")
    fb.write(f"\n-- 아티스트: {artist_name}\n")
    fc.write(f"\n-- 아티스트: {artist_name}\n")

    # 아티스트
    artist_id = artist['id']
    profile_image = artist['images'][0]['url'] if artist['images'] else ''
    genres = ', '.join(artist['genres'])
    fa.write(f"INSERT INTO artist (id, name, profile_image, genres) VALUES ('{artist_id}', '{artist_name}', '{profile_image}', '{sql_escape(genres)}');\n")

    for album in albums['items']:
        album_id = album['id']
        album_detail = sp.album(album_id)
        title = sql_escape(album_detail['name'])
        cover = album_detail['images'][0]['url'] if album_detail['images'] else ''
        release_date = album_detail['release_date']
        genre = ', '.join(album_detail.get('genres', [])) or ''
        label = sql_escape(album_detail.get('label', ''))
        description = ''  # 스포티파이에는 description 없음

        fb.write(f"INSERT INTO album (id, title, cover_image, release_date, genre, label, description, artist_id) VALUES ('{album_id}', '{title}', '{cover}', '{release_date}', '{sql_escape(genre)}', '{label}', '{description}', '{artist_id}');\n")

        tracks = sp.album_tracks(album_id)
        for track in tracks['items']:
            track_id = track['id']
            track_detail = sp.track(track_id)  # 별도 호출
            title = sql_escape(track['name'])
            duration = track['duration_ms'] // 1000
            streaming_url = track_detail['preview_url']
            mv_url = ''  # 뮤직비디오 URL은 제공 안 됨
            track_genre = genre  # 앨범 장르를 그대로 사용
            popularity = track_detail['popularity']
            track_no = track['track_number']

            fc.write(f"INSERT INTO track (id, title, duration, genre, streaming_url, mv_url, album_id, artist_id, popularity, track_no) "
                    f"VALUES ('{track_id}', '{title}', {duration}, '{sql_escape(track_genre)}', '{streaming_url}', '{mv_url}', '{album_id}', '{artist_id}', {popularity}, {track_no});\n")
    # 아티스트 정보 끝난 후 구분선 추가
    separator = "\n-- ==============================================\n\n"
    fa.write(separator)
    fb.write(separator)
    fc.write(separator)

print("✅ 저장완료!")