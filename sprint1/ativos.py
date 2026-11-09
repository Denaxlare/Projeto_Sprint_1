from . import modelos as estado
from .modelos import (
    BancoDeDados,
    DispositivoMovel,
    PortalCliente,
    Severidade,
    StatusAtivo,
    StatusTratamento,
    TipoAtivo,
    EstacaoTrabalho,
)
from .auxiliares import InteracaoConsole
from .gestores import GestorAtivos, GestorVulnerabilidades


class AtivosConsole:
    def __init__(
        self,
        gestor_ativos=None,
        gestor_vulnerabilidades=None,
        interacao=None,
    ):
        self.gestor_ativos = gestor_ativos or GestorAtivos(
            estado.repositorio_ativos
        )
        self.gestor_vulnerabilidades = (
            gestor_vulnerabilidades
            or GestorVulnerabilidades(estado.repositorio_ativos)
        )
        self.interacao = interacao or InteracaoConsole(self.gestor_ativos)

    def cadastrar_ativo(self):
        while True:
            try:
                id_ativo = int(input("Digite o ID do ativo: "))

                if self.gestor_ativos.buscar_por_id(id_ativo) is not None:
                    print("ID já cadastrado. Digite outro.")
                    continue

                break

            except ValueError:
                print("Digite um número inteiro válido.")

        while True:
            hostname = input("Digite o Hostname/Nome: ").strip()

            if not hostname:
                print("O Hostname/Nome não pode ficar vazio.")
                continue

            if self.gestor_ativos.buscar_por_hostname(hostname) is not None:
                print("Esse Hostname/Nome já está cadastrado. Digite outro.")
                continue

            break

        responsavel = self.interacao.escolher_opcao(estado.responsaveis)
        tipo_ativo = self.interacao.escolher_enum(TipoAtivo)

        setor = self._solicitar_texto_obrigatorio(
            "Digite o setor do ativo: ",
            "O setor do ativo não pode ficar vazio.",
        )
        descricao = self._solicitar_texto_obrigatorio(
            "Digite a descrição do ativo: ",
            "A descrição do ativo não pode ficar vazia.",
        )
        detalhes = self._coletar_detalhes_tipo(tipo_ativo)

        self.gestor_ativos.cadastrar(
            id_ativo,
            hostname,
            responsavel,
            tipo_ativo,
            StatusAtivo.ATIVO,
            setor,
            descricao,
            detalhes,
        )

        while True:
            print("\nDeseja cadastrar vulnerabilidades agora?")
            print("1 - Sim")
            print("2 - Não")

            try:
                escolha = int(input("Digite a opção: "))

                if escolha == 1:
                    break

                if escolha == 2:
                    print("Ativo cadastrado com sucesso.")
                    return

                print("Opção inválida. Tente novamente.")

            except ValueError:
                print("Digite um número válido.")

        while True:
            severidade = self.interacao.escolher_enum(Severidade)
            status_tratamento = self.interacao.escolher_enum(StatusTratamento)
            descricao_vulnerabilidade = input(
                "Digite a descrição da vulnerabilidade (opcional): "
            ).strip()

            id_vulnerabilidade = self.gestor_vulnerabilidades.cadastrar(
                id_ativo,
                severidade,
                status_tratamento,
                descricao_vulnerabilidade,
            )

            print("Vulnerabilidade cadastrada com sucesso.")
            print("ID da vulnerabilidade:", id_vulnerabilidade)

            if not self._perguntar_sim_nao("Deseja cadastrar outra?"):
                break

        print("Ativo cadastrado com sucesso.")

    def _coletar_detalhes_tipo(self, tipo_ativo):
        if tipo_ativo == TipoAtivo.ESTACAO_TRABALHO:
            return {
                "sistema_operacional": input(
                    "Digite o sistema operacional: "
                ).strip(),
                "antivirus_instalado": self._perguntar_sim_nao(
                    "O antivírus está instalado?"
                ),
            }
        if tipo_ativo == TipoAtivo.DISPOSITIVO_MOVEL:
            return {
                "numero_linha": input("Digite o número da linha: ").strip(),
                "possui_bloqueio_remoto": self._perguntar_sim_nao(
                    "Possui bloqueio remoto?"
                ),
            }
        if tipo_ativo == TipoAtivo.BANCO_DE_DADOS:
            return {
                "sistema_gerenciamento_banco_dados": input(
                    "Digite o sistema de gerenciamento do banco de dados: "
                ).strip(),
                "contem_dados_sensiveis": self._perguntar_sim_nao(
                    "Contém dados sensíveis?"
                ),
            }
        if tipo_ativo == TipoAtivo.PORTAL_CLIENTE:
            return {
                "url": input("Digite a URL do portal: ").strip(),
                "possui_certificado_ssl": self._perguntar_sim_nao(
                    "Possui certificado SSL?"
                ),
            }
        raise ValueError(f"Tipo de ativo não suportado: {tipo_ativo}")

    @staticmethod
    def _solicitar_texto_obrigatorio(prompt, mensagem_erro):
        while True:
            valor = input(prompt).strip()
            if valor:
                return valor
            print(mensagem_erro)

    @staticmethod
    def _perguntar_sim_nao(pergunta):
        while True:
            print(f"{pergunta}\n1 - Sim\n2 - Não")
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

    def consultar_por_id(self):
        while True:
            try:
                id_ativo = int(input("Digite o ID do ativo: "))
                ativo = self.gestor_ativos.buscar_por_id(id_ativo)
                if ativo is not None:
                    print("\nATIVO ENCONTRADO")
                    ativo.exibir_detalhes()
                    break
                print("Ativo não encontrado.")

            except ValueError:
                print("Digite um número inteiro válido.")

    def consultar_por_hostname(self):
        hostname = input("Digite o Hostname: ").strip()

        if not hostname:
            print("O Hostname não pode ficar vazio.")
            return

        ativo = self.gestor_ativos.buscar_por_hostname(hostname)
        if ativo is not None:
            print("\nATIVO ENCONTRADO")
            ativo.exibir_detalhes()
            return

        print("Ativo não encontrado.")

    def consultar_ativos(self):
        while True:
            print("\nCONSULTA DE ATIVOS")
            print("1 - Consultar por ID")
            print("2 - Consultar por Hostname")
            print("0 - Voltar")

            try:
                escolha = int(input("Digite a opção: "))

                if escolha == 1:
                    self.consultar_por_id()
                elif escolha == 2:
                    self.consultar_por_hostname()
                elif escolha == 0:
                    break
                else:
                    print("Opção inválida. Tente novamente.")

            except ValueError:
                print("Digite um número válido.")

    def atualizar_ativo(self):
        while True:
            try:
                id_ativo = int(input("Digite o ID do ativo: "))
                ativo = self.gestor_ativos.buscar_por_id(id_ativo)
                if ativo is not None:
                    break
                print("Ativo não encontrado.")

            except ValueError:
                print("Digite um número inteiro válido.")

        while True:
            print("\nATUALIZAÇÃO DE ATIVO")
            print("1 - Alterar responsável")
            print("2 - Alterar status do ativo")
            print("0 - Voltar")

            try:
                escolha = int(input("Digite a opção: "))

                if escolha == 1:
                    novo_responsavel = self.interacao.escolher_opcao(
                        estado.responsaveis
                    )

                    if novo_responsavel == ativo.responsavel:
                        print("O responsável selecionado já é o responsável atual.")
                    else:
                        self.gestor_ativos.atualizar_responsavel(
                            id_ativo,
                            novo_responsavel,
                        )
                        print("Responsável alterado com sucesso.")

                elif escolha == 2:
                    novo_status = self.interacao.escolher_enum(StatusAtivo)

                    if novo_status == ativo.status:
                        print("O status selecionado já é o status atual.")
                    else:
                        self.gestor_ativos.atualizar_status(
                            id_ativo,
                            novo_status,
                        )
                        print("Status alterado com sucesso.")

                elif escolha == 0:
                    break
                else:
                    print("Opção inválida. Tente novamente.")

            except ValueError:
                print("Digite um número válido.")

    def remover_ativo(self):
        while True:
            try:
                id_ativo = int(input("Digite o ID do ativo: "))
                ativo = self.gestor_ativos.buscar_por_id(id_ativo)
                if ativo is None:
                    print("Ativo não encontrado.")
                    continue

                print("\nATIVO ENCONTRADO")
                print("Hostname:", ativo.hostname)
                print("Responsável:", ativo.responsavel)

                if self._perguntar_sim_nao(
                    "Deseja realmente excluir este ativo?"
                ):
                    self.gestor_ativos.remover(id_ativo)
                    print("Ativo excluído com sucesso.")
                else:
                    print("Exclusão cancelada.")
                return

            except ValueError:
                print("Digite um número inteiro válido.")


_console_ativos = AtivosConsole()


def cadastrar_ativo():
    return _console_ativos.cadastrar_ativo()


def consultar_por_id():
    return _console_ativos.consultar_por_id()


def consultar_por_hostname():
    return _console_ativos.consultar_por_hostname()


def consultar_ativos():
    return _console_ativos.consultar_ativos()


def atualizar_ativo():
    return _console_ativos.atualizar_ativo()


def remover_ativo():
    return _console_ativos.remover_ativo()
