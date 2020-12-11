# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import requests
import json
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_key = ["************************************************"]


def get_video_id_by_query(q, limit=50):
    def create_request(q):
        return f"https://youtube.googleapis.com/youtube/v3/search?part=id%2Csnippet&q={q.replace(' ', '%20')}&maxResults={limit}&key={api_key[0]}"
    url = create_request("tuyen van hoa")
    res = requests.get(url)
    video_ids = list()
    for video in json.loads(res.text)["items"]:
        if "videoId" in video['id']:
            video_ids.append(video['id']['videoId'])
    return video_ids


def get_comment(data):
    with open("comments.txt", "a") as f:
        for comm in data:
            # print(comm["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
            f.write(comm["snippet"]["topLevelComment"]["snippet"]["textDisplay"] + "\n")


def get_commend_by_video_id(video_id):
    def create_request(video_id, nextPageToken=None):
        if nextPageToken is None:
            url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&textFormat=plainText&videoId={video_id}&key={api_key[0]}"
        else:
            url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&textFormat=plainText&videoId={video_id}&key={api_key[0]}&pageToken={nextPageToken}"
        return url
    res = None
    body = dict()
    next_page = None
    while True:
        res = requests.get(create_request(video_id, nextPageToken=next_page))
        body = json.loads(res.text)
        get_comment(body["items"])
        if "nextPageToken" in body:
            next_page = body["nextPageToken"]
        else:
            break


def main():
    query_search = input("Keyword search: ")
    video_ids = get_video_id_by_query(query_search)
    for video_id in video_ids:
        get_commend_by_video_id(video_id)


if __name__ == "__main__":
    main()
