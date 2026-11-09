import json

from . import modelos as estado
from .modelos import Ativo, Vulnerabilidade


class PersistenciaJSON:
    def __init__(self, repositorio, caminho="dados.json"):
        self._repositorio = repositorio
        self._caminho = caminho

    def salvar(self):
        dados = {
            "proximo_id_vulnerabilidade": self._repositorio.proximo_id_vulnerabilidade,
            "ativos": {},
        }

        for id_ativo, ativo in self._repositorio.ativos.items():
            dados["ativos"][id_ativo] = ativo.to_dict()

        with open(self._caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

        print("Dados salvos com sucesso.")

    def carregar(self):
        try:
            with open(self._caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            self._repositorio.limpar()
            return
        except json.JSONDecodeError:
            print("O arquivo de dados está inválido. Iniciando sem dados.")
            self._repositorio.limpar()
            return

        if "proximo_id_vulnerabilidade" not in dados or "ativos" not in dados:
            print("O arquivo de dados possui uma estrutura inválida.")
            self._repositorio.limpar()
            return

        self._repositorio.limpar()

        for id_ativo, ativo in dados["ativos"].items():
            id_ativo = int(id_ativo)
            objeto_ativo = Ativo.from_dict(id_ativo, ativo)
            self._repositorio.cadastrar(objeto_ativo)

            for id_vulnerabilidade, vulnerabilidade in ativo["vulnerabilidades"].items():
                self._repositorio.restaurar_vulnerabilidade(
                    id_ativo,
                    int(id_vulnerabilidade),
                    Vulnerabilidade.from_dict(vulnerabilidade),
                )

        self._repositorio.restaurar_proximo_id_vulnerabilidade(
            dados["proximo_id_vulnerabilidade"]
        )


_persistencia_padrao = PersistenciaJSON(estado.repositorio_ativos)


def salvar_dados():
    _persistencia_padrao.salvar()


def carregar_dados():
    _persistencia_padrao.carregar()
