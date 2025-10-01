from typing import Callable, List
import json
class AlertManager:
    def __init__(self):
        self._subs: List[Callable] = []
    def subscribe(self, fn: Callable):
        self._subs.append(fn)
    def emit(self, detection):
        payload = {
            "type": detection.kind,
            "bbox": detection.bbox,
            "confidence": detection.confidence,
            "ts": detection.ts,
            "frame_id": detection.frame_id,
            "media_path": detection.media_path,
            "face_id": detection.face_id,
        }
        for fn in self._subs:
            try:
                fn(payload)
            except Exception as e:
                print("[AlertManager] error en subscriptor:", e)
        print("[ALERTA]", json.dumps(payload, ensure_ascii=False))
