from fastapi import FastAPI
from app.api.route import target_users_router
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize FastAPI app
app = FastAPI()

# Include the router
app.include_router(target_users_router)
