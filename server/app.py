from fastapi import FastAPI
from server.routes.event import router as EventRouter

app = FastAPI()

app.include_router(EventRouter, tags=['Event'], prefix='/events')

@app.get('/', tags=['Root'])
async def read_root():
    return {'message': 'Welcome to this fantastic app!'}