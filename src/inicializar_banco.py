from db.mysql_handler import get_mysql_connection, garantir_database
from usuarios import criar_usuario
from dao import criar_cliente, criar_seguro

def criar_tabelas_mysql():
    conn = get_mysql_connection()
    if not conn:
        print("Não foi possível conectar ao MySQL para criar as tabelas.")
        return
    print("Conectado ao MySQL. Verificando/criando tabelas...")
    with conn.cursor(buffered=True) as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            cpf VARCHAR(11) PRIMARY KEY, nome VARCHAR(255) NOT NULL, data_nascimento DATE,
            endereco TEXT, telefone VARCHAR(20), email VARCHAR(255)
        ) ENGINE=InnoDB;
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS seguros (
            numero_apolice VARCHAR(50) PRIMARY KEY, tipo VARCHAR(50) NOT NULL, cpf VARCHAR(11) NOT NULL,
            valor_mensal DECIMAL(10, 2) NOT NULL, ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(cpf) REFERENCES clientes(cpf) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sinistros (
            id INT PRIMARY KEY AUTO_INCREMENT, numero_apolice VARCHAR(50) NOT NULL, descricao TEXT,
            data_ocorrencia DATE, status VARCHAR(50) DEFAULT 'ABERTO',
            FOREIGN KEY(numero_apolice) REFERENCES seguros(numero_apolice) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username VARCHAR(100) PRIMARY KEY, senha VARCHAR(255) NOT NULL,
            perfil ENUM('admin','comum') NOT NULL
        ) ENGINE=InnoDB;
        """)
        conn.commit()
    conn.close()
    print("Tabelas do MySQL verificadas/criadas com sucesso!")

def popular_dados_iniciais():
    print("\nPopulando banco de dados com dados iniciais...")
    try:
        criar_usuario("admin", "123456", "admin", usuario_ativo="sistema")
    except Exception as e:
        print(f"Erro ao criar usuário admin: {e}")
    try:
        criar_cliente("12345678901", "João Silva", "1980-05-12", "Rua A, 100", "1112345678", "joao@email.com")
        criar_cliente("98765432100", "Maria Oliveira", "1990-08-25", "Rua B, 200", "11987654321", "maria@email.com")
        print("Clientes iniciais cadastrados.")
    except Exception as e:
        print(f"Erro ao criar clientes: {e}")
    try:
        criar_seguro("AP1001", "Automovel", "12345678901", 200.0)
        criar_seguro("AP1002", "Vida", "98765432100", 50.0)
        print("Seguros iniciais cadastrados.")
    except Exception as e:
        print(f"Erro ao criar seguros: {e}")

if __name__ == "__main__":
    garantir_database()
    criar_tabelas_mysql()
    popular_dados_iniciais()
    print("\nSetup inicial concluído!")