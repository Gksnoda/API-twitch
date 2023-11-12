from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from mapeamento import *
from urllib.parse import quote_plus

# Substitua 'sua_senha' pela senha correta do seu banco de dados
senha_codificada = quote_plus('root')

# Use a senha codificada na URL de conexão


class DAO():
    # Iniciando a sessão com o banco de dados
    def getSession():
        engine = create_engine(f"postgresql+psycopg2://postgres:{senha_codificada}@localhost:5432/BD2_trabalho_Twitch")
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    
    # Método para inserir nas tabelas do banco
    # Dentro da classe DB ou onde você estiver chamando a função insert
    def insert(session, obj):
        try:
            session.add(obj)
            session.commit()
            print("Inserção bem-sucedida")
        except Exception as e:
            session.rollback()
            print(f"Erro durante a inserção: {e}")

        
# DAO's para selects (por id)
class DAOStream:
    def select(session, id):
        stream = session.query(Streams).filter(Streams.id == id).first()
        return stream
    
class DAOChannel:
    @staticmethod
    def insert(session, canal_obj):
        # Exemplo: Inserir dados na tabela de canais
        new_channel = Canais(
            channel_id=canal_obj.channel_id,
            broadcaster_name=canal_obj.broadcaster_name,
            broadcaster_lang=canal_obj.broadcaster_lang,
            game_name=canal_obj.game_name
        )
        session.add(new_channel)

    @staticmethod
    def select(session, channel_id):
        # Exemplo: Selecionar dados da tabela de canais
        return session.query(Canais).filter_by(channel_id=channel_id).first()
    
    @staticmethod
    def get_broadcaster_ids(session):
        try:
            # Modificar para selecionar os channel_id
            broadcaster_ids = session.query(Canais.channel_id).all()
            return [channel_id[0] for channel_id in broadcaster_ids]
        except:
            return []

class DAOUser:
    @staticmethod
    def insert(session: Session, usuario: Usuario):
        session.add(usuario)

    @staticmethod
    def select(session: Session, user_id: str):
        return session.query(Usuario).filter_by(user_id=user_id).first()

    @staticmethod
    def get_user_ids(session: Session):
        # Retorna uma lista de user_ids
        return [result.user_id for result in session.query(Usuario.user_id).all()]
    
class DAOPolls:
    @staticmethod
    def insert(session: Session, poll_obj: Polls):
        session.add(poll_obj)

    @staticmethod
    def select(session: Session, poll_id: str):
        return session.query(Polls).filter_by(poll_id=poll_id).first()