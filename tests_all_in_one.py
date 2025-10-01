# tests_all_in_one.py
# 1) API: /health y (si existe) /settings
# 2) BD: round-trip en SQLite temporal (no toca tu DB real)
# 3) Pipeline: guarda evidencia con detector falso (sin YOLO)

import os, numpy as np, importlib
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

api = importlib.import_module("app.api.main")
db_database = importlib.import_module("app.db.database")
db_crud = importlib.import_module("app.db.crud")
pipeline_mod = importlib.import_module("app.detection.pipeline")
base_mod = importlib.import_module("app.detection.base")
config_mod = importlib.import_module("config")

# 👇 Importamos los toggles para poder restaurarlos
try:
    from app.utils.runtime_settings import update_flags
except Exception:
    update_flags = None

Detection = base_mod.Detection
DetectionPipeline = pipeline_mod.DetectionPipeline
Base = db_database.Base

def test_api_health_and_settings():
    client = TestClient(api.app)

    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

    # /settings puede no existir -> no romper
    r = client.get("/settings")
    if r.status_code == 200:
        payload = {"enable_person": False, "frame_skip": 1}
        r = client.put("/settings", json=payload)
        assert r.status_code == 200
        assert isinstance(r.json(), dict)

def test_db_roundtrip_tmp_engine(tmp_path):
    db_file = tmp_path / "test_af.db"
    engine = create_engine(f"sqlite:///{db_file}", echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # Parcheamos para NO usar tu DB real
    db_database.engine = engine
    db_database.SessionLocal = SessionLocal
    Base.metadata.create_all(bind=engine)

    det = Detection(kind="person", bbox=(10,20,30,40), confidence=0.9,
                    ts=1234.5, frame_id=7, media_path="media/fake.jpg", face_id="")

    with SessionLocal() as db:
        row = db_crud.save_detection(db, det)
        assert row.id is not None

        rows = db_crud.list_detections(db, limit=3)
        assert len(rows) >= 1
        last = rows[0]
        assert last.kind == "person"
        assert (last.x, last.y, last.w, last.h) == (10,20,30,40)

# Detector falso: simula 1 persona detectada
class _FakeDetector:
    def detect(self, frame, ts, frame_id):
        h, w = frame.shape[:2]
        x = max(0, w//2 - 50); y = max(0, h//2 - 50)
        return [Detection(kind="person", bbox=(x, y, 100, 100),
                          confidence=0.95, ts=ts, frame_id=frame_id)]

def test_pipeline_evidence(tmp_path, monkeypatch):
    # ✅ Restablece flags para esta prueba (habilitar personas)
    if update_flags:
        update_flags(enable_person=True, enable_face=False, frame_skip=1)

    # Redirige MEDIA_DIR al tmp
    monkeypatch.setattr(config_mod.settings, "MEDIA_DIR", str(tmp_path), raising=False)

    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    meta = {"ts": 1.23, "frame_id": 2}

    pipe = DetectionPipeline(alerts=None)

    # Inyecta el detector falso (independiente de YOLO/HOG)
    if hasattr(pipe, "_hog"):
        monkeypatch.setattr(pipe._hog, "detect", _FakeDetector().detect)
    elif hasattr(pipe, "detectors"):
        pipe.detectors = [_FakeDetector()]

    dets = pipe.process(frame, meta)
    assert len(dets) >= 1, "El pipeline no devolvió detecciones con el fake"
    mp = dets[0].media_path
    assert mp and os.path.exists(mp), "No se guardó el recorte de evidencia"
