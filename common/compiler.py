"""Compiler for any code.

All supported compilers are listed in SUPPORTED_COMPILERS.
"""
import importlib

SUPPORTED_COMPILERS = (
    ('gcc', 'C (gcc)'),
    ('g++', 'C++ (g++)'),
)

SUPPORTED_LANGUAGE_SUFFIXES = {
    'gcc': (
        '.c',
    ),
    'g++': (
        '.cpp',
        '.cxx,'
        '.cc',
    ),
}

_compilers_alias = {
    'g++': 'gpp',
}


def get_compiler(compiler: str):
    """Get compiler for 'compiler'.

    `compiler` should be the name of the compiler.
    For example, use `get_compiler('gcc')` but not `get_compiler('c')`.
    """
    try:
        compiler = _compilers_alias.get(compiler, compiler)
        return importlib.import_module(
            '.' + compiler,
            'common.compilers'
        )
    except ImportError:
        raise NotImplementedError(
            f"Compiler {compiler} is not supported."
        )
