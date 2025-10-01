import argparse
from app.video.capture import VideoSource
from app.detection.pipeline import DetectionPipeline
from app.alerts.manager import AlertManager
from app.db.database import init_db, SessionLocal
from app.db import crud
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True, help="Ruta a video local (mp4/avi)")
    args = p.parse_args()
    init_db()
    source = VideoSource(args.video)
    alerts = AlertManager()
    pipe = DetectionPipeline(alerts=alerts)
    with SessionLocal() as db:
        for frame, meta in source:
            dets = pipe.process(frame, meta)
            for d in dets:
                crud.save_detection(db, d)
                alerts.emit(d)
if __name__ == "__main__":
    main()
