from pydantic import BaseModel
from dotenv import load_dotenv
import os, pathlib
load_dotenv()
class Settings(BaseModel):
    DB_URL: str = os.getenv("AF_DB_URL", "sqlite:///./aerofinder.db")
    MEDIA_DIR: str = os.getenv("AF_MEDIA_DIR", "./media")
    LOG_LEVEL: str = os.getenv("AF_LOG_LEVEL", "INFO")
    FRAME_SKIP: int = int(os.getenv("AF_FRAME_SKIP", "2"))
    MIN_CONFIDENCE: float = float(os.getenv("AF_MIN_CONFIDENCE", "0.5"))
    FACE_TOLERANCE: float = float(os.getenv("AF_FACE_TOLERANCE", "0.6"))
settings = Settings()
pathlib.Path(settings.MEDIA_DIR).mkdir(parents=True, exist_ok=True)
