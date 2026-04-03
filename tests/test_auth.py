from tests.conftest import auth


def test_register_success(client):
    r = client.post("/auth/register", json={"username": "novo_user", "password": "senha123", "role": "user"})
    assert r.status_code == 201
    assert r.json()["username"] == "novo_user"


def test_register_duplicate(client):
    client.post("/auth/register", json={"username": "dup", "password": "senha123", "role": "user"})
    r = client.post("/auth/register", json={"username": "dup", "password": "senha123", "role": "user"})
    assert r.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={"username": "login_test", "password": "senha123", "role": "user"})
    r = client.post("/auth/token", data={"username": "login_test", "password": "senha123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "wp_user", "password": "correta", "role": "user"})
    r = client.post("/auth/token", data={"username": "wp_user", "password": "errada"})
    assert r.status_code == 401


def test_acesso_sem_token(client):
    r = client.get("/colaboradores/")
    assert r.status_code == 401
