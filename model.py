import requests
from requests.exceptions import ConnectionError
import logging
from mapeamento import * 
from DAO import *
from sqlalchemy import *
from datetime import datetime
from decimal import *
import time

class DB:
    @staticmethod
    def insert(obj):
        try:
            session = DAO.getSession()
            DAO.insert(session, obj)
            session.commit()
            session.close()
            return 1
        except:
            return 0

    @staticmethod
    def select_user(user_id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            user = DAOUser.select(session, user_id)  # Assuming you have a select method in DAOUser
            session.commit()
            session.close()
            return user
        except:
            return 0


    def selectStream(id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            stream = DAOStream.select(session, id)
            session.commit()
            session.close()
            return stream
        except:
            return 0
        
    @staticmethod
    def get_user_ids_from_users():
        try:
            session = DAO.getSession()
            user_ids = DAOUser.get_user_ids(session)  # Assuming you have a get_user_ids method in DAOUser
            session.commit()
            session.close()
            return user_ids
        except:
            return []

    # Adicione uma função para inserir canais na tabela
    @staticmethod
    def insert_channel(obj):
        try:
            session = DAO.getSession()
            DAO.insert(session, obj)  # Assuming you have an insert method in DAO
            session.commit()
            session.close()
            return 1
        except Exception as e:
            print(f"Erro durante a inserção do canal: {str(e)}")
            return 0

    @staticmethod
    def selectChannel(channel_id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            channel = DAOChannel.select(session, channel_id)  # Assuming you have a select method in DAOChannel
            session.commit()
            session.close()
            return channel
        except:
            return 0
        
    @staticmethod
    def insert_poll(obj):
        try:
            session = DAO.getSession()
            DAO.insert(session, obj)
            session.commit()
            session.close()
            return 1
        except Exception as e:
            print(f"Erro durante a inserção da enquete: {str(e)}")
            return 0

    @staticmethod
    def select_poll(poll_id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            poll = DAOPolls.select(session, poll_id)
            session.commit()
            session.close()
            return poll
        except:
            return 0

    @staticmethod
    def get_broadcaster_ids_from_canais():
        try:
            session = DAO.getSession()
            channel_id = DAOChannel.get_broadcaster_ids(session)  # Assuming you have a get_broadcaster_ids method in DAOChannel
            session.commit()
            session.close()
            return channel_id
        except:
            return []
    
class API:
    def __init__(self):
        self.client_id = 'qphncqmutk6rmxx5dgbrihjmxzh03d'
        self.client_secret = 'zozuslb1mq6vfph841e9v5wpcjm73f'

    # Obter o token de acesso
    def get_app_access_token(self):
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, params=params)
        data = response.json()
        return data.get('access_token')

    # Altere a função get_users para chamar get_broadcaster_names e imprimir os nomes retornados
    def get_users(self, token_acesso):
        # Chame a função para obter os nomes dos transmissores
        broadcaster_names = self.get_broadcaster_names(token_acesso)

        # Divida a lista de logins em lotes de 100
        batches = [broadcaster_names[i:i + 100] for i in range(0, len(broadcaster_names), 100)]

        for batch in batches:
            url = 'https://api.twitch.tv/helix/users'
            
            # Corrija o parâmetro para aceitar uma lista de logins
            params = {
                'login': batch
            }

            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {token_acesso}'
            }

            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            # Adicione prints para visualizar os dados retornados pela API Twitch
            #print(data)

            for usuario in data.get('data', []):
                userObj = Usuario(user_id=usuario.get("id"),
                                login=usuario.get("login"),
                                display_name=usuario.get("display_name"),
                                user_type=usuario.get("type"),
                                broadcaster_type=usuario.get("broadcaster_type"),
                                description=usuario.get("description"),
                                email=usuario.get("email"),
                                created_at=usuario.get("created_at"))

                # Adicione prints para verificar os dados do usuário
                #print(f"Usuário: {userObj.user_id}, Login: {userObj.login}")

                # Verifica se o usuário já foi cadastrado
                check = DB.select_user(userObj.user_id)

                # Se não foi cadastrado, inserimos
                if not check:
                    DB.insert(userObj)
                # Se foi cadastrado, printamos uma mensagem
                #else:
                    #print(f"Usuário: {userObj.user_id} já cadastrado!")

    # Adicione uma função para obter os nomes dos transmissores
    def get_broadcaster_names(self, token_acesso):
        total_streams = 4000
        batch_size = 100
        broadcaster_names = []

        url = 'https://api.twitch.tv/helix/streams'

        # Variável para armazenar o cursor para a próxima página de resultados
        cursor = None

        for _ in range(total_streams // batch_size):
            params = {
                'first': batch_size,
                'language': 'pt',
                'after': cursor  # Adiciona o cursor à requisição para obter os próximos registros
            }

            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {token_acesso}'
            }

            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            # Adicione prints para visualizar os dados retornados pela API Twitch
            #print(data)

            # Certifique-se de converter para minúsculas antes de adicionar à lista
            batch_names = [stream.get("user_login").lower() for stream in data.get('data', [])]
            broadcaster_names.extend(batch_names)

            # Atualiza o cursor para a próxima página de resultados
            cursor = data.get('pagination', {}).get('cursor')

            # Adicione prints para visualizar os nomes dos transmissores do lote
            #print("Batch Broadcaster Names:", batch_names)

        # Adicione prints para visualizar a lista final de nomes dos transmissores
        #print("Total Broadcaster Names:", broadcaster_names)

        return broadcaster_names

        
    # Faz uma solicitação para obter informações sobre as streams
    def get_streams(self, token_acesso):
        url = 'https://api.twitch.tv/helix/streams'
        params = {
            'first': 10,
            'language': 'pt'
        }
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {token_acesso}'
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        #print(data)  # Adicione esta linha para visualizar a estrutura dos dados

        for stream in data.get('data', []):
            streamObj = Streams(stream_id = stream.get("id"),
                                broadcaster_name = stream.get("user_name"),
                                title = stream.get("title"),
                                started_at = stream.get("started_at"),
                                viewer_count = stream.get("viewer_count"),
                                stream_lang = stream.get("language"))
 
            # verifica se o genero já foi cadastrado
            check = DB.selectStream(streamObj.stream_id)
            streamID = streamObj.stream_id

            # Debug
            #print(f"Stream ID: {streamID}, Check: {check}")

            # se não foi cadastrado, inserimos
            if not check:
                DB.insert(streamObj)
            # se foi cadastrado, printamos uma mensagem
            else:
                print(f"Stream: {streamID} já cadastrada!")

    def get_categorias(self, token_acesso):
        # Lista de consultas de pesquisa que você deseja realizar
        consultas = ['#archery', 'angel of death', ...]  # Adicione suas consultas aqui

        for consulta in consultas:
            # Construa a URL com a consulta atual
            url = 'https://api.twitch.tv/helix/search/categories'
            params = {
                'first': 100,
                'language': 'pt',
                'query': consulta  # Adicione a consulta como um parâmetro
            }
            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {token_acesso}'
            }

            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            #print(data)

            for categoria in data.get('data', []):
                categoriaObj = Canais(category_id=categoria.get("id"),
                                    category_name=categoria.get("name"))

                # verifica se o canal já foi cadastrado
                check = DB.selectChannel(categoriaObj.category_id)
                categoriaID = categoriaObj.category_id

                # se não foi cadastrado, inserimos
                if not check:
                    DB.insert(categoriaObj)
                # se foi cadastrado, printamos uma mensagem
                else:
                    print(f"Canal: {categoriaID} já cadastrada!")
                    
    def get_user_ids_from_database(self):
        return DB.get_user_ids_from_users()
    
    def get_canais(self, token_acesso):
        # Obtém os user_ids da tabela de usuários
        user_ids_from_db = self.get_user_ids_from_database()

        # Verifica se há user_ids para evitar uma requisição desnecessária se a lista estiver vazia
        if user_ids_from_db:
            #print(f"User IDs from database: {user_ids_from_db}")

            url = 'https://api.twitch.tv/helix/channels'

            for batch in [user_ids_from_db[i:i + 100] for i in range(0, len(user_ids_from_db), 100)]:
                #print(f"Processing batch: {batch}")

                params = {
                    'first': 100,
                    'language': 'pt',
                    'broadcaster_id': batch
                }
                headers = {
                    'Client-ID': self.client_id,
                    'Authorization': f'Bearer {token_acesso}'
                }

                response = requests.get(url, params=params, headers=headers)
                data = response.json()

                #print(data)

                for canal in data.get('data', []):
                    canalObj = Canais(
                        channel_id=canal.get("broadcaster_id"),
                        broadcaster_name=canal.get("broadcaster_name"),
                        broadcaster_lang=canal.get("broadcaster_language"),
                        game_name=canal.get("game_name")
                    )

                    # verifica se o canal já foi cadastrado
                    check = DB.selectChannel(canalObj.channel_id)
                    canalID = canalObj.channel_id

                    # se não foi cadastrado, inserimos
                    if not check:
                        result = DB.insert_channel(canalObj)
                        #if result:
                            #print(f"Canal: {canalID} inserido com sucesso!")
                        #else:
                            #print(f"Erro ao inserir o canal: {canalID}")
                    # se foi cadastrado, printamos uma mensagem
                    #else:
                        #print(f"Canal: {canalID} já cadastrado!")
        else:
            print("Lista de user_ids está vazia. Nenhuma solicitação será feita.")

    def get_broadcaster_ids_from_database(self):
        return DB.get_broadcaster_ids_from_canais()

    def get_polls(self, token_acesso):
        if not token_acesso:    
            return print("Token de acesso ausente. Forneça um token válido.") 
        # Obtém os broadcaster_ids (channel_id) da tabela de canais
        broadcaster_ids_from_db = self.get_broadcaster_ids_from_database()

        # Verifica se há broadcaster_ids para evitar uma requisição desnecessária se a lista estiver vazia
        if broadcaster_ids_from_db:
            #print(f"Broadcaster IDs from database for polls: {broadcaster_ids_from_db}")

            url = 'https://api.twitch.tv/helix/polls'

            for batch in [broadcaster_ids_from_db[i:i + 100] for i in range(0, len(broadcaster_ids_from_db), 100)]:
                #print(f"Processing poll batch: {batch}")

                params = {
                    'broadcaster_id': batch
                }
                headers = {
                    'Client-ID': self.client_id,
                    'Authorization': f'Bearer {token_acesso}'
                }

                response = requests.get(url, params=params, headers=headers)
                data = response.json()

                # Adicione prints para visualizar os dados retornados pela API Twitch
                #print(data)

                for poll_data in data.get('data', []):
                    poll_obj = Polls(
                        poll_id=poll_data.get("id"),
                        title=poll_data.get("title"),
                        status=poll_data.get("status"),
                        started_at=poll_data.get("started_at"),
                        ended_at=poll_data.get("ended_at"),
                        broadcaster_id=poll_data.get("broadcaster_id")
                    )

                    # Verifica se a enquete já foi cadastrada
                    check = DB.select_poll(poll_obj.poll_id)
                    poll_id = poll_obj.poll_id

                    # Adicione prints para visualizar informações durante o processo
                    #print(f"Poll Data: {poll_data}")
                    #print(f"Poll ID: {poll_id}, Check: {check}")

                    # Se não foi cadastrada, inserimos
                    if not check:
                        result = DB.insert_poll(poll_obj)
                        if result:
                            print(f"Poll: {poll_id} inserida com sucesso!")
                        else:
                            print(f"Erro ao inserir a enquete: {poll_id}")
                    # Se foi cadastrada, printamos uma mensagem
                    else:
                        print(f"Poll: {poll_id} já cadastrada!")