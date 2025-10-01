from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer
from .database import Base
class DetectionORM(Base):
    __tablename__ = "detections"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kind: Mapped[str] = mapped_column(String(20))
    x: Mapped[int] = mapped_column(Integer)
    y: Mapped[int] = mapped_column(Integer)
    w: Mapped[int] = mapped_column(Integer)
    h: Mapped[int] = mapped_column(Integer)
    confidence: Mapped[float] = mapped_column(Float)
    ts: Mapped[float] = mapped_column(Float)
    frame_id: Mapped[int] = mapped_column(Integer)
    media_path: Mapped[str] = mapped_column(String(512), default="")
    face_id: Mapped[str] = mapped_column(String(128), default="")
