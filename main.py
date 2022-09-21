from fastapi import FastAPI


app=FastAPI()
#
# @app.get('/')
# async def direct():
#     return 'Hello World'

@app.get('/{id}')
async def get_url(id):
    return id

