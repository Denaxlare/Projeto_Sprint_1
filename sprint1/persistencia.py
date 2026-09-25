import json
import sprint1.modelos as estado
from sprint1.modelos import TipoAtivo, StatusAtivo, Severidade, StatusTratamento

def salvar_dados():
    dados = {
        "proximo_id_vulnerabilidade": estado.proximo_id_vulnerabilidade,
        "ativos": {}
    }

    for id_ativo, ativo in estado.ativos.items():
        dados["ativos"][id_ativo] = {
            "hostname": ativo["hostname"],
            "responsavel": ativo["responsavel"],
            "tipo": ativo["tipo"].name,
            "status": ativo["status"].name,
            "vulnerabilidades": {}
        }

        for (
            id_vulnerabilidade,
            vulnerabilidade
        ) in ativo["vulnerabilidades"].items():

            dados["ativos"][id_ativo]["vulnerabilidades"][
                id_vulnerabilidade
            ] = {
                "severidade": vulnerabilidade["severidade"].name,
                "status": vulnerabilidade["status"].name
            }

    with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    print("Dados salvos com sucesso.")


def carregar_dados():
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

    except FileNotFoundError:
        estado.ativos = {}
        estado.ativos_por_hostname = {}
        estado.proximo_id_vulnerabilidade = 1
        return

    except json.JSONDecodeError:
        print(
            "O arquivo de dados está inválido. "
            "Iniciando sem dados."
        )

        estado.ativos = {}
        estado.ativos_por_hostname = {}
        estado.proximo_id_vulnerabilidade = 1
        return

    if (
        "proximo_id_vulnerabilidade" not in dados
        or "ativos" not in dados
    ):
        print(
            "O arquivo de dados possui uma estrutura inválida."
        )

        estado.ativos = {}
        estado.ativos_por_hostname = {}
        estado.proximo_id_vulnerabilidade = 1
        return

    estado.ativos = {}
    estado.ativos_por_hostname = {}

    estado.proximo_id_vulnerabilidade = (
        dados["proximo_id_vulnerabilidade"]
    )

    for id_ativo, ativo in dados["ativos"].items():
        id_ativo = int(id_ativo)

        vulnerabilidades = {}

        for (
            id_vulnerabilidade,
            vulnerabilidade
        ) in ativo["vulnerabilidades"].items():

            id_vulnerabilidade = int(id_vulnerabilidade)

            vulnerabilidades[id_vulnerabilidade] = {
                "severidade": Severidade[
                    vulnerabilidade["severidade"]
                ],
                "status": StatusTratamento[
                    vulnerabilidade["status"]
                ]
            }

        estado.ativos[id_ativo] = {
            "hostname": ativo["hostname"],
            "responsavel": ativo["responsavel"],
            "tipo": TipoAtivo[ativo["tipo"]],
            "status": StatusAtivo[ativo["status"]],
            "vulnerabilidades": vulnerabilidades
        }

        estado.ativos_por_hostname[ativo["hostname"]] = id_ativo


# ============================================================
