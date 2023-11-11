import requests
from requests.exceptions import ConnectionError

from mapeamento import * 
from DAO import *
from sqlalchemy import *
from datetime import datetime
from decimal import *
import time

class DB:
    def insert(obj):
        try:
            session = DAO.getSession()
            DAO.insert(session, obj)
            session.commit()
            session.close()
            return 1
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
    
class API:
    def __init__(self):
        self.client_id = '4bozg8logk69ww648ugu8tvilmzr6e'
        self.client_secret = 'yfoft881uztzi8gbpjailj02ogycar'

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

    # Faz uma solicitação para obter informações sobre as streams
    def get_streams(self, token_acesso):
        url = 'https://api.twitch.tv/helix/streams'
        params = {
            'first': 10,  # Número de streams que você quer obter (máximo de 100)
            'language': 'pt'
        }
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {token_acesso}'
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        print(data)
        
        for stream in data.get('data'):
            streamObj = Stream(id = stream.get("id"),
                               user_name = stream.get("user_name"))

            # verifica se o genero já foi cadastrado
            check = DB.selectStream(streamObj.id)
            streamID = streamObj.id

            # se não foi cadastrado, inserimos
            if not check:
                DB.insert(streamObj)
            # se foi cadastrado, printamos uma mensagem
            else:
                print(f"Stream: {streamID} já cadastrada!")
        
        #return data.get('data')
    
    
