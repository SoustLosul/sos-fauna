"""Excecoes personalizadas do SOS Fauna Urbana.

Hierarquia:
    SosFaunaError                  (base de todos os erros do sistema)
    ├── ValidacaoError             (dado invalido; tambem e um ValueError)
    │   ├── StatusInvalidoError    (status inexistente ou operacao nao permitida no status atual)
    │   └── RegistroDuplicadoError (email/matricula ja cadastrados)
    └── PersistenciaError          (falha ao ler ou gravar os arquivos de dados)
"""


class SosFaunaError(Exception):
    """Erro base do sistema."""


class ValidacaoError(SosFaunaError, ValueError):
    """Dado invalido. Herda tambem de ValueError, entao `except ValueError` continua funcionando."""


class StatusInvalidoError(ValidacaoError):
    """Status inexistente ou operacao nao permitida no status atual."""


class RegistroDuplicadoError(ValidacaoError):
    """Tentativa de cadastrar um valor que deveria ser unico (email, matricula)."""


class PersistenciaError(SosFaunaError):
    """Falha ao ler ou gravar os arquivos de dados."""
