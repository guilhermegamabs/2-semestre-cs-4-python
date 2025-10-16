import re
from datetime import datetime

class CpfInvalido(Exception): pass
class OperacaoNaoPermitida(Exception): pass

def validar_cpf(cpf: str) -> bool:
    cpf_limpo = re.sub(r"\D", "", cpf)
    if len(cpf_limpo) != 11 or len(set(cpf_limpo)) == 1:
        raise CpfInvalido(f"CPF '{cpf}' é inválido.")
    return True