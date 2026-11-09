from .modelos import Ativo, StatusAtivo, Vulnerabilidade


class GestorAtivos:
    def __init__(self, repositorio):
        self._repositorio = repositorio

    def cadastrar(
        self,
        id_ativo,
        hostname,
        responsavel,
        tipo,
        status=StatusAtivo.ATIVO,
        setor="",
        descricao="",
        detalhes=None,
    ):
        if not setor.strip():
            raise ValueError("O setor do ativo não pode ficar vazio.")
        if not descricao.strip():
            raise ValueError("A descrição do ativo não pode ficar vazia.")

        ativo = Ativo.criar(
            id_ativo,
            hostname,
            responsavel,
            tipo,
            status,
            setor,
            descricao,
            **(detalhes or {}),
        )
        return self._repositorio.cadastrar(ativo)

    def buscar_por_id(self, id_ativo):
        return self._repositorio.buscar_por_id(id_ativo)

    def buscar_por_hostname(self, hostname):
        return self._repositorio.buscar_por_hostname(hostname)

    def buscar_por_responsavel(self, responsavel):
        return self._repositorio.buscar_por_responsavel(responsavel)

    def atualizar_responsavel(self, id_ativo, responsavel):
        ativo = self._repositorio.buscar_por_id(id_ativo)
        if ativo is None:
            return None
        ativo.responsavel = responsavel
        return ativo

    def atualizar_status(self, id_ativo, status):
        ativo = self._repositorio.buscar_por_id(id_ativo)
        if ativo is None:
            return None
        ativo.status = status
        return ativo

    def remover(self, id_ativo):
        return self._repositorio.remover(id_ativo)


class GestorVulnerabilidades:
    def __init__(self, repositorio):
        self._repositorio = repositorio

    def cadastrar(self, id_ativo, severidade, status, descricao=""):
        vulnerabilidade = Vulnerabilidade(severidade, status, descricao)
        return self._repositorio.cadastrar_vulnerabilidade(
            id_ativo,
            vulnerabilidade,
        )

    def listar_por_ativo(self, id_ativo):
        ativo = self._repositorio.buscar_por_id(id_ativo)
        if ativo is None:
            return None
        return ativo.listar_vulnerabilidades()

    def buscar(self, id_ativo, id_vulnerabilidade):
        ativo = self._repositorio.buscar_por_id(id_ativo)
        if ativo is None:
            return None
        return ativo.buscar_vulnerabilidade(id_vulnerabilidade)

    def atualizar_severidade(self, id_ativo, id_vulnerabilidade, severidade):
        vulnerabilidade = self.buscar(id_ativo, id_vulnerabilidade)
        if vulnerabilidade is None:
            return None
        vulnerabilidade.severidade = severidade
        return vulnerabilidade

    def atualizar_status(self, id_ativo, id_vulnerabilidade, status):
        vulnerabilidade = self.buscar(id_ativo, id_vulnerabilidade)
        if vulnerabilidade is None:
            return None
        vulnerabilidade.status = status
        return vulnerabilidade

    def remover(self, id_ativo, id_vulnerabilidade):
        ativo = self._repositorio.buscar_por_id(id_ativo)
        if ativo is None:
            return None
        return ativo.remover_vulnerabilidade(id_vulnerabilidade)
