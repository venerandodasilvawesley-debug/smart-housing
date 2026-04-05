from tests.conftest import auth


from datetime import date, timedelta


from datetime import date, timedelta



def _criar_quarto(client, token, numero=901, capacidade=2):
    return client.post("/quartos/", json={"numero": numero, "capacidade": capacidade}, headers=auth(token))


def _criar_colaborador(client, token, doc):
    return client.post("/colaboradores/", json={
        "nome": "Colab Teste", "documento": doc,
        "empresa": "Emp", "setor": "X"
    }, headers=auth(token))


def test_criar_quarto(client, admin_token):
    r = _criar_quarto(client, admin_token, 800)
    assert r.status_code == 201
    assert r.json()["capacidade"] == 2


def test_capacidade_negativa_bloqueada(client, admin_token):
    r = client.post("/quartos/", json={"numero": 999, "capacidade": -1}, headers=auth(admin_token))
    assert r.status_code == 422


def test_alocar_colaborador(client, admin_token):
    q = _criar_quarto(client, admin_token, 810, 2)
    c = _criar_colaborador(client, admin_token, "88800000001")
    r = client.post("/alocacoes/", json={
        "colaborador_id": c.json()["id"],
        "quarto_id": q.json()["id"],
        "data_entrada": str(date.today())
    }, headers=auth(admin_token))
    assert r.status_code == 201


def test_quarto_cheio_bloqueado(client, admin_token):
    """Não deve alocar quando quarto atingiu capacidade."""
    q = _criar_quarto(client, admin_token, 820, 1)
    c1 = _criar_colaborador(client, admin_token, "88800000002")
    c2 = _criar_colaborador(client, admin_token, "88800000003")
    qid = q.json()["id"]

    r1 = client.post("/alocacoes/", json={
        "colaborador_id": c1.json()["id"], "quarto_id": qid,
        "data_entrada": str(date.today())
    }, headers=auth(admin_token))
    assert r1.status_code == 201

    r2 = client.post("/alocacoes/", json={
        "colaborador_id": c2.json()["id"], "quarto_id": qid,
        "data_entrada": str(date.today())
    }, headers=auth(admin_token))
    assert r2.status_code == 409  # Quarto cheio


def test_alocar_quarto_inexistente(client, admin_token):
    c = _criar_colaborador(client, admin_token, "88800000004")
    r = client.post("/alocacoes/", json={
        "colaborador_id": c.json()["id"],
        "quarto_id": 99999,
        "data_entrada": str(date.today())
    }, headers=auth(admin_token))
    assert r.status_code == 404

def test_data_saida_anterior_entrada_bloqueada(client, admin_token):
    """data_saida anterior a data_entrada deve retornar 422."""
    q = _criar_quarto(client, admin_token, 830, 2)
    c = _criar_colaborador(client, admin_token, "88800000005")
    r = client.post("/alocacoes/", json={
        "colaborador_id": c.json()["id"],
        "quarto_id": q.json()["id"],
        "data_entrada": str(date.today()),
        "data_saida": str(date.today() - timedelta(days=1))
    }, headers=auth(admin_token))
    assert r.status_code == 422


def test_desalocar_colaborador(client, admin_token):
    """DELETE /alocacoes/{id} deve desalocar e decrementar ocupacao_atual."""
    q = _criar_quarto(client, admin_token, 840, 2)
    c = _criar_colaborador(client, admin_token, "88800000006")
    qid = q.json()["id"]

    al = client.post("/alocacoes/", json={
        "colaborador_id": c.json()["id"],
        "quarto_id": qid,
        "data_entrada": str(date.today())
    }, headers=auth(admin_token))
    assert al.status_code == 201
    alocacao_id = al.json()["id"]

    # Confirma ocupacao incrementada
    q_antes = client.get(f"/quartos/{qid}", headers=auth(admin_token)).json()
    assert q_antes["ocupacao_atual"] == 1

    # Desaloca
    r = client.delete(f"/alocacoes/{alocacao_id}", headers=auth(admin_token))
    assert r.status_code == 200
    assert "msg" in r.json()

    # Confirma ocupacao decrementada
    q_depois = client.get(f"/quartos/{qid}", headers=auth(admin_token)).json()
    assert q_depois["ocupacao_atual"] == 0


def test_desalocar_inexistente(client, admin_token):
    r = client.delete("/alocacoes/99999", headers=auth(admin_token))
    assert r.status_code == 404


def test_deletar_colaborador_com_alocacao_ativa_bloqueado(client, admin_token):
    """Não deve deletar colaborador com alocação ativa."""
    q = _criar_quarto(client, admin_token, 850, 2)
    c = _criar_colaborador(client, admin_token, "88800000007")
    client.post("/alocacoes/", json={
        "colaborador_id": c.json()["id"],
        "quarto_id": q.json()["id"],
        "data_entrada": str(date.today())
    }, headers=auth(admin_token))

    r = client.delete(f"/colaboradores/{c.json()['id']}", headers=auth(admin_token))
    assert r.status_code == 409
