DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'BD2_trabalho_Twitch',
        'USER': 'user_dba',
        'PASSWORD': 'senha123',
        'HOST': 'localhost',  # Ou o host do seu banco de dados
        'PORT': '5432',  # Porta do banco de dados (deixe vazio para usar a porta padrão)
    }
}

CHAVE_DE_ACESSO_API = 'de0eey6ylbtyxm5oq9wykk2sznftua'

##scurl -X GET "https://id.twitch.tv/oauth2/token"^
##-H "Content-Type: application/x-www-form-urlencoded"^
##-d "client_id=<qphncqmutk6rmxx5dgbrihjmxzh03d>&client_secret=<>"

##curl -X GET "https://api.twitch.tv/helix/users"^
##-H "Authorization: Bearer de0eey6ylbtyxm5oq9wykk2sznftua"^
##-H "Client-Id: qphncqmutk6rmxx5dgbrihjmxzh03d"

##client_id=qphncqmutk6rmxx5dgbrihjmxzh03d&client_secret=de0eey6ylbtyxm5oq9wykk2sznftua&grant_type=client_credentials