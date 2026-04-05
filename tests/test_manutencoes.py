from tests.conftest import auth


def _criar_quarto(client, token, numero=301):
    return client.post("/quartos/", json={"numero": numero, "capacidade": 3}, headers=auth(token))


def _criar_manutencao(client, token, quarto_id, descricao="Torneira com vazamento"):
    return client.post("/manutencoes/", json={
        "quarto_id": quarto_id,
        "descricao": descricao,
    }, headers=auth(token))


def test_listar_manutencoes(client, user_token):
    r = client.get("/manutencoes/", headers=auth(user_token))
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_criar_manutencao(client, admin_token):
    q = _criar_quarto(client, admin_token, 302)
    r = _criar_manutencao(client, admin_token, q.json()["id"])
    assert r.status_code == 201
    assert r.json()["status"] == "Aberto"
    assert r.json()["data_abertura"] is not None


def test_criar_manutencao_descricao_curta(client, admin_token):
    q = _criar_quarto(client, admin_token, 303)
    r = client.post("/manutencoes/", json={
        "quarto_id": q.json()["id"],
        "descricao": "x"
    }, headers=auth(admin_token))
    assert r.status_code == 422


def test_buscar_manutencao(client, admin_token):
    q = _criar_quarto(client, admin_token, 304)
    r = _criar_manutencao(client, admin_token, q.json()["id"])
    id_ = r.json()["id"]
    r2 = client.get(f"/manutencoes/{id_}", headers=auth(admin_token))
    assert r2.status_code == 200
    assert r2.json()["id"] == id_


def test_buscar_manutencao_inexistente(client, user_token):
    r = client.get("/manutencoes/99999", headers=auth(user_token))
    assert r.status_code == 404


def test_atualizar_status_manutencao(client, admin_token):
    q = _criar_quarto(client, admin_token, 305)
    r = _criar_manutencao(client, admin_token, q.json()["id"])
    id_ = r.json()["id"]
    r2 = client.put(f"/manutencoes/{id_}", json={"status": "Em andamento"}, headers=auth(admin_token))
    assert r2.status_code == 200
    assert r2.json()["status"] == "Em andamento"


def test_fechar_manutencao(client, admin_token):
    q = _criar_quarto(client, admin_token, 306)
    r = _criar_manutencao(client, admin_token, q.json()["id"])
    id_ = r.json()["id"]
    r2 = client.put(f"/manutencoes/{id_}", json={
        "status": "Fechado",
        "data_fechamento": "2026-04-05T10:00:00"
    }, headers=auth(admin_token))
    assert r2.status_code == 200
    assert r2.json()["status"] == "Fechado"
    assert r2.json()["data_fechamento"] is not None


def test_status_invalido_bloqueado(client, admin_token):
    q = _criar_quarto(client, admin_token, 307)
    r = _criar_manutencao(client, admin_token, q.json()["id"])
    id_ = r.json()["id"]
    r2 = client.put(f"/manutencoes/{id_}", json={"status": "Pendente"}, headers=auth(admin_token))
    assert r2.status_code == 422


def test_deletar_manutencao_admin(client, admin_token):
    q = _criar_quarto(client, admin_token, 308)
    r = _criar_manutencao(client, admin_token, q.json()["id"])
    id_ = r.json()["id"]
    r2 = client.delete(f"/manutencoes/{id_}", headers=auth(admin_token))
    assert r2.status_code == 200


def test_deletar_manutencao_user_proibido(client, admin_token, user_token):
    q = _criar_quarto(client, admin_token, 309)
    r = _criar_manutencao(client, admin_token, q.json()["id"])
    id_ = r.json()["id"]
    r2 = client.delete(f"/manutencoes/{id_}", headers=auth(user_token))
    assert r2.status_code == 403
