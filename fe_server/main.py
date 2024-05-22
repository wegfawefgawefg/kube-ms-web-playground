from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# Replace 'backend-service' and '8000' with your actual service name and port
backend_url = os.getenv("BACKEND_URL", "http://backend-service:8000")


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open(os.path.join(os.path.dirname(__file__), "static", "index.html")) as f:
        content = f.read().replace("{{ backend_url }}", backend_url)
    return HTMLResponse(content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
