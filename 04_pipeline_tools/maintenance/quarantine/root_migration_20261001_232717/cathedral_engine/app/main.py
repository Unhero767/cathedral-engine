# cathedral_engine/app/main.py

from fastapi import FastAPI
from cathedral_engine.app.logging.config import configure_logging
from cathedral_engine.app.routes import auth

# Initialize Ash Archive telemetry logging configuration
configure_logging()

app = FastAPI(title="Cathedral-Engine Sovereign API")

# Mount authentication and IAM telemetry routers
app.include_router(auth.router)
