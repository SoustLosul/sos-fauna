"""Validacoes usadas pelos setters (encapsulamento) das classes do modelo."""
from exceptions.erros import ValidacaoError


def exigir_texto(valor: str, campo: str) -> str:
    """Devolve o texto sem espacos nas pontas ou levanta ValidacaoError se ficar vazio."""
    texto = str(valor).strip()
    if not texto:
        raise ValidacaoError(f"{campo} e obrigatorio.")
    return texto


def exigir_preco(valor: float) -> float:
    """Converte para float e recusa valores negativos."""
    numero = float(valor)
    if numero < 0:
        raise ValidacaoError("O preco nao pode ser negativo.")
    return numero


def exigir_quantidade(valor: int) -> int:
    """Converte para int e recusa zero ou negativos."""
    numero = int(valor)
    if numero <= 0:
        raise ValidacaoError("A quantidade deve ser maior que zero.")
    return numero
