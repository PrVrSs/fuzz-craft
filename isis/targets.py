from collections import defaultdict
from functools import cached_property
from operator import attrgetter
from pathlib import Path
from typing import NamedTuple

import lief

from isis.constants import SHARED_LIB
from isis.utils import read_csv, get_mime
from isis.settings import settings


class CPPFunctionArgumentSchema(NamedTuple):
    type: str
    position: int


class CPPFunctionSchema(NamedTuple):
    name: str
    arguments: list[CPPFunctionArgumentSchema]
    return_type: str
    location: str


def convert_ql_to_schema(data: dict[str, list[str]]) -> list[CPPFunctionSchema]:
    return [
        CPPFunctionSchema(
            name=function,
            return_type=return_type,
            location=location,
            arguments=[
                CPPFunctionArgumentSchema(type=type_, position=int(position))
                for type_, position in arguments
            ]
        )
        for (function, return_type, location), arguments in data.items()
    ]


def cpp_function_ql(file: str) -> list[CPPFunctionSchema]:
    data = defaultdict(list)
    for row in read_csv(file=file):
        data[(
            row['function'],
            row['return_type'],
            row['location'],
        )].append((
            row['argument_type'],
            row['argument_idx'],
        ))

    return convert_ql_to_schema(data=data)


class Function:
    def __init__(self, project: str, functions_meta: list[CPPFunctionSchema]):
        self._project = project
        self._meta = functions_meta

    @cached_property
    def project_functions(self) -> list[CPPFunctionSchema]:
        return [
            function
            for function in self._meta
            if Path(self._project) in Path(function.location).parents and function.name != 'main'
        ]


class File:
    def __init__(self, path):
        self._path = path
        self._binary = lief.parse(path)

    def make_dot_so(self, function: str = 'vulnerable_fn') -> None:
        self._binary.add_exported_function(
            address=self._binary.get_function_address(function),
            name=function,
        )
        self._binary[lief.ELF.DYNAMIC_TAGS.FLAGS_1].remove(lief.ELF.DYNAMIC_FLAGS_1.PIE)
        self._binary.write(f'lib_{function}.so')


def prepare_argument(argument_type):
    pass


class CPP:
    def __init__(self, directory: str, function_ql: str):
        self._directory = directory
        self._functions = Function(
            project=self._directory,
            functions_meta=cpp_function_ql(file=function_ql),
        )

    @cached_property
    def shared_object(self) -> list[str]:
        return [
            str(file)
            for file in Path(self._directory).rglob('*')
            if get_mime(str(file)) == SHARED_LIB
        ]

    def run(self) -> None:
        for function in self._functions.project_functions:
            for argument in sorted(function.arguments, key=attrgetter('position')):
                prepare_argument(argument_type=argument.type)


def main():
    cpp = CPP(
        directory=settings['source'],
        function_ql=settings['decode_result'],
    )
    cpp.run()


if __name__ == '__main__':
    main()
