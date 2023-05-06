from fastapi import FastAPI, Request,Response,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from model import Todo
from json import loads,dumps
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
    try:
        todos = fetch_all()
        # return JSONResponse({
        #     "status_code":status.HTTP_200_OK,
        #     "data":todos
        # })
        return todos
    except Exception as e:
        return HTTPException(500,f"Internal server error {e}")

@app.get('/api/v1/todo/{title}',response_model=Todo)
async def get_todo(title:str):
    try:
        response = await fetch_one(title)
        if response:
            # return JSONResponse({
            #     "status_code":status.HTTP_200_OK,
            #     "message":"Success",
            #     "data":response
            # })
            return response
        return HTTPException(404,f"There is no todo of title {title}")
    except Exception as e:
        return HTTPException(500,f"Internal server error {e}")

@app.post('/api/v1/todo')
async def create_todo(todo:Todo):
    try:
        response = await create_todo(todo)
        print(response)
        if response:
            return response
        return HTTPException(400,"Bad request")
    except Exception as e:
        return HTTPException(500,f"Internal server error {e}")

@app.put('/api/v1/todo/{title}',response_model=Todo)
async def update_todo(title:str,desc:str):
    try:
        response = await update_todo(title,desc)
        if response:
            return JSONResponse({
                "status_code":status.HTTP_201_CREATED,
                "message":"Todo Updated",
                "data":response
            })
        return HTTPException(400,"Bad request")
    except Exception as e:
        return HTTPException(500,f"Internal server error {e}")

@app.delete('/api/v1/todo/delete/{title}')
async def delete_todo(title:str):
    try:
        response = await delete_todo(title)
        if response:
            return JSONResponse({
                "status_code":status.HTTP_200_OK,
                "message":"Todo Deleted",
                "data":response
            })
        return HTTPException(404,"Not Found")
    except Exception as e:
        return HTTPException(500,f"Internal server error {e}")


