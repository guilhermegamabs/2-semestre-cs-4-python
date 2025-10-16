from unittest.mock import patch, MagicMock
import pytest

from src.core.services import criar_cliente_service


@patch('src.core.services.dao_criar_cliente') 
@patch('src.core.services.registrar_evento')   
def test_criar_novo_cliente_sucesso(mock_registrar_evento, mock_dao_criar):
    """
    Testa o cenário de sucesso da criação de um cliente.
    """
    mock_dao_criar.return_value = True

    resultado = criar_cliente_service(
        cpf="12345678901", nome="João Teste", data_nasc=None, 
        endereco=None, telefone=None, email="joao@teste.com", usuario="admin"
    )

    assert resultado is True
    
    # Verifica se a função do DAO foi chamada uma vez com os dados corretos
    mock_dao_criar.assert_called_once_with(
        "12345678901", "João Teste", None, None, None, "joao@teste.com"
    )
    
    # Verifica se a função de log foi chamada
    mock_registrar_evento.assert_called_once()