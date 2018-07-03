import json


class Task:
    def __init__(self,
                 source_code: str,
                 language_suffix: str,
                 test_cases: tuple,
                 input_file_name: str,
                 output_file_name: str,
                 time_limit: float = 1.0,
                 memory_limit: float = 256.0,
                 stdio_flag: bool = False,
                 optimize_flag: bool = False):
        self.task = {
            'source_code': source_code,
            'language_suffix': language_suffix,
            'test_cases': test_cases,
            'input_file_name': input_file_name,
            'output_file_name': output_file_name,
            'time_limit': time_limit,
            'memory_limit': memory_limit,
            'stdio_flag': stdio_flag,
            'optimize_flag': optimize_flag,
        }

    def to_json(self):
        return json.dumps(self.task)

    @classmethod
    def from_json(cls, content):
        task = json.loads(content)
        return Task(**task)
