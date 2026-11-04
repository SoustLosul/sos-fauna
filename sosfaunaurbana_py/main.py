"""Ponto de entrada do SOS Fauna Urbana.

Carrega os dados salvos na pasta "dados" e abre a interface grafica.
Para executar:  python main.py
"""
import sys

from exceptions.erros import PersistenciaError
from main_gui import App
from repository.repositorio import carregar_dados, gerar_id


def main() -> None:
    """Inicia a aplicacao: carrega os dados, abre a janela e, ao fechar, mostra um resumo."""
    try:
        carregar_dados()
    except PersistenciaError as erro:
        print(f"Erro ao carregar os dados: {erro}")
        sys.exit(1)

    app = App()
    app.mainloop()
    print(f"IDs gerados nesta sessao: {gerar_id.chamadas}")


if __name__ == "__main__":
    main()
