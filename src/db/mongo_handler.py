import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_LOGS = os.getenv("MONGO_DB_LOGS")

def get_mongo_client():
    """
    Estabelece e retorna uma conexão com o cliente MongoDB.
    """
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ismaster')
        return client
    except ConnectionFailure as e:
        print(f"Erro de conexão com o MongoDB: {e}")
        return None

def get_mongo_database():
    """
    Retorna uma referência ao banco de dados de logs no MongoDB.
    """
    client = get_mongo_client()
    if client:
        return client[MONGO_DB_LOGS]
    return None

# --- Função de Teste ---
if __name__ == '__main__':
    db = get_mongo_database()
    if db:
        print(f"Conexão com o MongoDB no banco '{MONGO_DB_LOGS}' bem-sucedida!")
        print("Coleções existentes:", db.list_collection_names())
    else:
        print("Falha ao conectar com o MongoDB.")