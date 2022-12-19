from isis.codeql import codeql
from isis.settings import settings
from isis.template import TemplateEnum, Template
from isis.targets import CPP
from isis.file_manager import FileManager


class Harness:
    def __init__(self, source, codeql_cmd, template, language):
        self._file_manager = FileManager(source=source)
        self._codeql = codeql(
            language,
            codeql_cmd=codeql_cmd,
            file_manager=self._file_manager
        )
        self._targets = CPP(file_manager=self._file_manager)
        self._template = Template(template=template)

    def run(self):
        codeql_output = self._codeql.run_query('function.ql')
        data = self._targets.generate(function_ql=codeql_output)

        for function in data:
            output = (self._file_manager.harness / function.name).with_suffix('.cc')
            output.write_text(self._template.render(function_body='\n\t'.join(function.data)))


if __name__ == '__main__':
    Harness(
        source=settings['source'],
        codeql_cmd=settings['codeQL'],
        template=TemplateEnum.C_CPP_LIBFUZZER,
        language='cpp',
    ).run()
