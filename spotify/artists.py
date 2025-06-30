import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify 인증
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="SPOTIFY_CLIENT_ID",
    client_secret="SPOTIFY_CLIENT_SECRET"
))

# 아티스트 ID 직접 지정 (예: BTS)
artist_id = "2kxVxKOgoefmgkwoHipHsn"

# 아티스트 정보 가져오기
artist = sp.artist(artist_id)

# 필요한 정보 추출
name = artist['name']
genres = ", ".join(artist['genres'])
followers = artist['followers']['total']
popularity = artist['popularity']
spotify_url = artist['external_urls']['spotify']

# 파일에 저장
with open("artist_info.txt", "w", encoding="utf-8") as f:
    f.write("✅ [주요 정보]\n")
    f.write(f"🎵 아티스트 이름: {artist['name']}\n")

    # genres는 리스트 → 문자열로 변환
    genres = ", ".join(artist['genres'])
    f.write(f"📚 장르: {genres}\n")

    # followers는 dict 안 total
    f.write(f"👥 팔로워 수: {artist['followers']['total']}\n")

    f.write(f"🔥 인기도: {artist['popularity']}\n")

    f.write(f"🔗 Spotify 링크: {artist['external_urls']['spotify']}\n\n")

    # 추가 key값도 동일한 형식으로 작성
    f.write(f"🆔 아티스트 ID: {artist['id']}\n")
    f.write(f"🔗 URI: {artist['uri']}\n")
    f.write(f"🔗 API HREF: {artist['href']}\n")
    f.write(f"📌 객체 타입: {artist['type']}\n")

    # images 리스트 중 첫 번째 이미지 URL
    if artist['images']:
        f.write(f"🖼️ 대표 이미지 URL: {artist['images'][0]['url']}\n")
    else:
        f.write("🖼️ 대표 이미지 URL: 없음\n")


print("✅ artist_info.txt 에 저장 완료!")
