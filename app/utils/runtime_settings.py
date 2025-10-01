from pydantic import BaseModel
from threading import RLock
class RuntimeFlags(BaseModel):
    enable_person: bool = True
    enable_face: bool = False
    min_confidence: float = 0.5
    face_tolerance: float = 0.6
    frame_skip: int = 2
_flags = RuntimeFlags()
_lock = RLock()
def get_flags() -> RuntimeFlags:
    with _lock:
        return _flags.model_copy()
def update_flags(**kwargs) -> RuntimeFlags:
    with _lock:
        for k, v in kwargs.items():
            if hasattr(_flags, k) and v is not None:
                setattr(_flags, k, v)
        return _flags.model_copy()
