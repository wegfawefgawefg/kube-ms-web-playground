from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()


@app.get("/")
def read_root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
