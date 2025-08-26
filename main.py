from fastapi import FastAPI
from router.xfyun_websearch import router as xfyun_router
import uvicorn

app = FastAPI()

# 注册路由
app.include_router(xfyun_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=1234, reload=True)
