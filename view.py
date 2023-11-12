class View():
    def start(self):
        return self.menu()

    def menu(self):
        print("Menu:")
        print("1. Chamar a função get_streams")
        print("2. Chamar a função get_canais")
        print("3. Chamar a função get_usuarios")
        print("4. Chamar a função get_polls")
        print("5. Sair")

        # Pegar escolha do usuário
        opcao = int(input("Digite o número da opção desejada: "))
        return opcao
