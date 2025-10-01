import numpy as np, os
from app.detection.pipeline import DetectionPipeline
from app.detection.base import Detection
from config import settings
class _FakeDetector:
    def detect(self, frame, ts, frame_id):
        h, w = frame.shape[:2]
        x = max(0, w//2 - 50); y = max(0, h//2 - 50)
        return [Detection(kind="person", bbox=(x, y, 100, 100),
                          confidence=0.9, ts=ts, frame_id=frame_id)]
def test_pipeline_saves_evidence(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "MEDIA_DIR", str(tmp_path), raising=False)
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    meta = {"ts": 1.23, "frame_id": 2}
    pipe = DetectionPipeline(alerts=None)
    if hasattr(pipe, "_hog"):
        monkeypatch.setattr(pipe._hog, "detect", _FakeDetector().detect)
    dets = pipe.process(frame, meta)
    assert len(dets) == 1
    mp = dets[0].media_path
    assert mp and os.path.exists(mp)
