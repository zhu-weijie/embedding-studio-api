from fastapi import FastAPI

app = FastAPI(
    title="Embedding Studio API",
    description="An API for text processing and embedding generation.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Embedding Studio API!"}
