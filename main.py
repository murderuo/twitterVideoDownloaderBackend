from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from engine import TwitterDownloadUrlGetter

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://react-twitter-video-downloader.netlify.app','http://react-twitter-video-downloader.netlify.app','https://react-twitter-video-downloader.netlify.app/'],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index():
    return {'url':'/{id} id section must have twitter video tweet id'}

@app.get('/{id}')
async def get_url(id):

    tweet_tool = TwitterDownloadUrlGetter(id)
    url=tweet_tool.get_video_url()
    latest_videos=tweet_tool.latest_videos()
    if url==404: return {'error':'video not found'}
    return {'media_url':url,'latest_videos':latest_videos}
