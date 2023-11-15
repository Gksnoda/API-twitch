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
        engine = create_engine(f"postgresql+psycopg2://postgres:{senha_codificada}@localhost:5432/BD2_Twitch")
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


class DAOCategory:
    @staticmethod
    def select(session, id):
        category = session.query(Category).filter(Category.category_id == id).first()
        return category

    @staticmethod
    def get_category_names(session):
        try:
            return [category_name[0] for category_name in session.query(Category.category_name).all()]
        except:
            return []


# DAO das Streams
class DAOStream:
    @staticmethod
    def select(session, id):
        stream = session.query(Streams).filter(Streams.stream_id == id).first()
        return stream
    

# DAO dos Canais
class DAOChannel:
    @staticmethod
    def select(session, channel_id):
        # Exemplo: Selecionar dados da tabela de canais
        return session.query(Canais).filter_by(channel_id = channel_id).first()
    
    @staticmethod
    def get_broadcaster_ids(session):
        try:
            # Modificar para selecionar os channel_id
            return [channel_id[0] for channel_id in session.query(Canais.channel_id).all()]
        except:
            return []


# DAO dos Usuarios
class DAOUser:
    @staticmethod
    def select(session: Session, user_id: str):
        return session.query(Usuario).filter_by(user_id = user_id).first()

    @staticmethod
    def get_user_ids(session: Session):
        # Retorna uma lista de user_ids
        return [result.user_id for result in session.query(Usuario.user_id).all()]
    

# DAO dos Videos
class DAOVideo:
    @staticmethod
    def select(session, video_id):
        try:
            return session.query(Videos).filter(Videos.video_id == video_id).first()
        except Exception as e:
            print(f"Erro durante a seleção: {str(e)}")
