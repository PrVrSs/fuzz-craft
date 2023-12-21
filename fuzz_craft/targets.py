import re
from collections import defaultdict
from functools import cached_property
from typing import Any, Iterator, NamedTuple

import lief

from fuzz_craft.file_manager import FileManager
from fuzz_craft.fuzzers.libfuzzer import ConsumeBool, ConsumeFloatingPoint, ConsumeIntegral
from fuzz_craft.log import logger
from fuzz_craft.utils import read_csv


CPP_FUNCTION_QL = dict[tuple[str, str, str], list[tuple[str, str]]]


class CPPFunctionArgumentSchema(NamedTuple):
    type: str
    position: int


class CPPFunctionSchema(NamedTuple):
    name: str
    arguments: list[CPPFunctionArgumentSchema]
    return_type: str
    location: str

    def __str__(self):
        return f'{self.return_type} {self.name}({", ".join([f"{argument.type} arg_{index}" for index, argument in enumerate(self.arguments[::-1])])})'


def convert_ql_to_schema(data: CPP_FUNCTION_QL) -> list[CPPFunctionSchema]:
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


def get_template_argument(argument: str, position: int) -> str:
    if 'float' in argument or 'double' in argument:
        return f'auto argument_{position} = {ConsumeFloatingPoint(argument)};'

    if 'bool' in argument:
        return f'auto argument_{position} = {ConsumeBool(argument)};'

    return f'auto argument_{position} = {ConsumeIntegral(argument)};'


def prepare_double_pointer(argument: str, number: int) -> tuple[str, str]:
    template_argument = get_template_argument(argument=argument, position=number)

    template_argument_ptr = f'{argument} *ptr_{number} = &argument_{number};'
    template_argument_double_ptr = f'{argument} **double_ptr_{number} = &ptr_{number}'

    template_param = f'double_ptr_{number}'

    return '\n'.join([
        template_argument,
        template_argument_ptr,
        template_argument_double_ptr,
    ]), template_param


def prepare_pointer(argument: str, number: int) -> tuple[str, str]:
    template_argument = get_template_argument(argument=argument, position=number)

    template_argument_ptr = f'{argument} *ptr_{number} = &argument_{number};'
    template_param = f'ptr_{number}'

    return '\n\t'.join([template_argument, template_argument_ptr]), template_param


def prepare_type(argument: str, number: int):
    template_argument = get_template_argument(argument=argument, position=number)
    template_param = f'argument_{number}'

    return template_argument, template_param


ARGUMENT_REGEXP = re.compile(r'^(?P<Type>(?:\s?\w+)+)\s?(?P<Star>\*{0,3})(?:\[\])?$')


def prepare_argument(argument_type, position):
    result = ARGUMENT_REGEXP.match(argument_type)
    if result is None:
        return

    match len(result.group('Star')):
        case 1:
            return prepare_pointer(result.group('Type'), position)
        case 2:
            return prepare_double_pointer(result.group('Type'), position)
        case _:
            return prepare_type(result.group('Type'), position)


class Function:
    def __init__(self, file_manager: FileManager, functions_meta: list[CPPFunctionSchema]):
        self._file_manager = file_manager
        self._meta = functions_meta

    @cached_property
    def project_functions(self) -> list[CPPFunctionSchema]:
        return [
            function
            for function in self._meta
            if self._file_manager.in_project(function.location) and function.name != 'main'
        ]


class Result(NamedTuple):
    name: str
    data: Any


class Targets:
    def __init__(self, file_manager: FileManager):
        self._file_manager = file_manager

    def generate(self, function_ql: str) -> Iterator[Result]:
        raise NotImplementedError


class CPP(Targets):
    def generate(self, function_ql: str) -> list[CPPFunctionSchema]:
        functions = Function(
            file_manager=self._file_manager,
            functions_meta=cpp_function_ql(file=function_ql),
        )

        logger.info(f'Found {len(functions.project_functions)} functions')

        return functions.project_functions
