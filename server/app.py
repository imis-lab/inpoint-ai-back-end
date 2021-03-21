import requests
from decouple import config
from fastapi import FastAPI
from fastapi import status

from ai import discourse_graph
from server.models.responses import (ResponseModel, ErrorResponseModel)
from server.routes.event import router as EventRouter

MAIN_BACKEND_URL = config('MAIN_BACKEND_URL')

app = FastAPI()

app.include_router(EventRouter, tags=['Event'], prefix='/events')


@app.get('/', tags=['Root'])
async def read_root():
    return {'message': 'Welcome to the AI back-end!'}


@app.get('/initialize', tags=['Initialize Graph'])
async def initialize_graph():
    try:
        res = requests.get(f'{MAIN_BACKEND_URL}/api/discourses/ai')
    except requests.exceptions.RequestException as e:
        return ErrorResponseModel.return_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                  'Failed to communicate with the main back-end application!')
    if res.status_code == 200:
        json_data = res.json()
        discourse_graph.add_discourses(json_data)
    else:
        return ErrorResponseModel.return_response(f'{res.text}, {res.status_code}', status.HTTP_424_FAILED_DEPENDENCY,
                                                  'Failed to communicate with the main back-end application!')
    return ResponseModel.return_response({'message': 'The graph database has been initialized'})
