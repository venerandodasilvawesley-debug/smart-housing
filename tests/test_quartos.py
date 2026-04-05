from tests.conftest import auth
from datetime import date


def _criar_quarto(client, token, numero=101, capacidade=3):
    return client.post("/quartos/", json={"numero": numero, "capacidade": capacidade}, headers=auth(token))


def _criar_colaborador(client, token, doc="77700000001"):
    return client.post("/colaboradores/", json={
        "nome": "Colab Quarto", "documento": doc,
        "empresa": "Emp", "setor": "X"
    }, headers=auth(token))


def test_listar_quartos(client, user_token):
    r = client.get("/quartos/", headers=auth(user_token))
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_criar_quarto(client, admin_token):
    r = _criar_quarto(client, admin_token, 201, 4)
    assert r.status_code == 201
    assert r.json()["numero"] == 201
    assert r.json()["capacidade"] == 4
    assert r.json()["ocupacao_atual"] == 0


def test_criar_quarto_capacidade_zero_bloqueado(client, admin_token):
    r = client.post("/quartos/", json={"numero": 999, "capacidade": 0}, headers=auth(admin_token))
    assert r.status_code == 422


def test_buscar_quarto(client, admin_token):
    r = _criar_quarto(client, admin_token, 202)
    id_ = r.json()["id"]
    r2 = client.get(f"/quartos/{id_}", headers=auth(admin_token))
    assert r2.status_code == 200
    assert r2.json()["id"] == id_


def test_buscar_quarto_inexistente(client, user_token):
    r = client.get("/quartos/99999", headers=auth(user_token))
    assert r.status_code == 404


def test_atualizar_quarto(client, admin_token):
    r = _criar_quarto(client, admin_token, 203, 2)
    id_ = r.json()["id"]
    r2 = client.put(f"/quartos/{id_}", json={"capacidade": 5}, headers=auth(admin_token))
    assert r2.status_code == 200
    assert r2.json()["capacidade"] == 5


def test_deletar_quarto_admin(client, admin_token):
    r = _criar_quarto(client, admin_token, 204)
    id_ = r.json()["id"]
    r2 = client.delete(f"/quartos/{id_}", headers=auth(admin_token))
    assert r2.status_code == 200


def test_deletar_quarto_user_proibido(client, admin_token, user_token):
    r = _criar_quarto(client, admin_token, 205)
    id_ = r.json()["id"]
    r2 = client.delete(f"/quartos/{id_}", headers=auth(user_token))
    assert r2.status_code == 403


def test_deletar_quarto_com_alocacao_ativa_bloqueado(client, admin_token):
    """Não deve deletar quarto com alocação ativa (data_saida=None)."""
    q = _criar_quarto(client, admin_token, 206, 2)
    c = _criar_colaborador(client, admin_token, "77700000099")
    client.post("/alocacoes/", json={
        "colaborador_id": c.json()["id"],
        "quarto_id": q.json()["id"],
        "data_entrada": str(date.today())
    }, headers=auth(admin_token))

    r = client.delete(f"/quartos/{q.json()['id']}", headers=auth(admin_token))
    assert r.status_code == 409
