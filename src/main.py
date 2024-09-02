import uvicorn
from fastapi import FastAPI
from game.router import router as game_router

app = FastAPI(root_path="/api/v1")
app.include_router(game_router)


if __name__ == '__main__':
    uvicorn.run(app, port=4000, host='0.0.0.0')
