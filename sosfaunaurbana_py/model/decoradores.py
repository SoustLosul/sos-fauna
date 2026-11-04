"""Decoradores reutilizaveis do projeto SOS Fauna Urbana."""
import time
from functools import update_wrapper, wraps
from typing import Any, Callable

from exceptions.erros import StatusInvalidoError


def registrar(funcao: Callable[..., Any]) -> Callable[..., Any]:
    """Mostra no console cada chamada da funcao decorada."""
    @wraps(funcao)
    def embrulho(*args: Any, **kwargs: Any) -> Any:
        print(f"[LOG] Chamando {funcao.__qualname__} com {args}")
        return funcao(*args, **kwargs)
    return embrulho


def cronometrar(funcao: Callable[..., Any]) -> Callable[..., Any]:
    """Mostra quanto tempo a funcao decorada levou para rodar."""
    @wraps(funcao)
    def embrulho(*args: Any, **kwargs: Any) -> Any:
        inicio = time.perf_counter()
        resultado = funcao(*args, **kwargs)
        fim = time.perf_counter()
        print(f"[TEMPO] {funcao.__name__} levou {fim - inicio:.4f}s")
        return resultado
    return embrulho


def requer_status_pedido(*permitidos: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorador COM argumentos: so deixa o metodo rodar se o pedido estiver
    num dos status permitidos. Precisa da camada extra (fabrica -> decorador -> embrulho)."""
    def decorador(funcao: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(funcao)
        def embrulho(self: Any, *args: Any, **kwargs: Any) -> Any:
            if self.status_pedido not in permitidos:
                raise StatusInvalidoError(
                    f"'{funcao.__name__}' so e permitido com status "
                    f"{' ou '.join(permitidos)} (status atual: {self.status_pedido})."
                )
            return funcao(self, *args, **kwargs)
        return embrulho
    return decorador


class ContarChamadas:
    """Decorador feito com CLASSE: guarda estado (quantas vezes a funcao foi chamada)."""

    def __init__(self, funcao: Callable[..., Any]) -> None:
        update_wrapper(self, funcao)  # copia __name__, __doc__ etc. (equivale ao @wraps)
        self.funcao = funcao
        self.chamadas: int = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.chamadas += 1
        return self.funcao(*args, **kwargs)
