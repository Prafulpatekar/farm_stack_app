from fastapi import FastAPI, Request,Response,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

from database import (
    fetch_all,
    fetch_one,
    create_todo,
    update_todo,
    remove_todo,
    
)

origins = ['http://localhost:3000'] # client origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/check_health')
async def check_http(request:Request):
    return JSONResponse({
        "status_code":status.HTTP_200_OK,
        "message":f"Your request to this url {request.url} farm_stack_app is running Timestamp:{datetime.now()} also if you are running it in local server so instead of 😒Postman you can use /docs url for 🚀Swagger UI Docs🚀!!",
        # "data":None
    })

@app.get('/api/v1/todo')
async def get_todo():
    todos = await fetch_all()
    return JSONResponse({
        "status_code":status.HTTP_200_OK,
        "data":todos
    })

@app.get('/api/v1/todo/{id}')
async def get_todo(id:int):
    return Response(f"Single todo {id}")

@app.post('/api/v1/todo')
async def create_todo(request:Request):
    return Response(f"Add todo {request.body}")

@app.put('/api/v1/todo/{id}')
async def update_todo(id:int,request:Request):
    return Response(f"Update todo for {id} and {request.body}")

@app.delete('/api/v1/todo/delete/{id}')
async def delete_todo(id:int):
    return Response(f"Delete todo of id {id}")


