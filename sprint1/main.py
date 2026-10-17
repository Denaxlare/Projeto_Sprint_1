from ativos import (
    cadastrar_ativo,
    consultar_ativos,
    atualizar_ativo,
    remover_ativo,
)
from vulnerabilidades import gerenciamento_vulnerabilidades
from persistencia import salvar_dados, carregar_dados


def sair():
    salvar_dados()
    print("Programa encerrado.")


# ============================================================
def menu():
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

            if escolha == 1:
                cadastrar_ativo()

            elif escolha == 2:
                consultar_ativos()

            elif escolha == 3:
                atualizar_ativo()

            elif escolha == 4:
                remover_ativo()

            elif escolha == 5:
                gerenciamento_vulnerabilidades()

            elif escolha == 0:
                sair()
                break

            else:
                print("Opção inválida. Tente novamente.")

        except ValueError:
            print("Digite um número válido.")


# ============================================================


def main():
    carregar_dados()
    menu()


if __name__ == "__main__":
    main()
