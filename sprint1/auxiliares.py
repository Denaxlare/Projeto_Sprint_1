from . import modelos as estado
from .gestores import GestorAtivos


class InteracaoConsole:
    def __init__(self, gestor_ativos=None, responsaveis=None):
        self._gestor_ativos = gestor_ativos or GestorAtivos(
            estado.repositorio_ativos
        )
        self._responsaveis = responsaveis or estado.responsaveis

    def escolher_opcao(self, opcoes):
        while True:
            for indice, opcao in enumerate(opcoes, start=1):
                print(indice, "-", opcao)

            try:
                escolha = int(input("Digite um numero: "))

                if 1 <= escolha <= len(opcoes):
                    return opcoes[escolha - 1]

                print("Opção inválida. Tente novamente.")

            except ValueError:
                print("Digite um número válido.")

    def escolher_enum(self, tipo_enum):
        while True:
            for opcao in tipo_enum:
                print(opcao.value, "-", opcao.name)

            try:
                escolha = int(input("Digite um numero: "))
                return tipo_enum(escolha)

            except ValueError:
                print("Opção inválida. Tente novamente.")

    def escolher_ativo_por_responsavel(self):
        responsavel = self.escolher_opcao(self._responsaveis)
        ativos_responsavel = self._gestor_ativos.buscar_por_responsavel(
            responsavel
        )

        if not ativos_responsavel:
            print("Esse responsável não possui ativos cadastrados.")
            return None

        print("\nATIVOS DO RESPONSÁVEL")

        for id_ativo, ativo in ativos_responsavel.items():
            print(id_ativo, "-", ativo.hostname)

        while True:
            try:
                id_ativo = int(input("Digite o ID do ativo: "))

                if id_ativo in ativos_responsavel:
                    return id_ativo

                print("Esse ativo não pertence ao responsável selecionado.")

            except ValueError:
                print("Digite um número inteiro válido.")


_interacao_padrao = InteracaoConsole()


def escolher_opcao(opcoes):
    return _interacao_padrao.escolher_opcao(opcoes)


def escolher_enum(tipo_enum):
    return _interacao_padrao.escolher_enum(tipo_enum)


def escolher_ativo_por_responsavel():
    return _interacao_padrao.escolher_ativo_por_responsavel()
