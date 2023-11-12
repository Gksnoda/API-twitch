class View():
    def start(self):
        return self.menu()

    def menu(self):
        print("Menu:")
        print("1. Popular a tabela 'Usuários'")
        print("2. Popular a tabela 'Canais'")
        print("3. Popular a tabela 'Polls'")
        print("4. Popular a tabela 'Streams'")
        print("5. Popular a tabela 'Categories'")
        print("6. Popular a tabela 'Tags'")
        print("7. Popular a tabela 'Stream_Categories'")
        print("8. Sair")

        # Pegar escolha do usuário
        opcao = int(input("Digite o número da opção desejada: "))
        return opcao
