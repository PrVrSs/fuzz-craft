import ast
import tokenize
from typing import Any, NamedTuple

from fuzz_craft.file_manager import FileManager


def read_lines(filename: str) -> list[str]:
    with tokenize.open(filename) as fd:
        return fd.readlines()


def make_ast(lines: list[str]) -> ast.AST:
    return ast.parse(''.join(lines))


class Argument(NamedTuple):
    arg: str
    type_: str


class FunctionMeta:
    def __init__(self, name: str, arguments=None):
        self.name = name
        self._arguments = arguments

    @property
    def is_full_annotated(self) -> bool:
        return all([
            argument is not None
            for argument in self._arguments
        ])


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self._functions = []

    def run(self, node: ast.AST):
        self.generic_visit(node)
        return self._functions

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self._functions.append(
            FunctionMeta(
                name=node.name,
                arguments=self._prepare_arguments(node.args)
            )
        )

    def _prepare_annotation(self, annotation):
        match annotation:
            case ast.Name():
                return annotation.id
            case ast.Subscript():
                return Exception(f'Not supported {annotation!r}')
            case ast.BinOp():
                return Exception(f'Not supported {annotation!r}')
            case None:
                return
            case _:
                raise Exception(f'Unknown {annotation!r}')

    def _prepare_argument(self, node: ast.arg):
        try:
            return self._prepare_annotation(node.annotation)
        except Exception as exc:
            pass

    def _prepare_arguments(self, node: ast.arguments):
        return [
            self._prepare_argument(argument)
            for argument in node.args
        ]


class Processor:
    def __init__(self, file_manager: FileManager):
        self._file_manager = file_manager

    def run(self):
        return [
            FunctionVisitor().run(node=make_ast(read_lines(filename=py_file)))
            for py_file in self._file_manager.py_source
        ]
