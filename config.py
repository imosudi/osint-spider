import os

class Config:
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5090))
    DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")
