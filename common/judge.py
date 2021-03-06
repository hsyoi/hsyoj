"""Provide functions to judge the code."""
import difflib
import enum
import os
import shutil
import subprocess
import tempfile

from .compiler import SUPPORTED_LANGUAGE_SUFFIXES, get_compiler


class JudgeResult(enum.Enum):
    """All judge results."""

    CE = -1  # CompilationError
    AC = 0  # Accepted
    WA = 1  # WrongAnswer
    TLE = 2  # TimeLimitExceeded
    RE = 3  # RuntimeError
    MLE = 4  # MemoryLimitExceeded


def diff_bytes(bytes1: bytes, bytes2: bytes) -> bool:
    """Diff two bytes just like diff command.

    The function ignore empty lines at the end of file
    and spaces at the end of lines.

    Return `True` when two bytes are different,
    return `False` if they are the same.
    """
    differ = difflib.Differ()
    return not all(
        map(
            lambda s: s.startswith('  '),
            differ.compare(
                [s.rstrip() for s in bytes1.rstrip().splitlines()],
                [s.rstrip() for s in bytes2.rstrip().splitlines()]
            )
        )
    )


def judge(source_code: str,
          language_suffix: str,
          test_cases: list,
          input_file_name: str,
          output_file_name: str,
          time_limit: float = 1.0,
          memory_limit: float = 256.0,
          stdio_flag: bool = False,
          optimize_flag: bool = False):
    """Judge the source code.

    Using stdio instead of file IO is not recommended because it may cause
    TLE by OS buffers.


    Arguments

    :source_code: The source code
    :language_suffix: One of '.c', '.cpp', etc
    :test_cases: A list of tuples of input content and answer.
                 For example, in 'A+B Problem', [('13 5', '18'), ('1 2', '3')].
    :input_file_name: 'a+b.in'
    :output_file_name: 'a+b.out'
    :time_limit: seconds
    :memory_limit: Mb
    :stdio_flag: Whether use stdio
    :optimize_flag: Whether use optimize

    Returned:

      Return a list of judge result.
      [JudgeResult.AC, JudgeResult.AC, ...]
    """
    try:
        compiled_file = _compile_source_code(
            compiler=_get_compiler_by_suffix(
                language_suffix
            ),
            source_code=source_code,
            optimize_flag=optimize_flag
        )

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return [JudgeResult.CE]

    else:
        result = [
            _judge_test_case(
                test_case=test_case,
                compiled_file=compiled_file,
                input_file_name=input_file_name,
                output_file_name=output_file_name,
                time_limit=time_limit,
                memory_limit=memory_limit,
                stdio_flag=stdio_flag,
            ) for test_case in test_cases
        ]

        os.remove(compiled_file)

        return result


def _compile_source_code(compiler, source_code, optimize_flag):
    # Compile the source file
    executing_file = tempfile.mkstemp(suffix='.exe')
    os.close(executing_file[0])
    executing_file = executing_file[1]
    compiler.compile_source_code_to(
        source_code=source_code,
        target_file=executing_file,
        optimize_flag=optimize_flag
    )
    return executing_file


def _judge_test_case(test_case,
                     compiled_file,
                     input_file_name,
                     output_file_name,
                     time_limit,
                     memory_limit,
                     stdio_flag):
    with tempfile.TemporaryDirectory() as workspace:
        input_content, answer = test_case
        input_file, output_file, executing_file = \
            _prepare_running_workspace(
                workspace=workspace,
                compiled_file=compiled_file,
                input_content=input_content,
                input_file_name=input_file_name,
                output_file_name=output_file_name
            )

        result = _execute_program(
            stdio_flag,
            executing_file=executing_file,
            input_file=input_file,
            output_file=output_file,
            time_limit=time_limit,
            memory_limit=memory_limit,
        )

        if result is not None:
            return result

        return _compare_output_file_and_answer(
            output_file=output_file,
            answer=answer
        )


def _prepare_running_workspace(workspace,
                               compiled_file,
                               input_content,
                               input_file_name,
                               output_file_name):
    input_file = os.path.join(workspace, input_file_name)
    output_file = os.path.join(workspace, output_file_name)
    executing_file = os.path.join(
        workspace,
        os.path.basename(compiled_file)
    )
    shutil.copy(compiled_file, executing_file)
    with open(input_file, 'w') as f:
        f.write(input_content)
    return input_file, output_file, executing_file


def _execute_program(stdio_flag,
                     executing_file,
                     input_file,
                     output_file,
                     time_limit,
                     memory_limit
                     ):
    try:
        command = f"{executing_file}"
        if stdio_flag:
            command += f" < {input_file} > {output_file}"
        subprocess.run(
            command,
            timeout=time_limit,
            check=True,
            shell=True
        )
    except subprocess.CalledProcessError:
        return JudgeResult.RE
    except subprocess.TimeoutExpired:
        return JudgeResult.TLE
    else:
        return None


def _compare_output_file_and_answer(output_file, answer):
    with open(output_file, 'rb') as output:
        if not diff_bytes(output.read(), answer.encode()):
            return JudgeResult.AC
        return JudgeResult.WA


def _get_compiler_by_suffix(suffix: str):
    for compiler, language_suffixes in SUPPORTED_LANGUAGE_SUFFIXES.items():
        if suffix in language_suffixes:
            return get_compiler(compiler)
    raise NotImplementedError("Language not supported.")
