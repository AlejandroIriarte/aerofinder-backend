import cv2, time
from typing import Iterator
class VideoSource:
    def __init__(self, src=0, fps_limit: float | None = None):
        self.cap = cv2.VideoCapture(int(src) if str(src).isdigit() else src)
        if not self.cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la fuente de video: {src}")
        self.frame_id = 0
        self.fps_limit = fps_limit
    def __iter__(self) -> Iterator[tuple]:
        last = 0.0
        while True:
            ok, frame = self.cap.read()
            if not ok:
                break
            now = time.time()
            if self.fps_limit:
                if now - last < 1.0 / self.fps_limit:
                    continue
                last = now
            meta = {"ts": now, "frame_id": self.frame_id}
            self.frame_id += 1
            yield frame, meta
    def release(self):
        self.cap.release()
