from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

load_dotenv(override=True)

limiter = Limiter(
    get_remote_address,
    storage_uri=os.getenv("REDIS_RATE_LIMITER_URI")
)