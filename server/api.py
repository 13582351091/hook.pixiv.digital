from fastapi import FastAPI
from .notify import router as NotifyRouter
from .utils import config

app = FastAPI()
@app.get("/config.json", tags=["Root"])
async def read_root() -> dict:
    return config

# 全局路由
app.include_router(NotifyRouter, prefix=config['notify'])  # https://hook.pixiv.digital/uu接受回调
if __name__ == '__main__':
    print(config['notify'])

