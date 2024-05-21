from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

DATABASE = "posts.db"


class Post(BaseModel):
    username: str
    text: str


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        text TEXT NOT NULL
                    )"""
    )
    conn.commit()
    conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    # Handle any necessary cleanup here


app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/api/posts")
def create_post(post: Post):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (username, text) VALUES (?, ?)", (post.username, post.text)
    )
    conn.commit()
    conn.close()
    return post


@app.get("/api/posts")
def read_posts():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, text FROM posts ORDER BY id DESC LIMIT 100")
    posts = cursor.fetchall()
    conn.close()
    return [{"username": username, "text": text} for username, text in posts]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
