from dataclasses import dataclass
from typing import List, Tuple, Optional
@dataclass
class Detection:
    kind: str
    bbox: Tuple[int,int,int,int]
    confidence: float
    ts: float
    frame_id: int
    lat: Optional[float] = None
    lon: Optional[float] = None
    media_path: Optional[str] = None
    face_id: Optional[str] = None
class Detector:
    def detect(self, frame, ts: float, frame_id: int) -> List[Detection]:
        raise NotImplementedError
