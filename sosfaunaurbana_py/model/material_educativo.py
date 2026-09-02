class MaterialEducativo:
    def __init__(self, id_material, titulo, conteudo, tipo_midia):
        self.id_material = id_material
        self.titulo = titulo
        self.conteudo = conteudo
        self.tipo_midia = tipo_midia

    def __str__(self):
        return f"MaterialEducativo({self.titulo}, {self.tipo_midia})"
