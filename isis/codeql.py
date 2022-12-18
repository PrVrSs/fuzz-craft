import shutil
from pathlib import Path
from typing import Any, Type, final

from .exceptions import IsisException
from .utils import is_cmd_available, exec_cmd


ROOT: str = '.codeql'
DATABASE: str = 'database'
QUERIES_BASE_PATH: Path = Path(__file__).parent.resolve() / 'ql'
LANGUAGE_QL_MAP: dict[str, Type['BaseQL']] = {}


class BaseQL:
    LANGUAGE: str
    QUERY_PATH: Path

    def __init__(
            self,
            codeql_cmd: str,
            source: str,
    ):
        self._codeql_cmd = codeql_cmd
        self._source = Path(source)

        assert is_cmd_available(self._codeql_cmd) is True, 'Not found CodeQL.'
        assert self.LANGUAGE is not None, 'Langauge should be defined.'

        self._create_output_directory()
        self._create_database_directory()

    def __init_subclass__(cls) -> None:
        LANGUAGE_QL_MAP[cls.__name__.lower()] = cls

    def init_database(self) -> None:
        exec_cmd(self._create_database_cmd)

    def update_database(self) -> None:
        shutil.rmtree(self._database)
        self.init_database()

    def run_query(self, query: str) -> None:
        exec_cmd(self._codeql_query_cmd(query))
        exec_cmd(self._decode_cmd(query))

    @property
    def _root(self) -> Path:
        return self._source / ROOT

    @property
    def _database(self) -> Path:
        return self._root / DATABASE

    def _create_output_directory(self) -> None:
        Path(self._root).mkdir(parents=True, exist_ok=True)

    def _create_database_directory(self) -> None:
        Path(self._database).mkdir(parents=True, exist_ok=True)

    @property
    def _create_database_cmd(self) -> list[str]:
        return [
            self._codeql_cmd,
            'database', 'create',
            str(self._database),
            f'--language={self.LANGUAGE}',
            f'--source-root={str(self._source)}',
            '--overwrite',
        ]

    def _codeql_query_cmd(self, query_file: str) -> list[str]:
        return [
            self._codeql_cmd,
            'query', 'run',
            str(self.QUERY_PATH / query_file),
            '-o', str((self._root / query_file).with_suffix('.bqrs')),
            '-d', str(self._database)
        ]

    def _decode_cmd(self, query_file: str) -> list[str]:
        return [
            self._codeql_cmd,
            'bqrs', 'decode',
            '--format=csv',
            str((self._root / query_file).with_suffix('.bqrs')),
            '-o', str((self._root / query_file).with_suffix('.csv')),
        ]


@final
class PY(BaseQL):
    LANGUAGE = 'python'
    QUERY_PATH = QUERIES_BASE_PATH / 'python'


@final
class CPP(BaseQL):
    LANGUAGE = 'cpp'
    QUERY_PATH = QUERIES_BASE_PATH / 'c-cpp'

    @property
    def _create_database_cmd(self) -> list[str]:
        return [
            *super()._create_database_cmd,
            '--command=make',
        ]


class CodeQL:
    def __call__(self, language: str, /, **kwargs: Any) -> BaseQL:
        try:
            return LANGUAGE_QL_MAP[language](**kwargs)
        except KeyError:
            raise IsisException(f'Not supported: {language}') from None


codeql = CodeQL()
