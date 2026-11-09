from enum import Enum


class TipoAtivo(Enum):
    ESTACAO_TRABALHO = 1
    DISPOSITIVO_MOVEL = 2
    BANCO_DE_DADOS = 3
    PORTAL_CLIENTE = 4


class StatusAtivo(Enum):
    ATIVO = 1
    INATIVO = 2
    EM_MANUTENCAO = 3


class Severidade(Enum):
    SEGURA = 1
    BAIXA = 2
    MEDIA = 3
    ALTA = 4
    CRITICA = 5


class StatusTratamento(Enum):
    ABERTA = 1
    EM_TRATAMENTO = 2
    CORRIGIDA = 3
    ACEITA_COMO_RISCO = 4


class Vulnerabilidade:
    def __init__(
        self,
        severidade,
        status,
        descricao="",
    ):
        self.severidade = severidade
        self.status = status
        self.descricao = descricao

    @classmethod
    def from_dict(cls, dados):
        return cls(
            Severidade[dados["severidade"]],
            StatusTratamento[dados["status"]],
            dados.get("descricao", ""),
        )


class Ativo:
    def __init__(self, id_ativo, hostname, responsavel, tipo, status=StatusAtivo.ATIVO, setor="", descricao=""):
        self.id = id_ativo
        self.hostname = hostname
        self.responsavel = responsavel
        self.tipo = tipo
        self.status = status
        self.setor = setor
        self.descricao = descricao
        self._vulnerabilidades = {}

    @classmethod
    def criar(cls, id_ativo, hostname, responsavel, tipo, status=StatusAtivo.ATIVO,
              setor="", descricao="", **detalhes):
        classes_por_tipo = {
            TipoAtivo.ESTACAO_TRABALHO: EstacaoTrabalho,
            TipoAtivo.DISPOSITIVO_MOVEL: DispositivoMovel,
            TipoAtivo.BANCO_DE_DADOS: BancoDeDados,
            TipoAtivo.PORTAL_CLIENTE: PortalCliente,
        }
        classe_ativo = classes_por_tipo[tipo]
        return classe_ativo(
            id_ativo,
            hostname,
            responsavel,
            status,
            setor,
            descricao,
            **detalhes,
        )

    @classmethod
    def from_dict(cls, id_ativo, dados):
        tipo = TipoAtivo[dados["tipo"]]

        detalhes_por_tipo = {
            TipoAtivo.ESTACAO_TRABALHO: (
                "sistema_operacional",
                "antivirus_instalado",
            ),
            TipoAtivo.DISPOSITIVO_MOVEL: (
                "numero_linha",
                "possui_bloqueio_remoto",
            ),
            TipoAtivo.BANCO_DE_DADOS: (
                "sistema_gerenciamento_banco_dados",
                "contem_dados_sensiveis",
            ),
            TipoAtivo.PORTAL_CLIENTE: ("url", "possui_certificado_ssl"),
        }
        detalhes = {
            nome: dados[nome]
            for nome in detalhes_por_tipo[tipo]
            if nome in dados
        }
        return cls.criar(
            id_ativo,
            dados["hostname"],
            dados["responsavel"],
            tipo,
            StatusAtivo[dados["status"]],
            dados.get("setor", ""),
            dados.get("descricao", ""),
            **detalhes,
        )

    def adicionar_vulnerabilidade(self, id_vulnerabilidade, vulnerabilidade):
        if id_vulnerabilidade in self._vulnerabilidades:
            raise ValueError("ID de vulnerabilidade já cadastrado neste ativo.")
        self._vulnerabilidades[id_vulnerabilidade] = vulnerabilidade

    def buscar_vulnerabilidade(self, id_vulnerabilidade):
        return self._vulnerabilidades.get(id_vulnerabilidade)

    def listar_vulnerabilidades(self):
        return tuple(self._vulnerabilidades.items())

    def remover_vulnerabilidade(self, id_vulnerabilidade):
        return self._vulnerabilidades.pop(id_vulnerabilidade, None)

    def to_dict(self):
        return {
            "hostname": self.hostname,
            "responsavel": self.responsavel,
            "tipo": self.tipo.name,
            "status": self.status.name,
            "setor": self.setor,
            "descricao": self.descricao,
            **self._detalhes_dict(),
            "vulnerabilidades": {
                vid: {
                    "severidade": v.severidade.name,
                    "status": v.status.name,
                    "descricao": v.descricao,
                }
                for vid, v in self.listar_vulnerabilidades()
            },
        }

    def _detalhes_dict(self):
        return {}

    def exibir_detalhes(self):
        print(f"\nID: {self.id}")
        print(f"Hostname: {self.hostname}")
        print(f"Responsável: {self.responsavel}")
        print(f"Tipo: {self.tipo.name}")
        print(f"Status: {self.status.name}")
        print(f"Setor: {self.setor}")
        print(f"Descrição: {self.descricao}")
        print(f"Quantidade de vulnerabilidades: {len(self.listar_vulnerabilidades())}")


class EstacaoTrabalho(Ativo):
    def __init__(self, id_ativo, hostname, responsavel, status=StatusAtivo.ATIVO, setor="", descricao="", sistema_operacional="", antivirus_instalado=True):
        super().__init__(id_ativo, hostname, responsavel, TipoAtivo.ESTACAO_TRABALHO, status, setor, descricao)
        self.sistema_operacional = sistema_operacional
        self.antivirus_instalado = antivirus_instalado

    def to_dict(self):
        return super().to_dict()

    def _detalhes_dict(self):
        return {
            "sistema_operacional": self.sistema_operacional,
            "antivirus_instalado": self.antivirus_instalado,
        }

    def exibir_detalhes(self):
        super().exibir_detalhes()
        print(f"Sistema Operacional: {self.sistema_operacional}")
        print(f"Antivírus Instalado: {'Sim' if self.antivirus_instalado else 'Não'}")


