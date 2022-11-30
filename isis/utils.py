import csv
from typing import Iterator


def read_csv(file: str, ) -> Iterator[dict]:
    with open(file, mode='r', encoding='utf-8') as fd:
        for row in csv.DictReader(fd):
            yield row
