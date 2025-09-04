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

def test_register_duplicate_email_conflict(client):
    email = f"dup_{uuid.uuid4().hex}@example.com"
    pwd = "Passw0rd!234"
    r1 = client.post("/auth/register", json={"email": email, "password": pwd, "full_name": "Tester"})
    assert r1.status_code in (200, 201), r1.text
    r2 = client.post("/auth/register", json={"email": email, "password": pwd, "full_name": "Tester"})
    assert r2.status_code in (400, 409), r2.text

def test_register_invalid_email_422(client):
    r = client.post("/auth/register", json={"email": "not-an-email", "password": "Passw0rd!234"})
    assert r.status_code == 422, r.text

def test_login_unknown_user_401(client):
    r = client.post("/auth/login", json={"email": f"nouser_{uuid.uuid4().hex}@example.com", "password": "Passw0rd!234"})
    assert r.status_code == 401, r.text

def test_login_wrong_password_401(client):
    email = f"user_{uuid.uuid4().hex}@example.com"
    pwd = "Passw0rd!234"
    client.post("/auth/register", json={"email": email, "password": pwd})
    r = client.post("/auth/login", json={"email": email, "password": "WrongPass!234"})
    assert r.status_code == 401, r.text

def test_me_requires_bearer_token_401(client):
    r = client.get("/auth/me")
    assert r.status_code in (401, 403), r.text

def test_me_invalid_token_401(client):
    r = client.get("/auth/me", headers={"Authorization": "Bearer not-a-jwt"})
    assert r.status_code == 401, r.text
