from fastapi.testclient import TestClient
from app.api.main import app
def test_health_and_settings_toggle():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
    r = client.get("/settings")
    assert r.status_code == 200
    flags_before = r.json()
    assert "enable_person" in flags_before
    payload = {"enable_face": True, "enable_person": False, "frame_skip": 1}
    r = client.put("/settings", json=payload)
    assert r.status_code == 200
    flags_after = r.json()
    assert flags_after["enable_person"] is False
    assert flags_after["frame_skip"] == 1
