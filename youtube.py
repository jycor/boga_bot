import os
import googleapiclient.discovery

DEVELOPER_KEY = os.environ['YOUTUBE_API_KEY']

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=DEVELOPER_KEY)

# TODO: cache responses to reduce api calls?
# TODO: get n trending videos?
# get_trending() returns the #1 trending video on youtube.
def get_trending():
    req = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        maxResults=1
    )
    res = req.execute()
    yt_id = res['items'][0]['id']
    yt_link = "https://www.youtube.com/watch?v={0}".format(yt_id)
    return yt_link
