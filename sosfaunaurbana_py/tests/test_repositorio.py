"""Testes da persistencia: salvar, 'fechar o programa' e recuperar os dados."""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date

from exceptions.erros import PersistenciaError, RegistroDuplicadoError
from model.agente_resgate import AgenteResgate
from model.cidadao import Cidadao
from model.pedido import Pedido
from model.produto import Produto
from repository import repositorio as repo


class TestRepositorio(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._pasta_original = repo.PASTA_DADOS
        repo.PASTA_DADOS = self._tmp.name
        self._limpar_memoria()

    def tearDown(self) -> None:
        repo.PASTA_DADOS = self._pasta_original
        self._limpar_memoria()
        self._tmp.cleanup()

    @staticmethod
    def _limpar_memoria() -> None:
        for lista in (repo.cidadaos, repo.agentes, repo.equipes, repo.especies,
                      repo.solicitacoes, repo.produtos, repo.pedidos):
            lista.clear()
        repo.proximo_id = 1

    def _cidadao(self) -> Cidadao:
        c = Cidadao(repo.gerar_id(), "Ana", "ana@x.com", "123", date.today(),
                    "Rua A", "10", "Centro", "Recife", "50000")
        repo.cidadaos.append(c)
        repo.salvar_cidadao(c)
        return c

    def test_salvar_e_recuperar_apos_reiniciar(self) -> None:
        c = self._cidadao()
        p = Produto(repo.gerar_id(), "Luva", "grossa", 25.5, "EPI")
        repo.produtos.append(p)
        repo.salvar_produto(p)
        pedido = Pedido(repo.gerar_id(), date.today(), "Pendente", True, c)
        pedido += p * 2
        pedido.status_pedido = "Entregue"  # status diferente de Pendente tem que sobreviver
        repo.pedidos.append(pedido)
        repo.salvar_pedido(pedido)

        self._limpar_memoria()  # simula fechar e abrir o programa de novo
        with redirect_stdout(io.StringIO()):
            repo.carregar_dados()

        self.assertEqual([x.nome for x in repo.cidadaos], ["Ana"])
        self.assertEqual(repo.pedidos[0].status_pedido, "Entregue")
        self.assertEqual(repo.pedidos[0].valor_total, 51.0)
        self.assertEqual(repo.proximo_id, pedido.id_pedido + 1)  # IDs continuam de onde pararam

    def test_regravar_apos_edicao(self) -> None:
        c = self._cidadao()
        c.nome = "Ana Maria"
        repo.regravar_cidadaos()
        self._limpar_memoria()
        repo.carregar_cidadaos()
        self.assertEqual(repo.cidadaos[0].nome, "Ana Maria")

    def test_linha_corrompida_e_ignorada_com_aviso(self) -> None:
        self._cidadao()
        with open(repo.caminho_arquivo("cidadaos.txt"), "a", encoding="utf-8") as arq:
            arq.write("linha|quebrada\n")
            arq.write("9|  |x@x|s|2024-01-01|R|1|B|C|0\n")  # nome vazio: o modelo recusa
        self._limpar_memoria()
        saida = io.StringIO()
        with redirect_stdout(saida):
            repo.carregar_cidadaos()
        self.assertEqual(len(repo.cidadaos), 1)
        self.assertEqual(saida.getvalue().count("[AVISO]"), 2)

    def test_arquivo_inexistente_devolve_lista_vazia(self) -> None:
        self.assertEqual(repo.ler_linhas("nao_existe.txt"), [])

    def test_erro_de_gravacao_vira_persistencia_error(self) -> None:
        arquivo_no_lugar_da_pasta = os.path.join(self._tmp.name, "ocupado")
        open(arquivo_no_lugar_da_pasta, "w").close()
        repo.PASTA_DADOS = arquivo_no_lugar_da_pasta  # "pasta" que na verdade e um arquivo
        with self.assertRaises(PersistenciaError):
            repo.salvar_linha("x.txt", [1, 2])

    def test_unicidade_de_email_e_matricula(self) -> None:
        c = self._cidadao()
        with self.assertRaises(RegistroDuplicadoError):
            repo.garantir_email_cidadao_unico("ANA@x.com")  # ignora maiuscula/minuscula
        repo.garantir_email_cidadao_unico("ana@x.com", ignorar=c)  # editar o proprio cadastro e ok

        agente = AgenteResgate(repo.gerar_id(), "Bia", "", "x", date.today(), "M1", "Biologa")
        repo.agentes.append(agente)
        with self.assertRaises(RegistroDuplicadoError):
            repo.garantir_matricula_unica("m1")
        repo.garantir_matricula_unica("M2")


if __name__ == "__main__":
    unittest.main()
