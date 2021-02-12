from apiclient.discovery import build # pip install google-api-python-client
import sys
import datetime

YOUTUBE_API_KEY = 'AIzaSyB8ZADQShRlPfxTnD7sDGECEy7AbdZigfw'


max_pages = 16 #取得するページ数
maxResults = 50 #1ページあたりに含める検索結果数。maxは50
channelid = 'UCj6aXG5H_fm_RAvxH38REXw'

#動画情報を取得する関数
def search_videos(channelid, max_pages=10, maxResults=50):
    youtube = build('youtube', 'v3', developerKey = YOUTUBE_API_KEY)

    search_request = youtube.search().list(
        channelId=channelid,
        part='id,snippet',
        type='video',
        maxResults=maxResults,
    )

    i = 0
    while search_request and i < max_pages:
        search_response = search_request.execute()
        video_ids = [item['id']['videoId'] for item in search_response['items']]

        videos_response = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids)
        ).execute()

        yield videos_response['items']

        search_request = youtube.search().list_next(search_request, search_response)
        i += 1


def main():
    fname = sys.argv[1]
    channelid = sys.argv[2]
    for items_per_page in search_videos(channelid, max_pages, maxResults):
        with open(fname, 'a') as fp:
            for item in items_per_page:
                obj = {}
                obj['id'] = item['id']
                obj['url'] = 'http://youtube.com/watch?v='+obj['id']
                snippet = item['snippet']
                for key in ['publishedAt','channelId','title']:
                    obj[key] = snippet[key]
                statistics = item['statistics']
                for key in ['viewCount','likeCount','dislikeCount','favoriteCount','commentCount']:
                    obj[key] = statistics[key] if key in statistics else "NA"
                obj['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                result = ",".join(['"'+obj[v]+'"' for v in obj])
                fp.write(result)
                fp.write('\n')
main()
