import cv2
from typing import List
from .base import Detection, Detector
class HogPersonDetector(Detector):
    def __init__(self, min_conf=0.5):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.min_conf = float(min_conf)
    def detect(self, frame, ts: float, frame_id: int) -> List[Detection]:
        rects, weights = self.hog.detectMultiScale(frame, winStride=(8,8), padding=(8,8), scale=1.05)
        out = []
        for (x,y,w,h), conf in zip(rects, weights):
            if conf >= self.min_conf:
                out.append(Detection(kind="person", bbox=(int(x),int(y),int(w),int(h)),
                                     confidence=float(conf), ts=ts, frame_id=frame_id))
        return out
