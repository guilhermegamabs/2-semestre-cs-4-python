import hashlib
from src.db.mysql_handler import get_mysql_connection as conectar_mysql
from auditoria import registrar_evento

def criar_usuario(username, senha, perfil, usuario_ativo="sistema"):
    conn = conectar_mysql()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
            if cur.fetchone():
                print(f"Usuário '{username}' já existe.")
                registrar_evento(usuario_ativo, "CRIAR_FALHA", "USUARIO", username, nivel="ERROR")
                return
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            cur.execute("INSERT INTO usuarios (username, senha, perfil) VALUES (%s, %s, %s)",
                        (username, senha_hash, perfil))
            conn.commit()
        registrar_evento(usuario_ativo, "CRIAR", "USUARIO", username)
        print(f"Usuário '{username}' criado com sucesso.")
    finally:
        if conn and conn.is_connected():
            conn.close()

def autenticar(username, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    conn = conectar_mysql()
    if not conn: return None
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT username, perfil FROM usuarios WHERE username=%s AND senha=%s", (username, senha_hash))
            usuario = cur.fetchone()
        if usuario:
            registrar_evento(username, "LOGIN", "USUARIO", username)
            return usuario
        registrar_evento(username, "LOGIN_FALHA", "USUARIO", username, nivel="ERROR")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

def listar_usuarios():
    conn = conectar_mysql()
    if not conn: return []
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT username, perfil FROM usuarios")
            return cur.fetchall()
    finally:
        if conn and conn.is_connected():
            conn.close()

def alterar_senha(username, nova_senha, usuario_ativo):
    senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
    conn = conectar_mysql()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE usuarios SET senha=%s WHERE username=%s", (senha_hash, username))
            conn.commit()
            if cur.rowcount > 0:
                 registrar_evento(usuario_ativo, "ALTERAR_SENHA", "USUARIO", username)
                 print(f"Senha do usuário '{username}' alterada com sucesso.")
            else:
                print(f"Usuário '{username}' não encontrado.")
    finally:
        if conn and conn.is_connected():
            conn.close()

def deletar_usuario(username, usuario_ativo):
    conn = conectar_mysql()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE username=%s", (username,))
            conn.commit()
            if cur.rowcount > 0:
                registrar_evento(usuario_ativo, "DELETAR_USUARIO", "USUARIO", username)
                print(f"Usuário '{username}' deletado com sucesso.")
            else:
                print(f"Usuário '{username}' não encontrado.")
    finally:
        if conn and conn.is_connected():
            conn.close()