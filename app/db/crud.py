from sqlalchemy.orm import Session
from .models import DetectionORM
from app.detection.base import Detection
def save_detection(db: Session, d: Detection) -> DetectionORM:
    x,y,w,h = d.bbox
    row = DetectionORM(
        kind=d.kind, x=x, y=y, w=w, h=h,
        confidence=d.confidence, ts=d.ts, frame_id=d.frame_id,
        media_path=d.media_path or "", face_id=d.face_id or "",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
def list_detections(db: Session, limit: int = 100):
    return db.query(DetectionORM).order_by(DetectionORM.id.desc()).limit(limit).all()
