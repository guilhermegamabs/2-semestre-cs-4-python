import csv
from datetime import datetime
from pathlib import Path
from db.mysql_handler import get_mysql_connection as conectar_mysql

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

def receita_mensal():
    conn = conectar_mysql()
    if not conn: return 0
    total = 0
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(valor_mensal) FROM seguros WHERE ativo = TRUE")
            resultado = cur.fetchone()
            total = resultado[0] if resultado and resultado[0] is not None else 0
    finally:
        if conn and conn.is_connected():
            conn.close()
    return total

def top_clientes(n=5):
    conn = conectar_mysql()
    if not conn: return []
    clientes = []
    try:
        with conn.cursor() as cur:
            query = """
                SELECT c.nome, SUM(s.valor_mensal) as total_premio
                FROM clientes c JOIN seguros s ON c.cpf = s.cpf
                WHERE s.ativo = TRUE GROUP BY c.nome
                ORDER BY total_premio DESC LIMIT %s
            """
            cur.execute(query, (n,))
            clientes = cur.fetchall()
    finally:
        if conn and conn.is_connected():
            conn.close()
    return clientes

def sinistros_por_status():
    conn = conectar_mysql()
    if not conn: return []
    status = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT status, COUNT(*) FROM sinistros GROUP BY status")
            status = cur.fetchall()
    finally:
        if conn and conn.is_connected():
            conn.close()
    return status

def exportar_csv(nome_arquivo, dados, cabecalho):
    arquivo = EXPORT_DIR / f"{nome_arquivo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    try:
        with open(arquivo, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cabecalho)
            writer.writerows(dados)
        print(f"Relatório exportado com sucesso para: {arquivo}")
    except Exception as e:
        print(f"Erro ao exportar CSV: {e}")