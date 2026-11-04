from model.validadores import exigir_texto


class MaterialEducativo:
    """Conteudo educativo (texto, video etc.) sobre uma especie."""
    def __init__(self, id_material: int, titulo: str, conteudo: str, tipo_midia: str) -> None:
        self._id_material = id_material
        self.titulo = titulo
        self.conteudo = conteudo
        self.tipo_midia = tipo_midia

    @property
    def id_material(self) -> int:
        return self._id_material

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self._titulo = exigir_texto(valor, "Titulo")

    def __str__(self) -> str:
        return f"MaterialEducativo({self.titulo}, {self.tipo_midia})"
