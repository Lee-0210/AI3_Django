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
artist_id = "1uNFoZAHBGtllmzznpCI3s"
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

def safe_str(value):
    if value is None:
        return ''
    return str(value).strip()

artist_name = safe_str(artist['name'])

with open("artist_discography.txt", "a", encoding="utf-8") as f:
    # 아티스트 기본 정보
    f.write(f"🎵 아티스트 이름: {artist_name}\n")
    f.write(f"📚 장르: {', '.join(artist['genres'])}\n")
    f.write(f"👥 팔로워 수: {artist['followers']['total']}\n")
    f.write(f"🔥 인기도: {artist['popularity']}\n")
    f.write(f"🔗 Spotify 링크: {artist['external_urls']['spotify']}\n\n")

    f.write("📀 [디스코그래피 - 앨범 목록]\n\n")

    for album in albums['items']:
        album_id = safe_str(album['id'])
        album_detail = sp.album(album_id)

        title = safe_str(album_detail['name'])
        cover = album_detail['images'][0]['url'] if album_detail['images'] else ''
        release_date = safe_str(album_detail['release_date'])
        genre = ', '.join(album_detail.get('genres', [])) or ''
        label = safe_str(album_detail.get('label', ''))
        description = ''  # Spotify API에 없음

        # 앨범 정보
        f.write(f"앨범 id: {album_id}\n")
        f.write(f"앨범 제목: {title}\n")
        f.write(f"커버 이미지: {cover}\n")
        f.write(f"출시일: {release_date}\n")
        f.write(f"장르: {genre}\n")
        f.write(f"레이블: {label}\n")
        f.write(f"설명: {description}\n")

        f.write("\n수록곡:\n")

        tracks = sp.album_tracks(album_id)
        for track in tracks['items']:
            track_id = track['id']
            track_title = safe_str(track['name'])
            duration = track['duration_ms'] // 1000
            track_url = track['external_urls']['spotify']
            mv_url = ''  # 제공 안 됨
            track_genre = genre  # 앨범 장르와 동일

            f.write(f" - 곡 id: {track_id}\n")
            f.write(f"   곡 명: {track_title}\n")
            f.write(f"   재생시간(초): {duration}\n")
            f.write(f"   장르: {track_genre}\n")
            f.write(f"   스트리밍 URL: {track_url}\n")
            f.write(f"   뮤직비디오 URL: {mv_url}\n\n")

        f.write("-" * 40 + "\n\n")
