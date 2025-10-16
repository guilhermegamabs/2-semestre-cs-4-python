from core.services import (
    criar_cliente_service, listar_clientes_service, buscar_cliente_service, 
    atualizar_cliente_service, remover_cliente_service,
    criar_seguro_service, listar_seguros_service, buscar_seguro_service, 
    atualizar_seguro_service, cancelar_seguro_service,
    registrar_sinistro_service, listar_sinistros_service, buscar_sinistro_service, 
    atualizar_sinistro_service
)
from relatorios import receita_mensal, top_clientes, sinistros_por_status
from usuarios import (
    autenticar, listar_usuarios, criar_usuario, 
    alterar_senha, deletar_usuario
)
from validacoes import OperacaoNaoPermitida

def menu_principal():
    print("=== SISTEMA DE SEGUROS ===")
    usuario = None
    while not usuario:
        login = input("Login: ")
        senha = input("Senha: ")
        usuario = autenticar(login, senha)
        if not usuario:
            print("Usuário ou senha inválidos! Tente novamente.\n")
    username = usuario['username']
    perfil = usuario['perfil']
    print(f"\nBem-vindo, {username}! Perfil: {perfil}")
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Clientes\n2. Seguros / Apólices\n3. Sinistros\n4. Relatórios")
        if perfil == "admin":
            print("5. Gerenciamento de Usuários")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1": menu_clientes(username)
        elif opcao == "2": menu_seguros(username)
        elif opcao == "3": menu_sinistros(username)
        elif opcao == "4": menu_relatorios()
        elif opcao == "5" and perfil == "admin": menu_usuarios(username)
        elif opcao == "0": print("Saindo..."); break
        else: print("Opção inválida.")

def menu_clientes(username):
    while True:
        print("\n--- MENU CLIENTES ---\n1. Cadastrar\n2. Listar\n3. Buscar\n4. Atualizar\n5. Remover\n0. Voltar")
        sub = input("Escolha: ")
        if sub == "1":
            cpf = input("CPF: "); nome = input("Nome: "); data_nasc = input("Nascimento (AAAA-MM-DD): ")
            endereco = input("Endereço: "); telefone = input("Telefone: "); email = input("Email: ")
            criar_cliente_service(cpf, nome, data_nasc, endereco, telefone, email, usuario=username)
        elif sub == "2":
            clientes = listar_clientes_service()
            if not clientes: print("Nenhum cliente cadastrado.")
            for c in clientes: print(c)
        elif sub == "3":
            cpf = input("CPF do cliente: "); cliente = buscar_cliente_service(cpf)
            print(cliente if cliente else "Cliente não encontrado.")
        elif sub == "4":
            cpf = input("CPF do cliente: "); nome = input("Novo nome (Enter p/ manter): ")
            data_nasc = input("Nova data (Enter p/ manter): "); endereco = input("Novo endereço (Enter p/ manter): ")
            telefone = input("Novo telefone (Enter p/ manter): "); email = input("Novo email (Enter p/ manter): ")
            atualizar_cliente_service(cpf, nome or None, data_nasc or None, endereco or None, telefone or None, email or None, usuario=username)
        elif sub == "5":
            cpf = input("CPF do cliente a remover: ")
            if input(f"Confirma remoção do cliente {cpf}? (s/n): ").lower() == "s":
                remover_cliente_service(cpf, usuario=username)
        elif sub == "0": break
        else: print("Opção inválida.")

def menu_seguros(username):
    while True:
        print("\n--- MENU SEGUROS ---\n1. Criar\n2. Listar\n3. Buscar\n4. Atualizar\n5. Cancelar\n0. Voltar")
        sub = input("Escolha: ")
        if sub == "1":
            tipo = input("Tipo (Automovel/Vida/Residencial): ")
            cpf = input("CPF do cliente: ")
            try:
                valor = float(input("Valor mensal: "))
                criar_seguro_service(tipo, cpf, valor, usuario=username)
            except ValueError: print("Erro: Valor inválido.")
        elif sub == "2":
            seguros = listar_seguros_service()
            if not seguros: print("Nenhum seguro.")
            for s in seguros: print(s)
        elif sub == "3":
            numero = input("Nº da apólice: "); seguro = buscar_seguro_service(numero)
            print(seguro if seguro else "Seguro não encontrado.")
        elif sub == "4":
            numero = input("Nº da apólice: "); valor_input = input("Novo valor (Enter p/ manter): ")
            valor = float(valor_input) if valor_input else None
            atualizar_seguro_service(numero, valor_mensal=valor, usuario=username)
        elif sub == "5":
            numero = input("Nº da apólice a cancelar: ")
            if input(f"Confirma cancelamento da apólice {numero}? (s/n): ").lower() == "s":
                cancelar_seguro_service(numero, usuario=username)
        elif sub == "0": break
        else: print("Opção inválida.")

def menu_sinistros(username):
    while True:
        print("\n--- MENU SINISTROS ---\n1. Registrar\n2. Listar\n3. Buscar\n4. Atualizar status\n0. Voltar")
        sub = input("Escolha: ")
        if sub == "1":
            apolice = input("Nº da apólice: "); desc = input("Descrição: "); data = input("Data (AAAA-MM-DD): ")
            registrar_sinistro_service(apolice, desc, data, usuario=username)
        elif sub == "2":
            sinistros = listar_sinistros_service()
            if not sinistros: print("Nenhum sinistro.")
            for s in sinistros: print(s)
        elif sub == "3":
            try:
                sid = int(input("ID do sinistro: ")); sinistro = buscar_sinistro_service(sid)
                print(sinistro if sinistro else "Sinistro não encontrado.")
            except ValueError: print("ID inválido.")
        elif sub == "4":
            try:
                sid = int(input("ID do sinistro: ")); status = input("Novo status: ").upper()
                atualizar_sinistro_service(sid, status=status, usuario=username)
            except ValueError: print("ID inválido.")
        elif sub == "0": break
        else: print("Opção inválida.")

def menu_relatorios():
    while True:
        print("\n--- MENU RELATÓRIOS ---\n1. Receita mensal\n2. Top clientes\n3. Sinistros por status\n0. Voltar")
        sub = input("Escolha: ")
        if sub == "1": print(f"Receita mensal prevista: R$ {receita_mensal():,.2f}")
        elif sub == "2":
            print("Top clientes:"); [print(f" - {nome}: R$ {valor:,.2f}") for nome, valor in top_clientes()]
        elif sub == "3":
            print("Sinistros por status:"); [print(f" - {st}: {count}") for st, count in sinistros_por_status()]
        elif sub == "0": break
        else: print("Opção inválida.")

def menu_usuarios(username):
    while True:
        print("\n--- MENU USUÁRIOS ---\n1. Criar\n2. Listar\n3. Alterar senha\n4. Deletar\n0. Voltar")
        sub = input("Escolha: ")
        if sub == "1":
            login = input("Login: "); senha = input("Senha: "); perfil = input("Perfil (admin/comum): ")
            criar_usuario(login, senha, perfil, usuario_ativo=username)
        elif sub == "2": [print(f" - Login: {u['username']}, Perfil: {u['perfil']}") for u in listar_usuarios()]
        elif sub == "3":
            login = input("Login do usuário: "); senha = input("Nova senha: ")
            alterar_senha(login, senha, usuario_ativo=username)
        elif sub == "4":
            login = input("Login a deletar: ")
            if login == username: print("Erro: Não pode deletar o próprio usuário."); continue
            if input(f"Confirma exclusão de {login}? (s/n): ").lower() == "s":
                deletar_usuario(login, usuario_ativo=username)
        elif sub == "0": break
        else: print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()