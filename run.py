import os
from app.video.capture import VideoSource
from app.detection.pipeline import DetectionPipeline
from app.alerts.manager import AlertManager
from app.db.database import init_db, SessionLocal
from app.db import crud
def main():
    init_db()
    video_path = os.getenv("VIDEO_PATH", "0")
    source = VideoSource(video_path)
    alerts = AlertManager()
    pipe = DetectionPipeline(alerts=alerts)
    with SessionLocal() as db:
        for frame, meta in source:
            results = pipe.process(frame, meta)
            for det in results:
                crud.save_detection(db, det)
                alerts.emit(det)
if __name__ == "__main__":
    main()
