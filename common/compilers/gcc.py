"""GCC backend."""
import os
import subprocess
import tempfile

CompileCommand = "gcc {source} -o {target} -lm {optimize}"


def compile_source_code_to(source_code: str,
                           target_file: str,
                           optimize_flag=False):
    """Compile code into executing target file."""
    with tempfile.TemporaryDirectory() as work_place:
        source_file = os.path.join(work_place, 'source.c')
        with open(source_file, 'w') as f:
            f.write(source_code)
        compile_source_file_to(
            source_file,
            target_file,
            optimize_flag
        )


def compile_source_file_to(source_file: str,
                           target_file: str,
                           optimize_flag=False):
    """Compile source file into executing target file."""
    compile_command = CompileCommand.format(
        source=source_file,
        target=target_file,
        optimize='-O2' if optimize_flag else ''
    )
    subprocess.run(
        compile_command,
        timeout=5.0,
        check=True,
        shell=True
    )
