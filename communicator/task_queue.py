import json
import queue
import uuid

from problems.models import Problem
from users.models import User


class Task:
    __slots__ = [
        'judge_id',

        # User Information
        'user',
        'source_code',
        'compiler',

        # Problem Information
        'problem',
    ]

    def __init__(self,
                 user: User,
                 source_code: str,
                 compiler: str,
                 problem: Problem):
        self.judge_id = uuid.uuid1()
        self.user = user

        self.source_code = source_code
        self.compiler = compiler

        self.problem = problem

    def to_json(self):
        task = {
            'judge_id': self.judge_id.hex,
            'user': self.user.username,

            'source_code': self.source_code,
            'compiler': self.compiler,
        }
        task.update(**self.problem.get_problem_config())

        return json.dumps(task)


class TaskQueue(queue.Queue):
    def get(self, *args, **kwargs) -> Task:
        return super().get(*args, **kwargs)

    def put(self, item: Task, **kwargs):
        super().put(item, **kwargs)
