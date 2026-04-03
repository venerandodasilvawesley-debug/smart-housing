from tests.conftest import auth


def _criar_colaborador(client, token, doc="99999000001"):
    return client.post("/colaboradores/", json={
        "nome": "Teste Silva", "documento": doc,
        "empresa": "Empresa A", "setor": "TI"
    }, headers=auth(token))


def test_listar_colaboradores(client, user_token):
    r = client.get("/colaboradores/", headers=auth(user_token))
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_criar_colaborador(client, admin_token):
    r = _criar_colaborador(client, admin_token, "10000000001")
    assert r.status_code == 201
    assert r.json()["nome"] == "Teste Silva"


def test_buscar_colaborador(client, admin_token):
    r = _criar_colaborador(client, admin_token, "10000000002")
    id_ = r.json()["id"]
    r2 = client.get(f"/colaboradores/{id_}", headers=auth(admin_token))
    assert r2.status_code == 200
    assert r2.json()["id"] == id_


def test_buscar_colaborador_inexistente(client, user_token):
    r = client.get("/colaboradores/99999", headers=auth(user_token))
    assert r.status_code == 404


def test_atualizar_colaborador(client, admin_token):
    r = _criar_colaborador(client, admin_token, "10000000003")
    id_ = r.json()["id"]
    r2 = client.put(f"/colaboradores/{id_}", json={"setor": "RH"}, headers=auth(admin_token))
    assert r2.status_code == 200
    assert r2.json()["setor"] == "RH"


def test_deletar_colaborador_admin(client, admin_token):
    r = _criar_colaborador(client, admin_token, "10000000099")
    id_ = r.json()["id"]
    r2 = client.delete(f"/colaboradores/{id_}", headers=auth(admin_token))
    assert r2.status_code == 200


def test_deletar_colaborador_user_proibido(client, admin_token, user_token):
    r = _criar_colaborador(client, admin_token, "10000000098")
    id_ = r.json()["id"]
    r2 = client.delete(f"/colaboradores/{id_}", headers=auth(user_token))
    assert r2.status_code == 403


def test_validacao_nome_vazio(client, admin_token):
    r = client.post("/colaboradores/", json={"nome": "", "documento": "00000"}, headers=auth(admin_token))
    assert r.status_code == 422
