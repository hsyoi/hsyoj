"""Compiler for any code."""
import abc
import enum
import os
import shlex
import subprocess
import tempfile


class CompileResult(enum.Enum):
    CE = -1  # CompileError


class Compiler:
    """Common compiler for all languages."""
    SUFFIX = ''
    COMMAND = ""

    def __init__(self):
        self.command = self.COMMAND

    def compile_code(self, code: str, target: str, **kwargs):
        """Compile source code to target."""
        source_file = tempfile.NamedTemporaryFile(
            suffix=self.SUFFIX, mode='wt', delete=False)
        source_file.write(code)
        source_file.close()
        res = self.compile_file(source_file.name, target, **kwargs)
        os.remove(source_file.name)
        return res

    def compile_file(self, source, target, **kwargs):
        """Compile source file to target."""
        self.command = shlex.split(
            self.COMMAND.format(source=source, target=target))
        if kwargs.get('O2', False):
            self.command.append("-O2")
        return self.run()

    def run(self):
        """Start to compile the source."""
        try:
            subprocess.run(self.command, check=True, timeout=10)
        except subprocess.CalledProcessError:
            return CompileResult.CE
        except subprocess.TimeoutExpired:
            return CompileResult.CE
        return 0


class CCompiler(Compiler):
    """C Compiler."""
    SUFFIX = '.c'
    COMMAND = "g++ {source} -o {target} -lm"


class CppCompiler(Compiler):
    """Cpp Compiler."""
    SUFFIX = '.cpp'
    COMMAND = "g++ {source} -o {target} -lm"


def get_compiler(language: str=None) -> Compiler:
    if language in ('.c', 'c'):
        return CCompiler()
    if language in ('.cpp', '.cc', '.cxx', 'cpp'):
        return CppCompiler()
    return Compiler()
