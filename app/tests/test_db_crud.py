from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.db import database, crud
from app.detection.base import Detection
def test_db_roundtrip_with_temp_engine(tmp_path):
    db_file = tmp_path / "test_af.db"
    engine = create_engine(f"sqlite:///{db_file}", echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    database.engine = engine
    database.SessionLocal = SessionLocal
    Base.metadata.create_all(bind=engine)
    det = Detection(kind="person", bbox=(10,20,30,40), confidence=0.88, ts=1234.5, frame_id=7, media_path="media/fake.jpg", face_id="")
    with SessionLocal() as db:
        row = crud.save_detection(db, det)
        assert row.id is not None
        rows = crud.list_detections(db, limit=5)
        assert len(rows) >= 1
        last = rows[0]
        assert last.kind == "person"
        assert (last.x, last.y, last.w, last.h) == (10,20,30,40)
