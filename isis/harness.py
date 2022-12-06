from collections import defaultdict
from pathlib import Path

from isis.codeql import codeql
from isis.settings import settings
from isis.template import render, TemplateEnum
from isis.utils import read_csv


def prepare_harness_dir():
    Path(settings['harness_dir']).mkdir(parents=True, exist_ok=True)


def harness():
    py_codeql = codeql(
        'py',
        codeql_cmd=settings['codeQL'],
        source=settings['source'],
        project_directory=settings['project_directory'],
    )
    py_codeql.run_query('function.ql')

    data = defaultdict(list)
    for row in read_csv(settings['decode_result']):
        data[row['func_name']].append(row['annotation'])

    prepare_harness_dir()

    for function, arguments in data.items():
        file = str(Path(settings['harness_dir']) / f'fuzz_{function}.py')
        with open(file, mode='w', encoding='utf-8') as fd:
            fd.write(
                render(
                    TemplateEnum.PY_ATHERIS,
                    function=function,
                    arguments=', '.join(arguments),
                )
            )


if __name__ == '__main__':
    harness()
