import sprint1.modelos as estado
from sprint1.modelos import TipoAtivo, StatusAtivo, Severidade, StatusTratamento
from sprint1.auxiliares import escolher_opcao, escolher_enum, escolher_ativo_por_responsavel

def cadastrar_ativo():
    while True:
        try:
            id_ativo = int(input("Digite o ID do ativo: "))

            if id_ativo in estado.ativos:
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

        if hostname in estado.ativos_por_hostname:
            print("Esse Hostname/Nome já está cadastrado. Digite outro.")
            continue

        break

    responsavel = escolher_opcao(estado.responsaveis)

    tipo_ativo = escolher_enum(TipoAtivo)

    status = StatusAtivo.ATIVO

    vulnerabilidades = {}

    estado.ativos[id_ativo] = {
        "hostname": hostname,
        "responsavel": responsavel,
        "tipo": tipo_ativo,
        "status": status,
        "vulnerabilidades": vulnerabilidades
    }

    estado.ativos_por_hostname[hostname] = id_ativo

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
        severidade = escolher_enum(Severidade)

        status_tratamento = escolher_enum(StatusTratamento)

        estado.ativos[id_ativo]["vulnerabilidades"][estado.proximo_id_vulnerabilidade] = {
            "severidade": severidade,
            "status": status_tratamento
        }

        print("Vulnerabilidade cadastrada com sucesso.")

        estado.proximo_id_vulnerabilidade += 1

        continuar = True

        while True:
            print("Deseja cadastrar outra?")
            print("1 - Sim")
            print("2 - Não")

            try:
                outra = int(input("Digite a opção: "))

                if outra == 1:
                    break

                if outra == 2:
                    continuar = False
                    break

                print("Opção inválida. Tente novamente.")

            except ValueError:
                print("Digite um número válido.")

        if not continuar:
            break

    print("Ativo cadastrado com sucesso.")


# ============================================================

def consultar_por_id():
    while True:
        try:
            id_ativo = int(input("Digite o ID do ativo: "))

            if id_ativo in estado.ativos:
                ativo = estado.ativos[id_ativo]

                print("\nATIVO ENCONTRADO")
                print("ID:", id_ativo)
                print("Hostname:", ativo["hostname"])
                print("Responsável:", ativo["responsavel"])
                print("Tipo:", ativo["tipo"].name)
                print("Status:", ativo["status"].name)
                print(
                    "Quantidade de vulnerabilidades:",
                    len(ativo["vulnerabilidades"])
                )

                break

            print("Ativo não encontrado.")

        except ValueError:
            print("Digite um número inteiro válido.")


def consultar_por_hostname():
    hostname = input("Digite o Hostname: ").strip()

    if not hostname:
        print("O Hostname não pode ficar vazio.")
        return

    if hostname in estado.ativos_por_hostname:
        id_ativo = estado.ativos_por_hostname[hostname]

        ativo = estado.ativos[id_ativo]

        print("\nATIVO ENCONTRADO")
        print("ID:", id_ativo)
        print("Hostname:", ativo["hostname"])
        print("Responsável:", ativo["responsavel"])
        print("Tipo:", ativo["tipo"].name)
        print("Status:", ativo["status"].name)
        print(
            "Quantidade de vulnerabilidades:",
            len(ativo["vulnerabilidades"])
        )

        return

    print("Ativo não encontrado.")


def consultar_ativos():
    while True:
        print("\nCONSULTA DE ATIVOS")
        print("1 - Consultar por ID")
        print("2 - Consultar por Hostname")
        print("0 - Voltar")

        try:
            escolha = int(input("Digite a opção: "))

            if escolha == 1:
                consultar_por_id()

            elif escolha == 2:
                consultar_por_hostname()

            elif escolha == 0:
                break

            else:
                print("Opção inválida. Tente novamente.")

        except ValueError:
            print("Digite um número válido.")


# ============================================================

def atualizar_ativo():
    while True:
        try:
            id_ativo = int(input("Digite o ID do ativo: "))

            if id_ativo in estado.ativos:
                ativo = estado.ativos[id_ativo]
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
                novo_responsavel = escolher_opcao(estado.responsaveis)

                if novo_responsavel == ativo["responsavel"]:
                    print(
                        "O responsável selecionado já é o "
                        "responsável atual."
                    )
                else:
                    ativo["responsavel"] = novo_responsavel
                    print("Responsável alterado com sucesso.")

            elif escolha == 2:
                novo_status = escolher_enum(StatusAtivo)

                if novo_status == ativo["status"]:
                    print(
                        "O status selecionado já é o status atual."
                    )
                else:
                    ativo["status"] = novo_status
                    print("Status alterado com sucesso.")

            elif escolha == 0:
                break

            else:
                print("Opção inválida. Tente novamente.")

        except ValueError:
            print("Digite um número válido.")


# ============================================================

def remover_ativo():
    while True:
        try:
            id_ativo = int(input("Digite o ID do ativo: "))

            if id_ativo in estado.ativos:
                ativo = estado.ativos[id_ativo]

                print("\nATIVO ENCONTRADO")
                print("Hostname:", ativo["hostname"])
                print("Responsável:", ativo["responsavel"])

                while True:
                    print("\nDeseja realmente excluir este ativo?")
                    print("1 - Sim")
                    print("2 - Não")

                    try:
                        confirmacao = int(input("Digite a opção: "))

                        if confirmacao == 1:
                            del estado.ativos_por_hostname[ativo["hostname"]]
                            del estado.ativos[id_ativo]

                            print("Ativo excluído com sucesso.")
                            return

                        elif confirmacao == 2:
                            print("Exclusão cancelada.")
                            return

                        else:
                            print("Opção inválida. Tente novamente.")

                    except ValueError:
                        print("Digite um número válido.")

            else:
                print("Ativo não encontrado.")

        except ValueError:
            print("Digite um número inteiro válido.")


# ============================================================
