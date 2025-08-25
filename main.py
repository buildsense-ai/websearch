from fastapi import FastAPI
from router.xfyun_websearch import router as xfyun_router

app = FastAPI()

# 注册路由
app.include_router(xfyun_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