class DispositivoMovel(Ativo):
    def __init__(self, id_ativo, hostname, responsavel, status=StatusAtivo.ATIVO, setor="", descricao="", numero_linha="", possui_bloqueio_remoto=True):
        super().__init__(id_ativo, hostname, responsavel, TipoAtivo.DISPOSITIVO_MOVEL, status, setor, descricao)
        self.numero_linha = numero_linha
        self.possui_bloqueio_remoto = possui_bloqueio_remoto

    def to_dict(self):
        return super().to_dict()

    def _detalhes_dict(self):
        return {
            "numero_linha": self.numero_linha,
            "possui_bloqueio_remoto": self.possui_bloqueio_remoto,
        }

    def exibir_detalhes(self):
        super().exibir_detalhes()
        print(f"Número da Linha: {self.numero_linha}")
        print(f"Bloqueio Remoto Ativo: {'Sim' if self.possui_bloqueio_remoto else 'Não'}")


class BancoDeDados(Ativo):
    def __init__(self, id_ativo, hostname, responsavel, status=StatusAtivo.ATIVO, setor="", descricao="", sistema_gerenciamento_banco_dados="", contem_dados_sensiveis=True):
        super().__init__(id_ativo, hostname, responsavel, TipoAtivo.BANCO_DE_DADOS, status, setor, descricao)
        self.sistema_gerenciamento_banco_dados = sistema_gerenciamento_banco_dados
        self.contem_dados_sensiveis = contem_dados_sensiveis

    def to_dict(self):
        return super().to_dict()

    def _detalhes_dict(self):
        return {
            "sistema_gerenciamento_banco_dados": self.sistema_gerenciamento_banco_dados,
            "contem_dados_sensiveis": self.contem_dados_sensiveis,
        }

    def exibir_detalhes(self):
        super().exibir_detalhes()
        print(f"SGBD: {self.sistema_gerenciamento_banco_dados}")
        print(f"Contém Dados Sensíveis (LGPD): {'Sim' if self.contem_dados_sensiveis else 'Não'}")


class PortalCliente(Ativo):
    def __init__(self, id_ativo, hostname, responsavel, status=StatusAtivo.ATIVO, setor="", descricao="", url="", possui_certificado_ssl=True):
        super().__init__(id_ativo, hostname, responsavel, TipoAtivo.PORTAL_CLIENTE, status, setor, descricao)
        self.url = url
        self.possui_certificado_ssl = possui_certificado_ssl

    def to_dict(self):
        return super().to_dict()

    def _detalhes_dict(self):
        return {
            "url": self.url,
            "possui_certificado_ssl": self.possui_certificado_ssl,
        }

    def exibir_detalhes(self):
        super().exibir_detalhes()
        print(f"URL: {self.url}")
        print(f"Possui Certificado SSL: {'Sim' if self.possui_certificado_ssl else 'Não'}")

class RepositorioAtivos:
    def __init__(self):
        self._ativos = {}
        self._ids_por_hostname = {}
        self._proximo_id_vulnerabilidade = 1

    @property
    def ativos(self):
        return self._ativos

    @property
    def proximo_id_vulnerabilidade(self):
        return self._proximo_id_vulnerabilidade

    def cadastrar(self, ativo):
        if ativo.id in self._ativos:
            raise ValueError("ID já cadastrado.")

        if ativo.hostname in self._ids_por_hostname:
            raise ValueError("Hostname/Nome já cadastrado.")

        self._ativos[ativo.id] = ativo
        self._ids_por_hostname[ativo.hostname] = ativo.id
        return ativo

    def buscar_por_id(self, id_ativo):
        return self._ativos.get(id_ativo)

    def buscar_por_hostname(self, hostname):
        id_ativo = self._ids_por_hostname.get(hostname)
        if id_ativo is None:
            return None
        return self._ativos[id_ativo]

    def buscar_por_responsavel(self, responsavel):
        return {
            id_ativo: ativo
            for id_ativo, ativo in self._ativos.items()
            if ativo.responsavel == responsavel
        }

    def cadastrar_vulnerabilidade(self, id_ativo, vulnerabilidade):
        ativo = self._ativos[id_ativo]
        id_vulnerabilidade = self._proximo_id_vulnerabilidade
        ativo.adicionar_vulnerabilidade(id_vulnerabilidade, vulnerabilidade)
        self._proximo_id_vulnerabilidade += 1
        return id_vulnerabilidade

    def restaurar_vulnerabilidade(self, id_ativo, id_vulnerabilidade, vulnerabilidade):
        ativo = self._ativos[id_ativo]
        ativo.adicionar_vulnerabilidade(id_vulnerabilidade, vulnerabilidade)

    def remover(self, id_ativo):
        ativo = self._ativos.pop(id_ativo)
        del self._ids_por_hostname[ativo.hostname]
        return ativo

    def limpar(self):
        self._ativos.clear()
        self._ids_por_hostname.clear()
        self._proximo_id_vulnerabilidade = 1

    def restaurar_proximo_id_vulnerabilidade(self, proximo_id):
        self._proximo_id_vulnerabilidade = proximo_id


# ============================================================

responsaveis = ("Camila", "Amanda", "Elaine", "Igor")

repositorio_ativos = RepositorioAtivos()


# ============================================================
