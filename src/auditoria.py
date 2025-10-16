import logging
from datetime import datetime
from src.db.mongo_handler import get_mongo_database
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "auditoria.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def registrar_evento(usuario, operacao, entidade, referencia, nivel="INFO"):
    data_hora = datetime.now()
    
    print(f"[{nivel}] {data_hora.strftime('%Y-%m-%d %H:%M:%S')} | {usuario} | {operacao} | {entidade} | {referencia}")
    
    log_message = f"{usuario} | {operacao} | {entidade} | {referencia}"
    if nivel.upper() == "INFO":
        logging.info(log_message)
    else:
        logging.error(log_message)
    
    try:
        db = get_mongo_database() 
        if db is not None:
            auditoria_collection = db["auditoria"] 
            log_document = {
                "usuario": usuario, "operacao": operacao, "entidade": entidade,
                "referencia": referencia, "timestamp": data_hora, "nivel": nivel
            }
            auditoria_collection.insert_one(log_document)
        else:
            print("ERRO CRÍTICO: Não foi possível obter a conexão com o MongoDB para registrar o log.")
    except Exception as e:
        print(f"ERRO: Falha ao registrar auditoria no MongoDB: {e}")