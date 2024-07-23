from fastapi.middleware.cors import CORSMiddleware
import logging


def setup_cors_and_logging(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logging.basicConfig(level=logging.INFO)
