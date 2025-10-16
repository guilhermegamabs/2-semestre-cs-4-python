# src/db/mysql_handler.py (VERSÃO CORRIGIDA)

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Lê as variáveis de configuração
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_PORT = os.getenv("MYSQL_PORT")

def garantir_database():
    """Conecta ao servidor MySQL e cria o banco de dados se ele não existir."""
    try:
        # Conecta ao servidor SEM especificar o banco de dados
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        cursor = conn.cursor()
        # Executa o comando para criar o banco de dados
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"Banco de dados '{MYSQL_DB}' garantido.")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Erro ao garantir a existência do banco de dados: {e}")
        # Encerra o script se não conseguir criar o banco, pois nada mais vai funcionar.
        exit()

def get_mysql_connection():
    """Estabelece e retorna uma conexão com o banco de dados MySQL JÁ EXISTENTE."""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB, # Agora a conexão pode usar o DB, pois garantimos que ele existe
            port=MYSQL_PORT
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None