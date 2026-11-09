from .ativos import AtivosConsole
from .vulnerabilidades import VulnerabilidadesConsole
from .persistencia import PersistenciaJSON
from . import modelos as estado

class MenuConsole:
    def __init__(self, acoes=None):
        if acoes is None:
            ativos = AtivosConsole()
            vulnerabilidades = VulnerabilidadesConsole()
            acoes = {
                1: ativos.cadastrar_ativo,
                2: ativos.consultar_ativos,
                3: ativos.atualizar_ativo,
                4: ativos.remover_ativo,
                5: vulnerabilidades.gerenciamento_vulnerabilidades,
            }
        self._acoes = acoes

    def executar(self):
        while True:
            print("\nMENU PRINCIPAL")
            print("1 - Cadastro de ativos")
            print("2 - Consulta de ativos")
            print("3 - Atualização de ativos")
            print("4 - Exclusão de ativos")
            print("5 - Gerenciamento de vulnerabilidades")
            print("0 - Sair")

            try:
                escolha = int(input("Digite a opção: "))
            except ValueError:
                print("Digite um número válido.")
                continue

            if escolha == 0:
                return

            acao = self._acoes.get(escolha)
            if acao is None:
                print("Opção inválida. Tente novamente.")
                continue

            acao()


class Aplicacao:
    def __init__(self, menu_console=None, persistencia=None):
        self._menu_console = menu_console or MenuConsole()
        self._persistencia = persistencia or PersistenciaJSON(
            estado.repositorio_ativos
        )

    def sair(self):
        self._persistencia.salvar()
        print("Programa encerrado.")

    def executar(self):
        self._persistencia.carregar()
        self._menu_console.executar()
        self.sair()


# Funções mantidas para compatibilidade com chamadas existentes.
def sair():
    Aplicacao().sair()


def menu():
    MenuConsole().executar()


# ============================================================


def main():
    Aplicacao().executar()


if __name__ == "__main__":
    main()
