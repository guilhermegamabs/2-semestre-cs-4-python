from datetime import datetime
from src.dao import (
    criar_cliente as dao_criar_cliente, listar_clientes as dao_listar_clientes,
    buscar_cliente as dao_buscar_cliente, atualizar_cliente as dao_atualizar_cliente,
    remover_cliente as dao_remover_cliente, criar_seguro as dao_criar_seguro,
    listar_seguros as dao_listar_seguros, buscar_seguro as dao_buscar_seguro,
    atualizar_seguro as dao_atualizar_seguro, cancelar_seguro as dao_cancelar_seguro,
    registrar_sinistro as dao_registrar_sinistro, listar_sinistros as dao_listar_sinistros,
    buscar_sinistro as dao_buscar_sinistro, atualizar_sinistro as dao_atualizar_sinistro
)
from src.auditoria import registrar_evento

def criar_cliente_service(cpf, nome, data_nasc, endereco, telefone, email, usuario):
    sucesso = dao_criar_cliente(cpf, nome, data_nasc, endereco, telefone, email)
    if sucesso:
        registrar_evento(usuario, "CRIAR", "CLIENTE", f"CPF: {cpf}")
        print("Cliente cadastrado com sucesso!")
        return True
    return False

def listar_clientes_service():
    return dao_listar_clientes()

def buscar_cliente_service(cpf):
    return dao_buscar_cliente(cpf)

def atualizar_cliente_service(cpf, nome, data_nasc, endereco, telefone, email, usuario):
    sucesso = dao_atualizar_cliente(cpf, nome, data_nasc, endereco, telefone, email)
    if sucesso:
        registrar_evento(usuario, "ATUALIZAR", "CLIENTE", f"CPF: {cpf}")
        print("Cliente atualizado com sucesso!")
        return True
    else:
        print("Nenhum dado alterado ou cliente não encontrado.")
        return False

def remover_cliente_service(cpf, usuario):
    sucesso = dao_remover_cliente(cpf)
    if sucesso:
        registrar_evento(usuario, "REMOVER", "CLIENTE", f"CPF: {cpf}")
        print("Cliente removido com sucesso!")
        return True
    else:
        print("Cliente não encontrado.")
        return False

def criar_seguro_service(tipo, cpf, valor, usuario):
    numero_apolice = f"AP{int(datetime.now().timestamp())}"
    sucesso = dao_criar_seguro(numero_apolice, tipo, cpf, valor)
    if sucesso:
        print(f"Apólice gerada com o número: {numero_apolice}")
        registrar_evento(usuario, "CRIAR", "SEGURO", f"Apólice: {numero_apolice}")
        print("Seguro criado com sucesso!")
        return True
    return False

def listar_seguros_service():
    return dao_listar_seguros()

def buscar_seguro_service(numero_apolice):
    return dao_buscar_seguro(numero_apolice)

def atualizar_seguro_service(numero, valor_mensal, usuario):
    sucesso = dao_atualizar_seguro(numero, valor_mensal=valor_mensal)
    if sucesso:
        registrar_evento(usuario, "ATUALIZAR", "SEGURO", f"Apólice: {numero}")
        print("Seguro atualizado com sucesso!")
        return True
    else:
        print("Nenhum dado alterado ou seguro não encontrado.")
        return False

def cancelar_seguro_service(numero, usuario):
    sucesso = dao_cancelar_seguro(numero)
    if sucesso:
        registrar_evento(usuario, "CANCELAR", "SEGURO", f"Apólice: {numero}")
        print("Seguro cancelado com sucesso!")
        return True
    else:
        print("Seguro não encontrado ou já cancelado.")
        return False

def registrar_sinistro_service(numero_apolice, descricao, data, usuario):
    sucesso = dao_registrar_sinistro(numero_apolice, descricao, data)
    if sucesso:
        registrar_evento(usuario, "REGISTRAR", "SINISTRO", f"Apólice: {numero_apolice}")
        print("Sinistro registrado com sucesso!")
        return True
    else:
        print("Falha ao registrar sinistro. Verifique se a apólice existe.")
        return False

def listar_sinistros_service():
    return dao_listar_sinistros()

def buscar_sinistro_service(sinistro_id):
    return dao_buscar_sinistro(sinistro_id)

def atualizar_sinistro_service(sinistro_id, status, usuario):
    sucesso = dao_atualizar_sinistro(sinistro_id, status=status)
    if sucesso:
        registrar_evento(usuario, "ATUALIZAR_STATUS", "SINISTRO", f"ID: {sinistro_id}")
        print("Status do sinistro atualizado com sucesso!")
        return True
    else:
        print("Nenhum dado alterado ou sinistro não encontrado.")
        return False