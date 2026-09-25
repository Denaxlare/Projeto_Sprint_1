import sprint1.modelos as estado

def escolher_opcao(opcoes):
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


def escolher_enum(tipo_enum):
    while True:
        for opcao in tipo_enum:
            print(opcao.value, "-", opcao.name)

        try:
            escolha = int(input("Digite um numero: "))
            return tipo_enum(escolha)

        except ValueError:
            print("Opção inválida. Tente novamente.")


def escolher_ativo_por_responsavel():
    responsavel = escolher_opcao(estado.responsaveis)

    ativos_responsavel = {}

    for id_ativo, ativo in estado.ativos.items():
        if ativo["responsavel"] == responsavel:
            ativos_responsavel[id_ativo] = ativo

    if not ativos_responsavel:
        print("Esse responsável não possui estado.ativos cadastrados.")
        return None

    print("\nATIVOS DO RESPONSÁVEL")

    for id_ativo, ativo in ativos_responsavel.items():
        print(id_ativo, "-", ativo["hostname"])

    while True:
        try:
            id_ativo = int(input("Digite o ID do ativo: "))

            if id_ativo in ativos_responsavel:
                return id_ativo

            print("Esse ativo não pertence ao responsável selecionado.")

        except ValueError:
            print("Digite um número inteiro válido.")


# ============================================================
