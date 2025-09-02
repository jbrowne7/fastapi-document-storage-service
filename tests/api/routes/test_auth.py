import uuid

def test_register_login_me(client):
    email = f"test+{uuid.uuid4().hex}@example.com"
    pwd = "Passw0rd!234"

    r = client.post("/auth/register", json={"email": email, "password": pwd, "full_name": "Tester"})
    assert r.status_code in (200, 201), r.text

    r = client.post("/auth/login", json={"email": email, "password": pwd})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json().get("email") == email