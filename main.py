from fastapi import FastAPI
from engine import TwitterDownloadUrlGetter

app=FastAPI()


@app.get('/{id}')
async def get_url(id):

    downloadable_url = TwitterDownloadUrlGetter(id)
    url=downloadable_url.get_video_url()
    return {'media_url':url}
