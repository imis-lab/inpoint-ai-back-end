from fastapi import APIRouter, Body, status
from server.models.responses import ResponseModel, ErrorResponseModel

router = APIRouter()

@router.get('/', response_description='')
async def get_discourses():
    return ResponseModel.return_response({'message': 'OK!'})