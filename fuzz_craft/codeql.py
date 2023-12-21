from pathlib import Path
from typing import Any, Type, final

from .exceptions import FuzzCraftException
from .file_manager import FileManager
from .utils import exec_cmd, is_cmd_available


QUERIES_BASE_PATH: Path = Path(__file__).parent.resolve() / 'ql'
LANGUAGE_QL_MAP: dict[str, Type['BaseQL']] = {}


class BaseQL:
    LANGUAGE: str
    QUERY_PATH: Path

    def __init__(self, codeql_cmd: str, file_manager: FileManager):
        self._codeql_cmd = codeql_cmd
        self._file_manager = file_manager

        assert is_cmd_available(self._codeql_cmd) is True, 'Not found CodeQL.'
        assert self.LANGUAGE is not None, 'Langauge should be defined.'

    def __init_subclass__(cls) -> None:
        LANGUAGE_QL_MAP[cls.__name__.lower()] = cls

    def init_database(self, options: list[str] | None = None) -> None:
        exec_cmd(self._create_database_cmd(options or []))

    def query(self, query: str) -> str:
        exec_cmd(self._codeql_query_cmd(query))
        exec_cmd(self._decode_cmd(query))

        return str((self._file_manager.queries / query).with_suffix('.csv'))

    def _create_database_cmd(self, options: list[str]) -> list[str]:
        return [
            self._codeql_cmd,
            'database', 'create',
            str(self._file_manager.database),
            f'--language={self.LANGUAGE}',
            f'--source-root={str(self._file_manager.source)}',
            '--overwrite',
            *options,
        ]

    def _codeql_query_cmd(self, query_file: str) -> list[str]:
        return [
            self._codeql_cmd,
            'query', 'run',
            str(self.QUERY_PATH / query_file),
            '-o', str((self._file_manager.queries / query_file).with_suffix('.bqrs')),
            '-d', str(self._file_manager.database)
        ]

    def _decode_cmd(self, query_file: str) -> list[str]:
        return [
            self._codeql_cmd,
            'bqrs', 'decode',
            '--format=csv',
            str((self._file_manager.queries / query_file).with_suffix('.bqrs')),
            '-o', str((self._file_manager.queries / query_file).with_suffix('.csv')),
        ]


@final
class PY(BaseQL):
    LANGUAGE = 'python'
    QUERY_PATH = QUERIES_BASE_PATH / 'python'


@final
class CPP(BaseQL):
    LANGUAGE = 'cpp'
    QUERY_PATH = QUERIES_BASE_PATH / 'c-cpp'


class CodeQL:
    def __call__(self, language: str, /, **kwargs: Any) -> BaseQL:
        try:
            return LANGUAGE_QL_MAP[language](**kwargs)
        except KeyError:
            raise FuzzCraftException(f'Not supported: {language}') from None


codeql = CodeQL()
