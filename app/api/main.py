import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

app = FastAPI(
    title="GOVAIAPP",
    description="API de generation de politiques de gouvernance IA",
    version="0.1.0",
)

app.include_router(router)