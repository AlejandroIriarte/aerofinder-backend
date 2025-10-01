from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.db.database import SessionLocal, init_db
from app.db import crud
import time, json
from app.utils.runtime_settings import get_flags, update_flags
app = FastAPI(title="AeroFinder API", version="0.2")
@app.on_event("startup")
def _startup():
    init_db()
@app.get("/health")
def health():
    return {"status": "ok", "ts": time.time()}
@app.get("/detections")
def detections(limit: int = 50):
    with SessionLocal() as db:
        rows = crud.list_detections(db, limit=limit)
        return [{
            "id": r.id, "kind": r.kind, "bbox": [r.x,r.y,r.w,r.h],
            "confidence": r.confidence, "ts": r.ts, "frame_id": r.frame_id,
            "media_path": r.media_path, "face_id": r.face_id,
        } for r in rows]
@app.get("/alerts/stream")
def alerts_stream():
    def gen():
        while True:
            yield f"data: {json.dumps({'heartbeat': time.time()})}\n\n"
            time.sleep(2)
    return StreamingResponse(gen(), media_type="text/event-stream")
class FlagsIn(BaseModel):
    enable_person: bool | None = None
    enable_face: bool | None = None
    min_confidence: float | None = None
    face_tolerance: float | None = None
    frame_skip: int | None = None
@app.get("/settings")
def get_settings():
    return get_flags().model_dump()
@app.put("/settings")
def set_settings(payload: FlagsIn):
    updated = update_flags(**{k: v for k, v in payload.model_dump().items() if v is not None})
    return updated.model_dump()
