import cv2, os, uuid
from typing import List
from .base import Detection
from .hog_person import HogPersonDetector
from config import settings
from app.utils.runtime_settings import get_flags
class DetectionPipeline:
    def __init__(self, alerts=None):
        self.alerts = alerts
        self._hog = HogPersonDetector(min_conf=settings.MIN_CONFIDENCE)
    def process(self, frame, meta) -> List[Detection]:
        f = get_flags()
        ts = meta.get("ts"); fid = meta.get("frame_id")
        if f.frame_skip and fid % max(1, f.frame_skip) != 0:
            return []
        detections: List[Detection] = []
        if f.enable_person:
            detections.extend(self._hog.detect(frame, ts, fid))
        for d in detections:
            x,y,w,h = d.bbox
            H,W = frame.shape[:2]
            x = max(0, min(x, W-1)); y = max(0, min(y, H-1))
            w = max(1, min(w, W - x)); h = max(1, min(h, H - y))
            crop = frame[y:y+h, x:x+w]
            fn = f"{uuid.uuid4().hex}.jpg"
            out_path = os.path.join(settings.MEDIA_DIR, fn)
            cv2.imwrite(out_path, crop)
            d.media_path = out_path
        return detections
