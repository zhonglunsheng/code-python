import json
import logging
import sys
import threading
import time
from typing import Union, List

import uvicorn
from fastapi import FastAPI, Query
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from asyncer import asyncify

from fastapitest import init_logging

logger = init_logging()

class User(BaseModel):
    class Info(BaseModel):
        address: str

    # 必填
    user_name: str = Field(..., title="hello", description="用户名")
    # 选填 默认值
    passw_word: str = Field(default="123", title="hello", description="用户名")
    # 嵌套复杂对象
    info_list: List[Info] = Field(..., description="用户信息")


app = FastAPI(title="fastapi框架基础使用")
# 静态文件访问
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    print("程序启动")


@app.on_event("shutdown")
async def shutdown_event():
    print("程序结束")


@app.exception_handler(RequestValidationError)
async def handle_validate_param_exception(request: Request, exc: RequestValidationError):
    print(exc.errors())
    return JSONResponse({
        "code": 500,
        "msg": "必填参数校验失败，请检查传入参数",
        "data": exc.errors()
    })


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logger.info("加载中间件2")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.post("/user")
def read_root(user: User):
    return user


@app.get("/test")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def sync_data(name):
    time.sleep(5)
    print("sync data ...")
    print(threading.current_thread().name)
    return name

@app.get("/test2")
async def read_item(backgroundTask: BackgroundTasks):
    backgroundTask.add_task(sync_data)


@app.get("/test3")
async def read_item(backgroundTask: BackgroundTasks):
    """
    同步线程 转换为异步 并且获取结果
    :param backgroundTask:
    :return:
    """
    print(threading.current_thread().name)
    message = await asyncify(sync_data)(name="World")
    return message

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
