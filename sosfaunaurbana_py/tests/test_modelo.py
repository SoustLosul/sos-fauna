"""Testes das classes do modelo: pilares da POO, regras de negocio, operadores e decoradores."""
import io
import unittest
from contextlib import redirect_stdout
from datetime import date

from exceptions.erros import StatusInvalidoError, ValidacaoError
from model.agente_resgate import AgenteResgate
from model.cidadao import Cidadao
from model.decoradores import ContarChamadas, cronometrar, registrar
from model.equipe_resgate import EquipeResgate
from model.pedido import Pedido
from model.produto import Produto
from model.usuario import Usuario


def novo_cidadao(id_usuario: int = 1, nome: str = "Ana", email: str = "ana@x.com") -> Cidadao:
    return Cidadao(id_usuario, nome, email, "123", date.today(), "Rua A", "10", "Centro", "Recife", "50000")


def novo_agente(id_usuario: int = 2, matricula: str = "M1") -> AgenteResgate:
    return AgenteResgate(id_usuario, "Bia", "", "x", date.today(), matricula, "Biologa")


class TestEncapsulamento(unittest.TestCase):
    def test_nome_obrigatorio(self) -> None:
        with self.assertRaises(ValidacaoError):
            novo_cidadao(nome="   ")

    def test_cidadao_exige_email_mas_agente_nao(self) -> None:
        with self.assertRaises(ValidacaoError):
            novo_cidadao(email="")
        self.assertEqual(novo_agente().email, "")

    def test_matricula_obrigatoria(self) -> None:
        with self.assertRaises(ValidacaoError):
            novo_agente(matricula=" ")

    def test_id_e_somente_leitura(self) -> None:
        with self.assertRaises(AttributeError):
            novo_cidadao().id_usuario = 99  # type: ignore[misc]

    def test_senha_privada_e_verificacao(self) -> None:
        c = novo_cidadao()
        self.assertTrue(c.verificar_senha("123"))
        self.assertFalse(c.verificar_senha("errada"))
        self.assertNotIn("123", repr(c))  # o repr nao vaza a senha

    def test_preco_negativo_e_quantidade_zero(self) -> None:
        with self.assertRaises(ValidacaoError):
            Produto(1, "Luva", "", -1, "EPI")
        with self.assertRaises(ValidacaoError):
            Produto(1, "Luva", "", 10, "EPI") * 0

    def test_valida_tambem_e_value_error(self) -> None:
        with self.assertRaises(ValueError):  # compatibilidade com `except ValueError`
            novo_cidadao(nome="")

    def test_listas_internas_sao_somente_leitura(self) -> None:
        equipe = EquipeResgate(5, "Alfa", "Zona Sul")
        self.assertIsInstance(equipe.agentes, tuple)
        with self.assertRaises(AttributeError):
            equipe.agentes.append(novo_agente())  # type: ignore[attr-defined]


class TestHerancaEPolimorfismo(unittest.TestCase):
    def test_heranca(self) -> None:
        self.assertTrue(issubclass(Cidadao, Usuario))
        self.assertTrue(issubclass(AgenteResgate, Usuario))

    def test_polimorfismo_descrever(self) -> None:
        usuarios: list[Usuario] = [novo_cidadao(), novo_agente()]
        textos = [u.descrever() for u in usuarios]  # mesmo metodo, comportamento diferente
        self.assertTrue(textos[0].startswith("Cidadao("))
        self.assertTrue(textos[1].startswith("AgenteResgate("))
        self.assertEqual([str(u) for u in usuarios], textos)

    def test_ordenacao_por_nome(self) -> None:
        nomes = [u.nome for u in sorted([novo_cidadao(1, "Zeca"), novo_cidadao(2, "Ana")])]
        self.assertEqual(nomes, ["Ana", "Zeca"])


class TestOperadores(unittest.TestCase):
    def setUp(self) -> None:
        self.luva = Produto(10, "Luva", "grossa", 25.5, "EPI")
        self.rede = Produto(11, "Rede", "captura", 80.0, "Captura")

    def test_produto_vezes_quantidade(self) -> None:
        item = self.luva * 3
        self.assertEqual(item.quantidade, 3)
        self.assertEqual(item.subtotal, 76.5)
        self.assertEqual((2 * self.luva).quantidade, 2)

    def test_item_mais_item(self) -> None:
        total = self.luva * 2 + self.luva * 3
        self.assertEqual(total.quantidade, 5)
        with self.assertRaises(ValidacaoError):
            self.luva * 1 + self.rede * 1

    def test_pedido_iadd_e_len(self) -> None:
        pedido = Pedido(20, date.today(), "Pendente", True, novo_cidadao())
        pedido += self.luva * 2
        pedido += self.rede * 1
        self.assertEqual(len(pedido), 2)
        self.assertEqual(pedido.valor_total, 131.0)

    def test_comparacoes(self) -> None:
        self.assertTrue(self.luva < self.rede)
        self.assertEqual(sorted([self.rede, self.luva]), [self.luva, self.rede])
        self.assertEqual(self.luva, Produto(10, "Outro nome", "", 1, "x"))  # igualdade por id

    def test_equipe_iadd_nao_duplica(self) -> None:
        equipe = EquipeResgate(5, "Alfa", "Zona Sul")
        agente = novo_agente()
        with redirect_stdout(io.StringIO()):  # @registrar imprime o log
            equipe += agente
            equipe += agente
        self.assertEqual(len(equipe), 1)
        self.assertIs(agente.equipe, equipe)


class TestRegrasDePedido(unittest.TestCase):
    def test_exige_aceite_do_termo(self) -> None:
        with self.assertRaises(ValidacaoError):
            Pedido(1, date.today(), "Pendente", False, novo_cidadao())

    def test_status_invalido(self) -> None:
        pedido = Pedido(1, date.today(), "Pendente", True, novo_cidadao())
        with self.assertRaises(StatusInvalidoError):
            pedido.status_pedido = "Voando"

    def test_so_pedido_pendente_aceita_itens(self) -> None:
        pedido = Pedido(1, date.today(), "Pendente", True, novo_cidadao())
        pedido.status_pedido = "Confirmado"
        with self.assertRaises(StatusInvalidoError):
            pedido += Produto(10, "Luva", "", 5, "EPI") * 1


class TestDecoradores(unittest.TestCase):
    def test_contar_chamadas(self) -> None:
        @ContarChamadas
        def somar(a: int, b: int) -> int:
            return a + b
        somar(1, 2)
        somar(3, 4)
        self.assertEqual(somar.chamadas, 2)
        self.assertEqual(somar.__name__, "somar")  # update_wrapper preservou o nome

    def test_cronometrar_mantem_resultado_e_nome(self) -> None:
        @cronometrar
        def dobro(x: int) -> int:
            return x * 2
        saida = io.StringIO()
        with redirect_stdout(saida):
            self.assertEqual(dobro(4), 8)
        self.assertIn("dobro levou", saida.getvalue())
        self.assertEqual(dobro.__name__, "dobro")

    def test_registrar(self) -> None:
        @registrar
        def ola() -> str:
            return "oi"
        saida = io.StringIO()
        with redirect_stdout(saida):
            self.assertEqual(ola(), "oi")
        self.assertIn("[LOG]", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
