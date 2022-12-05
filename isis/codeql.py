import shutil
from pathlib import Path
from subprocess import check_call
from typing import final

from isis.settings import settings


ROOT = '.codeql'
DATABASE = 'database'
QUERIES_BASE_PATH: Path = Path(__file__).parent.resolve() / 'ql'


def is_codeql_available(cmd: str = 'codeql') -> bool:
    if shutil.which(cmd) is None:
        return False

    return True


def reset_directory(path: str) -> None:
    if Path(path).exists():
        shutil.rmtree(path)

    Path(path).mkdir(parents=True)


def exec_cmd(cmd: list[str]):
    return check_call(cmd)


class QL:

    LANGUAGE = None
    QUERY_PATH = None

    def __init__(self, ql, source, project_directory: Path, is_first_run: bool = True):
        self._ql = ql
        self._source = source
        self._project_directory = project_directory

        assert is_codeql_available(self._ql) is True, 'Not found CodeQL.'
        assert self.LANGUAGE is not None, 'Langauge should be defined.'

        if is_first_run is True:
            self._create_output_directory()
            self._create_database_directory()
            self._init_database()

    def update_database(self):
        shutil.rmtree(self._database)
        self._init_database()

    def run_query(self, query):
        exec_cmd(self._codeql_query_cmd(query))
        exec_cmd(self._decode_cmd(query))

    @property
    def _root(self) -> Path:
        return self._project_directory / ROOT

    @property
    def _database(self) -> Path:
        return self._root / DATABASE

    def _create_output_directory(self) -> None:
        Path(self._root).mkdir(parents=True, exist_ok=True)

    def _create_database_directory(self) -> None:
        Path(self._database).mkdir(parents=True, exist_ok=True)

    def _init_database(self) -> None:
        exec_cmd(self._create_database_cmd)

    @property
    def _create_database_cmd(self) -> list[str]:
        return [
            self._ql,
            'database', 'create',
            str(self._database),
            f'--language={self.LANGUAGE}',
            f'--source-root={self._source}',
        ]

    def _codeql_query_cmd(self, query_file: str):
        return [
            self._ql,
            'query', 'run',
            str(self.QUERY_PATH / query_file),
            '-o', str((self._root / query_file).with_suffix('.bqrs')),
            '-d', str(self._database)
        ]

    def _decode_cmd(self, query_file: str):
        return [
            self._ql,
            'bqrs', 'decode',
            '--format=csv',
            str((self._root / query_file).with_suffix('.bqrs')),
            '-o', str((self._root / query_file).with_suffix('.csv')),
        ]


@final
class PY(QL):
    LANGUAGE = 'python'
    QUERY_PATH = QUERIES_BASE_PATH / 'python'


@final
class CPP(QL):
    LANGUAGE = 'cpp'
    QUERY_PATH = QUERIES_BASE_PATH / 'c-cpp'

    @property
    def _create_database_cmd(self):
        return [
            *super()._create_database_cmd,
            '--command=make',
        ]


def run():
    py_ql = PY(
        ql=settings['codeQL'],
        source=settings['source'],
        project_directory=Path(settings['project_directory']),
        # is_first_run=False,
    )

    py_ql.run_query('function.ql')


if __name__ == '__main__':
    run()
