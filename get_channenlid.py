from apiclient.discovery import build # pip install google-api-python-client
import datetime
import sys

YOUTUBE_API_KEY = 'AIzaSyB8ZADQShRlPfxTnD7sDGECEy7AbdZigfw'

max_pages = 16 #取得するページ数
maxResults = 50 #1ページあたりに含める検索結果数。maxは50
channelid = 'UCLn8FintdYEDCSK6HaX5Q4g'

#動画情報を取得する関数
def search_videos(query, max_pages=10, maxResults=50):
    youtube = build('youtube', 'v3', developerKey = YOUTUBE_API_KEY)

    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=maxResults,
    )

    channels = []
    print(vars(search_response))
    search_response = search_response.execute()
    print(search_response)

query = sys.argv[1]

search_videos(query, max_pages, maxResults)
