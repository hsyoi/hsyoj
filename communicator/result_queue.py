import json
import queue
import uuid


class Result:
    __slots__ = [
        'judge_id',
        'results',
    ]

    def __init__(self, judge_id: uuid.UUID, *results):
        self.judge_id = judge_id
        self.results = [result.value for result in results]

    def is_accept(self) -> bool:
        return all(
            map(
                lambda res: res == 0,
                self.results
            )
        )

    def is_compilation_error(self) -> bool:
        return self.results[0] == -1

    @staticmethod
    def from_json(content):
        content = json.loads(content)

        # When a judge machine connect to the server for the first time
        # It will send a empty list
        if not content:
            return None

        res = Result(
            uuid.UUID(hex=content['judge_id']),
            *[]
        )
        res.results = content['results']
        return res


class ResultQueue(queue.Queue):
    def get(self, *args, **kwargs) -> Result:
        return super().get(*args, **kwargs)

    def put(self, item: Result, **kwargs):
        super().put(item, **kwargs)
