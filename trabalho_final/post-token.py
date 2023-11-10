import requests

def obter_token_de_acesso():
    url = 'https://id.twitch.tv/oauth2/token'
    
    params = {
        'client_id': 'qphncqmutk6rmxx5dgbrihjmxzh03d',
        'client_secret': 'de0eey6ylbtyxm5oq9wykk2sznftua',
        'grant_type': 'client_credentials',
    }

    response = requests.post(url, data=params)

    if response.status_code == 200:
        # Obter os dados da resposta JSON
        resposta_json = response.json()

        # Extrair os campos específicos da resposta
        access_token = resposta_json.get('access_token')
        expires_in = resposta_json.get('expires_in')
        refresh_token = resposta_json.get('refresh_token')
        scopes = resposta_json.get('scope')
        token_type = resposta_json.get('token_type')

        # Fazer o que for necessário com os dados extraídos
        print(f'Token de Acesso: {access_token}')
        print(f'Expira em: {expires_in} segundos')
        print(f'Refresh Token: {refresh_token}')
        print(f'Scopes: {scopes}')
        print(f'Tipo de Token: {token_type}')

        return access_token
    else:
        response.raise_for_status()

# Chamar a função para obter o token de acesso
token = obter_token_de_acesso()

##Token de Acesso: irmdjdghguse62flus4kdco8lgiq12
##Expira em: 4886520 segundos
##Refresh Token: None
##Scopes: None
##Tipo de Token: bearer