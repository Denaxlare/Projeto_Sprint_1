import modelos as estado
from modelos import Severidade, StatusTratamento
from auxiliares import escolher_enum, escolher_ativo_por_responsavel


def cadastrar_vulnerabilidade():
    id_ativo = escolher_ativo_por_responsavel()

    if id_ativo is None:
        return

    while True:
        severidade = escolher_enum(Severidade)

        status_tratamento = escolher_enum(StatusTratamento)

        estado.ativos[id_ativo].vulnerabilidades[
            estado.proximo_id_vulnerabilidade
        ] = {"severidade": severidade, "status": status_tratamento}

        print("Vulnerabilidade cadastrada com sucesso.")
        print("ID da vulnerabilidade:", estado.proximo_id_vulnerabilidade)

        estado.proximo_id_vulnerabilidade += 1

        while True:
            print("\nDeseja cadastrar outra vulnerabilidade?")
            print("1 - Sim")
            print("2 - Não")

            try:
                escolha = int(input("Digite a opção: "))

                if escolha == 1:
                    break

                elif escolha == 2:
                    return

                else:
                    print("Opção inválida. Tente novamente.")

            except ValueError:
                print("Digite um número válido.")


# ============================================================


def visualizar_vulnerabilidades():
    id_ativo = escolher_ativo_por_responsavel()

    if id_ativo is None:
        return

    vulnerabilidades = estado.ativos[id_ativo].vulnerabilidades

    print("\nVULNERABILIDADES DO ATIVO")

    if not vulnerabilidades:
        print("Este ativo não possui vulnerabilidades cadastradas.")
        return

    for id_vulnerabilidade, vulnerabilidade in vulnerabilidades.items():
        print("\nID:", id_vulnerabilidade)
        print("Severidade:", vulnerabilidade["severidade"].name)
        print("Status:", vulnerabilidade["status"].name)


# ============================================================


def atualizar_vulnerabilidade():
    id_ativo = escolher_ativo_por_responsavel()

    if id_ativo is None:
        return

    vulnerabilidades = estado.ativos[id_ativo].vulnerabilidades

    if not vulnerabilidades:
        print("Este ativo não possui vulnerabilidades cadastradas.")
        return

    print("\nVULNERABILIDADES DO ATIVO")

    for id_vulnerabilidade, vulnerabilidade in vulnerabilidades.items():
        print(
            id_vulnerabilidade,
            "- Severidade:",
            vulnerabilidade["severidade"].name,
            "| Status:",
            vulnerabilidade["status"].name,
        )

    while True:
        try:
            id_vulnerabilidade = int(input("Digite o ID da vulnerabilidade: "))

            if id_vulnerabilidade in vulnerabilidades:
                break

            print("Vulnerabilidade não encontrada.")

        except ValueError:
            print("Digite um número inteiro válido.")

    vulnerabilidade = vulnerabilidades[id_vulnerabilidade]

    while True:
        print("\nATUALIZAÇÃO DE VULNERABILIDADE")
        print("1 - Alterar severidade")
        print("2 - Alterar status de tratamento")
        print("0 - Voltar")

        try:
            escolha = int(input("Digite a opção: "))

            if escolha == 1:
                nova_severidade = escolher_enum(Severidade)

                if nova_severidade == vulnerabilidade["severidade"]:
                    print("A severidade selecionada já é a atual.")
                else:
                    vulnerabilidade["severidade"] = nova_severidade
                    print("Severidade alterada com sucesso.")

            elif escolha == 2:
                novo_status = escolher_enum(StatusTratamento)

                if novo_status == vulnerabilidade["status"]:
                    print("O status selecionado já é o atual.")
                else:
                    vulnerabilidade["status"] = novo_status
                    print("Status alterado com sucesso.")

            elif escolha == 0:
                break

            else:
                print("Opção inválida. Tente novamente.")

        except ValueError:
            print("Digite um número válido.")


# ============================================================


def remover_vulnerabilidade():
    id_ativo = escolher_ativo_por_responsavel()

    if id_ativo is None:
        return

    vulnerabilidades = estado.ativos[id_ativo].vulnerabilidades

    if not vulnerabilidades:
        print("Este ativo não possui vulnerabilidades cadastradas.")
        return

    print("\nVULNERABILIDADES DO ATIVO")

    for id_vulnerabilidade, vulnerabilidade in vulnerabilidades.items():
        print(
            id_vulnerabilidade,
            "- Severidade:",
            vulnerabilidade["severidade"].name,
            "| Status:",
            vulnerabilidade["status"].name,
        )

    while True:
        try:
            id_vulnerabilidade = int(input("Digite o ID da vulnerabilidade: "))

            if id_vulnerabilidade in vulnerabilidades:
                break

            print("Vulnerabilidade não encontrada.")

        except ValueError:
            print("Digite um número inteiro válido.")

    while True:
        print("\nDeseja realmente remover esta vulnerabilidade?")
        print("1 - Sim")
        print("2 - Não")

        try:
            confirmacao = int(input("Digite a opção: "))

            if confirmacao == 1:
                del vulnerabilidades[id_vulnerabilidade]

                print("Vulnerabilidade removida com sucesso.")
                return

            elif confirmacao == 2:
                print("Remoção cancelada.")
                return

            else:
                print("Opção inválida. Tente novamente.")

        except ValueError:
            print("Digite um número válido.")


# ============================================================


def gerenciamento_vulnerabilidades():
    while True:
        print("\nGERENCIAMENTO DE VULNERABILIDADES")
        print("1 - Cadastrar vulnerabilidade")
        print("2 - Visualizar vulnerabilidades")
        print("3 - Atualizar vulnerabilidade")
        print("4 - Remover vulnerabilidade")
        print("0 - Voltar")

        try:
            escolha = int(input("Digite a opção: "))

            if escolha == 1:
                cadastrar_vulnerabilidade()

            elif escolha == 2:
                visualizar_vulnerabilidades()

            elif escolha == 3:
                atualizar_vulnerabilidade()

            elif escolha == 4:
                remover_vulnerabilidade()

            elif escolha == 0:
                break

            else:
                print("Opção inválida. Tente novamente.")

        except ValueError:
            print("Digite um número válido.")


# ============================================================
