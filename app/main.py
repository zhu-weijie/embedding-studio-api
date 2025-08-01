import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
max_tries = 60 * 5
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        logger.error(e)
        raise e


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing service...")
    init()
    logger.info("Service finished initializing.")

    yield

    logger.info("Service shutting down.")


app = FastAPI(
    title="Embedding Studio API",
    description="An API for text processing and embedding generation.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Embedding Studio API!"}
