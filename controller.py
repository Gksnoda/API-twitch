from model import *
from view import View

class Controller:
    def __init__(self, API):
        self.view = View()
        self.API = API

    def start(self):
        opcao = self.view.start()

        while opcao != 7:
            if opcao == 1:
                token_acesso = self.API.get_app_access_token()
                usuarios = self.API.get_users(token_acesso)

            if opcao == 2:
                token_acesso = self.API.get_app_access_token()
                canais = self.API.get_canais(token_acesso)

            if opcao == 3:
                token_acesso = self.API.get_app_access_token()
                top_games = self.API.get_top_games(token_acesso)

            if opcao == 4:
                token_acesso = self.API.get_app_access_token()
                streams = self.API.get_streams(token_acesso)

            if opcao == 5:
                token_acesso = self.API.get_app_access_token()
                videos = self.API.get_videos(token_acesso)
                
            if opcao == 6:
                print('Tags')

            #else:
                #print("\nOpção inválida.\n")
            
            opcao = self.view.menu()


if __name__ == "__main__":
    # Obtém o app access token
    token_acesso = API()
    controlador = Controller(token_acesso)
    controlador.start()
    