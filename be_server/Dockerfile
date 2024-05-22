FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./main.py /app/main.py
COPY ./posts.db /app/posts.db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
