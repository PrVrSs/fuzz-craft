import json
from pathlib import Path

from llama_index.llms import OpenAI

from fuzz_craft.codeql import codeql
from fuzz_craft.file_manager import FileManager
from fuzz_craft.targets import CPP
from fuzz_craft.template import Template


class Harness:
    def __init__(self, source, codeql_cmd, template, language, api_key):
        self._file_manager = FileManager(source=source)
        self._codeql = codeql(
            language,
            codeql_cmd=codeql_cmd,
            file_manager=self._file_manager
        )
        self._targets = CPP(file_manager=self._file_manager)
        self._template = Template(template=template)
        self._llm = OpenAI(
            temperature=0,
            model='gpt-3.5-turbo',
            api_key=api_key,
        )

    def run(self):
        codeql_output = self._codeql.query('function.ql')
        data = self._targets.generate(function_ql=codeql_output)

        for function in data:
            query = self._template.render(
                source=str(Path(function.location).name),
                metadata=json.dumps(
                    {
                        'source': str(Path(function.location).name),
                        'annotation': str(function)
                    },
                    indent=2,
                )
            )
            response = self._llm.complete(query)

            output = (self._file_manager.harness / function.name).with_suffix('.cc')
            output.write_text(response.text)
