from collections import defaultdict
from pathlib import Path

from isis.settings import settings
from isis.template import Template
from isis.codeql import run as codeql_run
from isis.utils import read_csv


def prepare_harness_dir():
    Path(settings['harness_dir']).mkdir(parents=True, exist_ok=True)


def harness():
    codeql_run()

    data = defaultdict(list)
    for row in read_csv(settings['decode_result']):
        data[row['func_name']].append(row['annotation'])

    prepare_harness_dir()

    template = Template()
    for function, arguments in data.items():
        file = str(Path(settings['harness_dir']) / f'fuzz_{function}.py')
        with open(file, mode='w', encoding='utf-8') as fd:
            fd.write(
                template.render(
                    function=function,
                    arguments=', '.join(arguments),
                )
            )


if __name__ == '__main__':
    harness()
