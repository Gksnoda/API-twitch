import requests
from config import DATABASES, CHAVE_DE_ACESSO_API


def obter_dados_da_api(chave_acesso):
    url_api = 'https://api.twitch.tv/helix/users'
    
    headers = {
        'Authorization': f'Bearer {chave_acesso}',
    }

    response = requests.get(url_api, headers=headers)

    if response.status_code == 200:
        dados_completos = response.json()

        # Selecione apenas os dados desejados
        dados_selecionados = {
            'campo1': dados_completos['campo1'],
            'campo2': dados_completos['campo2'],
            # Adicione mais campos conforme necessário
        }

        return dados_selecionados
    else:
        response.raise_for_status()
