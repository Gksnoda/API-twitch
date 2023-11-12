from model import *
from view import View

class Controller:
    def __init__(self, API):
        self.view = View()
        self.API = API

    def start(self):
        opcao = self.view.start()

        while opcao != 5:
            if opcao == 1:
                #print('1111111')
                # Obtém informações sobre streams e imprime o resultado
                token_acesso = self.API.get_app_access_token()
                streams = self.API.get_streams(token_acesso)

            if opcao == 2:
                token_acesso = self.API.get_app_access_token()
                canais = self.API.get_canais(token_acesso)
        
            if opcao == 3:
                token_acesso = self.API.get_app_access_token()
                usuarios = self.API.get_users(token_acesso)
            
            if opcao == 4:
                token_acesso = self.API.get_app_access_token()
                polls = self.API.get_polls(token_acesso)

            if opcao == 5:
                print("inserir")
            #else:
            #    print("Opção inválida. Por favor, escolha uma opção válida.")
            opcao = self.view.menu()

if __name__ == "__main__":
    # Obtém o app access token
    token_acesso = API()
    controlador = Controller(token_acesso)
    controlador.start()
    