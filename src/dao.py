import re
from db.mysql_handler import get_mysql_connection as conectar_mysql
from validacoes import validar_cpf

# FUNÇÕES DE CLIENTES

def criar_cliente(cpf, nome, data_nasc=None, endereco=None, telefone=None, email=None):
    """Insere um novo cliente no MySQL, limpando o CPF antes de salvar."""
    cpf = re.sub(r"\D", "", cpf)
    validar_cpf(cpf)
    conn = conectar_mysql()
    if not conn: return False

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT cpf FROM clientes WHERE cpf=%s", (cpf,))
            if cur.fetchone():
                print(f"ERRO: Cliente com CPF {cpf} já existe.")
                return False
            
            query = """
                INSERT INTO clientes (cpf, nome, data_nascimento, endereco, telefone, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (cpf, nome, data_nasc, endereco, telefone, email))
            conn.commit()
            return True
    finally:
        if conn and conn.is_connected():
            conn.close()

def listar_clientes():
    conn = conectar_mysql()
    if not conn: return []
    try:
        with conn.cursor(dictionary=True) as cur: 
            cur.execute("SELECT * FROM clientes")
            return cur.fetchall()
    finally:
        if conn and conn.is_connected():
            conn.close()

def buscar_cliente(cpf):
    cpf = re.sub(r"\D", "", cpf)
    conn = conectar_mysql()
    if not conn: return None
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM clientes WHERE cpf=%s", (cpf,))
            return cur.fetchone()
    finally:
        if conn and conn.is_connected():
            conn.close()

def atualizar_cliente(cpf, nome, data_nasc, endereco, telefone, email):
    cpf = re.sub(r"\D", "", cpf)
    conn = conectar_mysql()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            campos, valores = [], []
            if nome: campos.append("nome=%s"); valores.append(nome)
            if data_nasc: campos.append("data_nascimento=%s"); valores.append(data_nasc)
            if endereco: campos.append("endereco=%s"); valores.append(endereco)
            if telefone: campos.append("telefone=%s"); valores.append(telefone)
            if email: campos.append("email=%s"); valores.append(email)
            if not campos: return False
            query = f"UPDATE clientes SET {', '.join(campos)} WHERE cpf=%s"
            valores.append(cpf)
            cur.execute(query, tuple(valores))
            conn.commit()
            return cur.rowcount > 0
    finally:
        if conn and conn.is_connected():
            conn.close()

def remover_cliente(cpf):
    cpf = re.sub(r"\D", "", cpf)
    conn = conectar_mysql()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM clientes WHERE cpf=%s", (cpf,))
            conn.commit()
            return cur.rowcount > 0
    finally:
        if conn and conn.is_connected():
            conn.close()

# FUNÇÕES DE SEGUROS (APÓLICES)

def criar_seguro(numero_apolice, tipo, cpf_cliente, valor_mensal):
    conn = conectar_mysql()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            # 1. VERIFICAR SE O CLIENTE EXISTE
            cur.execute("SELECT cpf FROM clientes WHERE cpf=%s", (cpf_cliente,))
            if not cur.fetchone():
                print(f"ERRO: Cliente com CPF {cpf_cliente} não encontrado. Não é possível criar o seguro.")
                return False

            # 2. VERIFICAR SE A APÓLICE JÁ EXISTE 
            cur.execute("SELECT numero_apolice FROM seguros WHERE numero_apolice=%s", (numero_apolice,))
            if cur.fetchone():
                print(f"ERRO: Apólice {numero_apolice} já existe.")
                return False
            
            # 3. INSERIR O SEGURO
            query = "INSERT INTO seguros (numero_apolice, tipo, cpf, valor_mensal) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (numero_apolice, tipo, cpf_cliente, valor_mensal))
            conn.commit()
            return True
    finally:
        if conn and conn.is_connected():
            conn.close()

def listar_seguros():
    conn = conectar_mysql()
    if not conn: return []
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM seguros")
            return cur.fetchall()
    finally:
        if conn and conn.is_connected():
            conn.close()

def buscar_seguro(numero_apolice):
    conn = conectar_mysql()
    if not conn: return None
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM seguros WHERE numero_apolice=%s", (numero_apolice,))
            return cur.fetchone()
    finally:
        if conn and conn.is_connected():
            conn.close()

def atualizar_seguro(numero_apolice, valor_mensal=None, ativo=None):
    conn = conectar_mysql()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            campos, valores = [], []
            if valor_mensal is not None: campos.append("valor_mensal=%s"); valores.append(valor_mensal)
            if ativo is not None: campos.append("ativo=%s"); valores.append(ativo)
            if not campos: return False
            query = f"UPDATE seguros SET {', '.join(campos)} WHERE numero_apolice=%s"
            valores.append(numero_apolice)
            cur.execute(query, tuple(valores))
            conn.commit()
            return cur.rowcount > 0
    finally:
        if conn and conn.is_connected():
            conn.close()

def cancelar_seguro(numero_apolice):
    return atualizar_seguro(numero_apolice, ativo=False)

# FUNÇÕES DE SINISTROS

def registrar_sinistro(numero_apolice, descricao, data_ocorrencia):
    conn = conectar_mysql()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO sinistros (numero_apolice, descricao, data_ocorrencia) VALUES (%s, %s, %s)"
            cur.execute(query, (numero_apolice, descricao, data_ocorrencia))
            conn.commit()
            return True
    finally:
        if conn and conn.is_connected():
            conn.close()

def listar_sinistros():
    conn = conectar_mysql()
    if not conn: return []
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM sinistros")
            return cur.fetchall()
    finally:
        if conn and conn.is_connected():
            conn.close()

def buscar_sinistro(sinistro_id):
    conn = conectar_mysql()
    if not conn: return None
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM sinistros WHERE id=%s", (sinistro_id,))
            return cur.fetchone()
    finally:
        if conn and conn.is_connected():
            conn.close()

def atualizar_sinistro(sinistro_id, status=None, descricao=None):
    conn = conectar_mysql()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            campos, valores = [], []
            if status: campos.append("status=%s"); valores.append(status)
            if descricao: campos.append("descricao=%s"); valores.append(descricao)
            if not campos: return False
            query = f"UPDATE sinistros SET {', '.join(campos)} WHERE id=%s"
            valores.append(sinistro_id)
            cur.execute(query, tuple(valores))
            conn.commit()
            return cur.rowcount > 0
    finally:
        if conn and conn.is_connected():
            conn.close()