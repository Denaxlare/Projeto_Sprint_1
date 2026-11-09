from . import modelos as estado
from .modelos import Severidade, StatusTratamento
from .auxiliares import InteracaoConsole
from .gestores import GestorVulnerabilidades


class VulnerabilidadesConsole:
    def __init__(self, gestor_vulnerabilidades=None, interacao=None):
        self.gestor_vulnerabilidades = (
            gestor_vulnerabilidades
            or GestorVulnerabilidades(estado.repositorio_ativos)
        )
        self.interacao = interacao or InteracaoConsole()

    def cadastrar_vulnerabilidade(self):
        id_ativo = self.interacao.escolher_ativo_por_responsavel()
        if id_ativo is None:
            return

        while True:
            severidade = self.interacao.escolher_enum(Severidade)
            status_tratamento = self.interacao.escolher_enum(StatusTratamento)
            descricao = input(
                "Digite a descrição da vulnerabilidade (opcional): "
            ).strip()

            id_vulnerabilidade = self.gestor_vulnerabilidades.cadastrar(
                id_ativo,
                severidade,
                status_tratamento,
                descricao,
            )

            print("Vulnerabilidade cadastrada com sucesso.")
            print("ID da vulnerabilidade:", id_vulnerabilidade)
            if not self._perguntar_sim_nao(
                "Deseja cadastrar outra vulnerabilidade?"
            ):
                return

    def visualizar_vulnerabilidades(self):
        id_ativo = self.interacao.escolher_ativo_por_responsavel()
        if id_ativo is None:
            return

        vulnerabilidades = self.gestor_vulnerabilidades.listar_por_ativo(
            id_ativo
        )
        print("\nVULNERABILIDADES DO ATIVO")

        if not vulnerabilidades:
            print("Este ativo não possui vulnerabilidades cadastradas.")
            return

        for id_vulnerabilidade, vulnerabilidade in vulnerabilidades:
            self._exibir_vulnerabilidade(id_vulnerabilidade, vulnerabilidade)

    def atualizar_vulnerabilidade(self):
        vulnerabilidade = self._selecionar_vulnerabilidade()
        if vulnerabilidade is None:
            return

        id_ativo, id_vulnerabilidade, objeto_vulnerabilidade = vulnerabilidade

        while True:
            print("\nATUALIZAÇÃO DE VULNERABILIDADE")
            print("1 - Alterar severidade")
            print("2 - Alterar status de tratamento")
            print("0 - Voltar")

            try:
                escolha = int(input("Digite a opção: "))

                if escolha == 1:
                    nova_severidade = self.interacao.escolher_enum(Severidade)
                    if nova_severidade == objeto_vulnerabilidade.severidade:
                        print("A severidade selecionada já é a atual.")
                    else:
                        self.gestor_vulnerabilidades.atualizar_severidade(
                            id_ativo,
                            id_vulnerabilidade,
                            nova_severidade,
                        )
                        objeto_vulnerabilidade.severidade = nova_severidade
                        print("Severidade alterada com sucesso.")

                elif escolha == 2:
                    novo_status = self.interacao.escolher_enum(StatusTratamento)
                    if novo_status == objeto_vulnerabilidade.status:
                        print("O status selecionado já é o atual.")
                    else:
                        self.gestor_vulnerabilidades.atualizar_status(
                            id_ativo,
                            id_vulnerabilidade,
                            novo_status,
                        )
                        objeto_vulnerabilidade.status = novo_status
                        print("Status alterado com sucesso.")

                elif escolha == 0:
                    return
                else:
                    print("Opção inválida. Tente novamente.")

            except ValueError:
                print("Digite um número válido.")

    def remover_vulnerabilidade(self):
        vulnerabilidade = self._selecionar_vulnerabilidade()
        if vulnerabilidade is None:
            return

        id_ativo, id_vulnerabilidade, _ = vulnerabilidade
        if self._perguntar_sim_nao(
            "Deseja realmente remover esta vulnerabilidade?"
        ):
            self.gestor_vulnerabilidades.remover(
                id_ativo,
                id_vulnerabilidade,
            )
            print("Vulnerabilidade removida com sucesso.")
        else:
            print("Remoção cancelada.")

    def gerenciamento_vulnerabilidades(self):
        acoes = {
            1: self.cadastrar_vulnerabilidade,
            2: self.visualizar_vulnerabilidades,
            3: self.atualizar_vulnerabilidade,
            4: self.remover_vulnerabilidade,
        }

        while True:
            print("\nGERENCIAMENTO DE VULNERABILIDADES")
            print("1 - Cadastrar vulnerabilidade")
            print("2 - Visualizar vulnerabilidades")
            print("3 - Atualizar vulnerabilidade")
            print("4 - Remover vulnerabilidade")
            print("0 - Voltar")

            try:
                escolha = int(input("Digite a opção: "))
            except ValueError:
                print("Digite um número válido.")
                continue

            if escolha == 0:
                return
            acao = acoes.get(escolha)
            if acao is None:
                print("Opção inválida. Tente novamente.")
                continue
            acao()

    def _selecionar_vulnerabilidade(self):
        id_ativo = self.interacao.escolher_ativo_por_responsavel()
        if id_ativo is None:
            return None

        vulnerabilidades = self.gestor_vulnerabilidades.listar_por_ativo(
            id_ativo
        )
        if not vulnerabilidades:
            print("Este ativo não possui vulnerabilidades cadastradas.")
            return None

        print("\nVULNERABILIDADES DO ATIVO")
        for id_vulnerabilidade, vulnerabilidade in vulnerabilidades:
            self._exibir_vulnerabilidade(id_vulnerabilidade, vulnerabilidade)

        while True:
            try:
                id_vulnerabilidade = int(
                    input("Digite o ID da vulnerabilidade: ")
                )
            except ValueError:
                print("Digite um número inteiro válido.")
                continue

            objeto_vulnerabilidade = self.gestor_vulnerabilidades.buscar(
                id_ativo,
                id_vulnerabilidade,
            )
            if objeto_vulnerabilidade is not None:
                return id_ativo, id_vulnerabilidade, objeto_vulnerabilidade

            print("Vulnerabilidade não encontrada.")

    @staticmethod
    def _exibir_vulnerabilidade(id_vulnerabilidade, vulnerabilidade):
        print(
            id_vulnerabilidade,
            "- Severidade:",
            vulnerabilidade.severidade.name,
            "| Status:",
            vulnerabilidade.status.name,
            "| Descrição:",
            vulnerabilidade.descricao,
        )

    @staticmethod
    def _perguntar_sim_nao(pergunta):
        while True:
            print(f"\n{pergunta}\n1 - Sim\n2 - Não")
            try:
                escolha = int(input("Digite a opção: "))
            except ValueError:
                print("Digite um número válido.")
                continue

            if escolha == 1:
                return True
            if escolha == 2:
                return False
            print("Opção inválida. Tente novamente.")


_console_vulnerabilidades = VulnerabilidadesConsole()


def cadastrar_vulnerabilidade():
    return _console_vulnerabilidades.cadastrar_vulnerabilidade()


def visualizar_vulnerabilidades():
    return _console_vulnerabilidades.visualizar_vulnerabilidades()


def atualizar_vulnerabilidade():
    return _console_vulnerabilidades.atualizar_vulnerabilidade()


def remover_vulnerabilidade():
    return _console_vulnerabilidades.remover_vulnerabilidade()


def gerenciamento_vulnerabilidades():
    return _console_vulnerabilidades.gerenciamento_vulnerabilidades()
