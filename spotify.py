import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ✅ 인증 정보 입력
client_id = '2ba4d34e04994e64b21753ef7b9ad2c5'
client_secret = 'db366f14e61d4f52ba1a408801c43d8c'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ✅ 한국 차트 Top 50 플레이리스트 ID
korea_top50_playlist_id = '2Bas8kAMgrb1Eo1Udkxnh8'

# ✅ 플레이리스트에서 트랙 추출 → 앨범 ID 추출
results = sp.playlist_tracks(korea_top50_playlist_id, market='KR', limit=50)
album_ids = set()
for item in results['items']:
    album = item['track']['album']
    album_ids.add(album['id'])  # 중복 제거

# ✅ 앨범 정보 + 수록곡 상세 정보 저장 함수
def save_album_with_track_details(album_id, filename='korea_albums_with_tracks_detailed.txt'):
    album = sp.album(album_id, market='KR')
    track_items = sp.album_tracks(album_id, market='KR')['items']
    track_ids = [track['id'] for track in track_items if track['id']]

    # 최대 50개씩 나눠서 상세 정보 요청 (API 제한 대응)
    detailed_tracks = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        batch_result = sp.tracks(batch)['tracks']
        detailed_tracks.extend(batch_result)

    cover_url = album['images'][0]['url'] if album['images'] else "커버 이미지 없음"
    album_type = album.get('album_type', '정보없음')
    label = album.get('label', '정보없음')
    release_date_precision = album.get('release_date_precision', '정보없음')

    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"[앨범] {album['name']} ({album['release_date']}) (ID: {album['id']})\n")  # 앨범 ID 추가
        f.write(f"아티스트: {', '.join(artist['name'] for artist in album['artists'])}\n")
        f.write(f"앨범 커버: {cover_url}\n")
        f.write(f"앨범 종류: {album_type}\n")
        f.write(f"레이블: {label}\n")
        f.write(f"출시일 정밀도: {release_date_precision}\n")
        f.write(f"총 트랙 수: {album['total_tracks']}\n")
        f.write("🎵 수록곡 상세 정보:\n")

        for i, track in enumerate(detailed_tracks, start=1):
            name = track['name']
            track_id = track['id']
            artists = ', '.join(artist['name'] for artist in track['artists'])
            duration = track['duration_ms'] // 1000
            popularity = track['popularity']
            explicit = "Yes" if track['explicit'] else "No"
            preview = track['preview_url'] or "미리듣기 없음"
            url = track['external_urls']['spotify']
            track_number = track.get('track_number', '정보없음')
            disc_number = track.get('disc_number', '정보없음')
            isrc = track.get('external_ids', {}).get('isrc', '정보없음')
            is_local = "Yes" if track.get('is_local', False) else "No"

            f.write(f"  {i}. {name} (ID: {track_id})\n")
            f.write(f"     - 아티스트: {artists}\n")
            f.write(f"     - 트랙 번호: {track_number} | 디스크 번호: {disc_number}\n")
            f.write(f"     - 길이: {duration}초 | 인기: {popularity} | 욕설 포함: {explicit} | 로컬곡 여부: {is_local}\n")
            f.write(f"     - ISRC 코드: {isrc}\n")
            f.write(f"     - 미리듣기: {preview}\n")
            f.write(f"     - 링크: {url}\n")
        f.write("-" * 60 + "\n\n")


# ✅ 실행
output_file = 'korea_albums_with_tracks_detailed.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("📀 한국 차트 기반 최신 앨범 정보 (수록곡 상세 포함)\n")
    f.write("=" * 60 + "\n\n")

for album_id in album_ids:
    save_album_with_track_details(album_id, output_file)

print("✅ 한국 최신 앨범 50개 및 수록곡 상세 정보 저장 완료!")
