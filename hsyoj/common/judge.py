"""Functions to run the program and check the answer."""
import difflib
import enum
import os
import shutil
import subprocess
import tempfile

from .compiler import CompileResult, get_compiler


class JudgeResult(enum.Enum):
    """All judge results"""
    AC = 0  # Accept
    WA = 1  # WrongAnswer
    TLE = 2  # TimeLimitExceeded
    RE = 3  # RuntimeError
    MLE = 4  # MemoryLimitExceeded


def diff_bytes(bytes1: bytes, bytes2: bytes) -> bool:
    """Diff two bytes just like diff command.

    The function ignore empty line at the end of file and space at the end of lines.
    Return True if two bytes are different, return False if they are the same.
    """
    differ = difflib.Differ()
    return not all(map(lambda s: s.startswith('  '), differ.compare(
        [s.rstrip() for s in bytes1.rstrip().splitlines()],
        [s.rstrip() for s in bytes2.rstrip().splitlines()]
    )))


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


def judge(language: str, source_code: str,
          test_cases: list, input_file: str, output_file: str,
          time_limit: float=1.0, memory_limit: float=128.0,  # TODO: Memory limit support
          **kwargs):
    """Judge the source code.

    It is not recommended for using stdio instead of file IO.
    The program maybe report TLE wrongly because of OS buffers.

    Arguments:
    language: 'c', 'cpp', etc.
    source_code: source code.
    test_cases: a list of tuples of file names. [('1.in', '1.ans'), ('2.in', '2.ans')]
    """
    with tempfile.TemporaryDirectory() as work_dir:
        compiler = get_compiler(language)
        # Compile the source file
        binary = tempfile.mkstemp(dir=work_dir)
        os.close(binary[0])
        binary = binary[1]
        compiler_result = compiler.compile_code(source_code, target=binary,
                                                O2=kwargs.get('O2', True))
        if compiler_result is CompileResult.CE:
            return [compiler_result]

        # Run the program
        def run():
            """Yield a list of result."""
            stdio = kwargs.get('stdio', False)

            for test_case in test_cases:
                with tempfile.TemporaryDirectory(dir=work_dir) as exec_dir:
                    input_file_path = os.path.join(exec_dir, input_file)
                    output_file_path = os.path.join(exec_dir, output_file)
                    input_case = test_case[0]
                    answer_case = test_case[1]
                    shutil.copy(binary, exec_dir)
                    shutil.copy(input_case, input_file_path)

                    try:
                        subprocess.run(
                            f"{binary}" if not stdio else
                            f"{binary} < {input_file_path} > {output_file_path}",
                            timeout=time_limit,
                            check=True,
                            shell=True
                        )
                    except subprocess.CalledProcessError:
                        yield JudgeResult.RE
                    except subprocess.TimeoutExpired:
                        yield JudgeResult.TLE

                    # Check answer
                    if not diff_files(output_file_path, answer_case):
                        yield JudgeResult.AC
                    else:
                        yield JudgeResult.WA

        return list(run())
