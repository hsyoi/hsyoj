"""Functions to run the program and check the answer."""
import difflib
import enum
import os
import shutil
import subprocess
import tempfile

from .compiler import CompileResult, get_compiler


class JudgeResult(enum.Enum):
    """All judge results."""

    AC = 0  # Accept
    WA = 1  # WrongAnswer
    TLE = 2  # TimeLimitExceeded
    RE = 3  # RuntimeError
    MLE = 4  # MemoryLimitExceeded


def get_compiler_by_suffix(suffix: str):
    if suffix in ('.c', ):
        return get_compiler('gcc')
    elif suffix in ('.cpp', '.cc', '.cxx'):
        return get_compiler('g++')
    else:
        raise NotImplementedError("Language not supported.")


def diff_bytes(bytes1: bytes, bytes2: bytes) -> bool:
    """Diff two bytes just like diff command.

    The function ignore empty line at the end of file
    and space at the end of lines.

    Return True if two bytes are different,
    return False if they are the same.
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


def diff_files(output_file: str, answer_file: str) -> bool:
    """Check the answer.

    Return True if there is no difference output_file and answer_file.
    """
    # TODO: Special judge support
    with open(output_file, 'rb') as f:
        output = f.read()
    with open(answer_file, 'rb') as f:
        answer = f.read()
    return diff_bytes(output, answer)


def judge(source_code: str, language_suffix: str,
          test_cases: list, input_file_name: str, output_file_name: str,
          time_limit: float=1.0, memory_limit: float=256.0,
          # TODO: Memory limit support
          stdio_flag=False,
          optimize_flag=False
          ):
    """Judge the source code.

    It is not recommended for using stdio instead of file IO.
    The program maybe report TLE wrongly because of OS buffers.

    Arguments:

    source_code: source code.
    language_suffix: '.c', '.cpp', etc.
    test_cases: a list of tuples of input content and answer
    For example, in 'A+B Problem', [('13 5', '18'), ('1 2', '3')]
    """
    compiler = get_compiler_by_suffix(language_suffix)

    # Compile the source file
    compiled_file = tempfile.mkstemp(suffix='.exe')
    os.close(compiled_file[0])
    compiled_file = compiled_file[1]

    compiler_result = compiler.compile_source_code_to(
        source_code=source_code,
        target_file=compiled_file,
        optimize_flag=optimize_flag
    )

    if compiler_result is CompileResult.CE:
        return [compiler_result]

    judge_results = []

    # Run the program
    for test_case in test_cases:
        with tempfile.TemporaryDirectory() as workspace:
            input_file_path = os.path.join(workspace, input_file_name)
            output_file_path = os.path.join(workspace, output_file_name)
            input_content, answer = test_case
            shutil.copy(compiled_file, workspace)
            executing_file = os.path.join(
                workspace,
                os.path.basename(compiled_file)
            )

            with open(input_file_path, 'w') as f:
                f.write(input_content)

            try:
                if not stdio_flag:
                    subprocess.run(
                        f"{executing_file}",
                        timeout=time_limit,
                        check=True,
                        shell=True
                    )
                else:
                    subprocess.run(
                        f"{executing_file} " +
                        f"< {input_file_path} " +
                        f"> {output_file_path}",
                        timeout=time_limit,
                        check=True,
                        shell=True
                    )
            except subprocess.CalledProcessError:
                judge_results.append(JudgeResult.RE)
            except subprocess.TimeoutExpired:
                judge_results.append(JudgeResult.TLE)

            # Check answer
            with open(output_file_path, 'rb') as output:
                if not diff_bytes(output.read(), answer.encode()):
                    judge_results.append(JudgeResult.AC)
                else:
                    judge_results.append(JudgeResult.WA)

    return judge_results
