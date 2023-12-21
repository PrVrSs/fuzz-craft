from functools import cached_property
from pathlib import Path

from .constants import SHARED_LIB
from .utils import get_mime


ROOT: str = '.fuzz_craft'
DATABASE: str = 'database'
QUERIES: str = 'queries'
HARNESS: str = 'harness'


class FileManager:
    def __init__(self, source: str):
        self._source = Path(source)

        self._create_output_directory()
        self._create_database_directory()
        self._create_queries_directory()
        self._create_harness_directory()

    @property
    def source(self) -> Path:
        return self._source

    @property
    def root(self) -> Path:
        return self._source / ROOT

    @property
    def database(self) -> Path:
        return self.root / DATABASE

    @property
    def queries(self) -> Path:
        return self.root / QUERIES

    @property
    def harness(self) -> Path:
        return self.root / HARNESS

    @cached_property
    def shared_object(self) -> list[str]:
        return [
            str(file)
            for file in self._source.rglob('*')
            if get_mime(str(file)) == SHARED_LIB
        ]

    @cached_property
    def py_source(self) -> list[str]:
        return[
            str(file)
            for file in  self._source.rglob('*.py')
        ]

    def in_project(self, path: str) -> bool:
        return self._source in Path(path).parents

    def _create_output_directory(self) -> None:
        Path(self.root).mkdir(parents=True, exist_ok=True)

    def _create_database_directory(self) -> None:
        Path(self.database).mkdir(parents=True, exist_ok=True)

    def _create_queries_directory(self) -> None:
        Path(self.queries).mkdir(parents=True, exist_ok=True)

    def _create_harness_directory(self) -> None:
        Path(self.harness).mkdir(parents=True, exist_ok=True)
