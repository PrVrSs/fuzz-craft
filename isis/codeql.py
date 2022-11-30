import shutil
from pathlib import Path
from subprocess import check_call

from isis.exceptions import IsisException
from isis.settings import settings


QueryPath = Path(__file__).parent.resolve() / 'ql'
PythonQuery = QueryPath / 'python'


def create_database(codeql: str, output: str, target: str, source: str) -> int:
    return check_call(
        [
            codeql,
            'database', 'create',
            output,
            f'--language={target}',
            f'--source-root={source}',
        ]
    )


def is_codeql_available(cmd: str = 'codeql') -> bool:
    if shutil.which(cmd) is None:
        return False

    return True


def prepare_database_dir(path: str) -> None:
    if Path(path).exists():
        shutil.rmtree(path)

    Path(path).mkdir(parents=True)


def run_query(codeql: str, query: str, output: str, database: str) -> int:
    return check_call(
        [
            codeql,
            'query', 'run', query,
            '-o', output,
            '-d', database
        ]
    )


def decode_query(codeql: str, bqrs: str, output: str) -> int:
    return check_call(
        [
            codeql,
            'bqrs', 'decode',
            '--format=csv',
            bqrs,
            '-o', output,
        ]
    )


def init_database():
    prepare_database_dir(settings['database'])
    create_database(
        codeql=settings['codeQL'],
        output=settings['database'],
        target=settings['language'],
        source=settings['source'],
    )


def run():
    if not is_codeql_available(settings['CodeQL']):
        raise IsisException

    if settings['init_db'] is True:
        init_database()

    run_query(
        codeql=settings['codeQL'],
        query=str(PythonQuery / 'function.ql'),
        output=settings['query_result'],
        database=settings['database'],
    )
    decode_query(
        codeql=settings['codeQL'],
        bqrs=settings['query_result'],
        output=settings['decode_result'],
    )


if __name__ == '__main__':
    run()
