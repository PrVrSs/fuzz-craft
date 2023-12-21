import csv
import shutil
from pathlib import Path
from subprocess import check_call
from typing import Iterator

import magic


def read_csv(file: str) -> Iterator[dict[str, str]]:
    with open(file, mode='r', encoding='utf-8') as fd:
        for row in csv.DictReader(fd):
            yield row


def is_cmd_available(cmd: str) -> bool:
    if shutil.which(cmd) is None:
        return False

    return True


def get_mime(file: str) -> str:
    return magic.from_file(file, mime=True)


def reset_directory(path: str) -> None:
    if Path(path).exists():
        shutil.rmtree(path)

    Path(path).mkdir(parents=True)


def exec_cmd(cmd: list[str]) -> int:
    return check_call(cmd)
