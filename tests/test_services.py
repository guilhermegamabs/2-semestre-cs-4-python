import pytest
from unittest.mock import patch
from src.core.services import criar_cliente_service

@patch('src.core.services.dao_criar_cliente')
@patch('src.core.services.registrar_evento')
def test_criar_cliente_service_sucesso(mock_registrar_evento, mock_dao_criar):
    """Testa o cenário de sucesso da criação de um cliente."""
    mock_dao_criar.return_value = True

    resultado = criar_cliente_service("12345678901", "Teste", None, None, None, None, "admin")

    assert resultado is True
    mock_dao_criar.assert_called_once()
    mock_registrar_evento.assert_called_once()

@patch('src.core.services.dao_criar_cliente')
@patch('src.core.services.registrar_evento')
def test_criar_cliente_service_falha_dao(mock_registrar_evento, mock_dao_criar):
    """Testa o cenário onde o DAO falha ao criar o cliente."""
    mock_dao_criar.return_value = False

    resultado = criar_cliente_service("12345678901", "Teste", None, None, None, None, "admin")

    assert resultado is False
    mock_dao_criar.assert_called_once()
    mock_registrar_evento.assert_not_called()