from enum import Enum


class TipoAtivo(Enum):
    PC = 1
    IOT = 2
    ROTEADOR = 3
    BANCO_DE_DADOS = 4


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


class Ativo:
    def __init__(
        self,
        id_ativo,
        hostname,
        responsavel,
        tipo,
        status=StatusAtivo.ATIVO
    ):
        self.id = id_ativo
        self.hostname = hostname
        self.responsavel = responsavel
        self.tipo = tipo
        self.status = status
        self.vulnerabilidades = {}

# ============================================================

responsaveis = ("Camila", "Amanda", "Elaine", "Igor")

ativos = {}

ativos_por_hostname = {}

proximo_id_vulnerabilidade = 1


# ============================================================
