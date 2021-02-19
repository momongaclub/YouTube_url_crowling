from apiclient.discovery import build
import sys
import time

# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup


# どこまでやったっけ情報を記録。
# データベースに書き込む


YOUTUBE_API_KEY = 'AIzaSyChpNl0DlPSsb7lU6RmiFV0Y2MTyBVzWLw'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def load_ids(fname):
    ids = []
    with open(fname, 'r') as fp:
        for line in fp:
            line = line.rstrip('\n')
            url = 'https://www.youtube.com/watch?v=' + line
            ids.append(url)
    return ids


def get_movie_infos(ids, youtube_api):
    all_movie_info = []
    info_names = ['publishedAt', 'channelId', 'title', 'description', 'channelTitle']
    for id_ in ids:
        time.sleep(5)
        search_response = youtube_api.search().list(
            part='id, snippet',
            q = id_,
        ).execute()

        movie_infos = []
        try:
            results = search_response['items'][0]['snippet']
            for info_name in info_names:
                movie_infos.append(results[info_name])
            print('result', movie_infos)
            all_movie_info.append(movie_infos)
        except:
            print('not found')
    return all_movie_info


def write_info(fname, movie_info):
    with open(fname, 'w') as fp:
        for line in movie_info:
            line = '\t'.join(line)
            fp.write(line)
            fp.write('\n')

def get_movie_infos_beautiful(ids):
    all_movie_info = []
    for id_ in ids:
        print(id_)
        html = urllib.request.urlopen(id_)
        soup = BeautifulSoup(html, "html.parser")
        print(soup.title.string) # アルゴリズム雑記
        title = soup.title.string
        url = id_
        all_movie_info.append([title, url, 'cid'])
    return all_movie_info

def main():
    youtube_api = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    ids = load_ids(sys.argv[1])
    all_movie_info = get_movie_infos_beautiful(ids)
    write_info(sys.argv[2], all_movie_info)

main()
