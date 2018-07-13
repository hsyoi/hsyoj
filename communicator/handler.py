import queue
import threading
import uuid

from common.judge import JudgeResult, judge, SUPPORTED_LANGUAGE_SUFFIXES
from problems.models import Problem
from records.models import Record
from users.models import User
from .message_queue import get_message_queue
from .result_queue import Result, ResultQueue
from .task_queue import Task, TaskQueue


class JudgingTasks:
    def __init__(self):
        self.lock = threading.Lock()
        self.dict = dict()

    def add_task(self, task: Task):
        with self.lock:
            self.dict[task.judge_id] = task

    def pop_task(self, judge_id: uuid.UUID) -> Task:
        with self.lock:
            task = self.dict.pop(judge_id)
        return task


class Handler(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)

        self.available_judges = queue.Queue()

        self.message_queue = get_message_queue()
        self.task_queue = TaskQueue()
        self.result_queue = ResultQueue()
        self.judging_tasks = JudgingTasks()

        self.message_handler = MessageHandler(self)
        self.task_handler = TaskHandler(self)
        self.result_handler = ResultHandler(self)

    def run(self):
        self.message_queue.start()
        self.task_handler.start()
        self.result_handler.start()


class _BaseHandler(threading.Thread):
    def __init__(self, owner: Handler):
        super().__init__(daemon=True)

        self.owner = owner

    def run(self):
        while True:
            self.handle()

    def handle(self):
        raise NotImplementedError


class MessageHandler(_BaseHandler):
    def handle(self):
        socket_id, content = self.owner.message_queue.recv()
        self.owner.available_judges.put(socket_id)

        result = Result.from_json(content)

        if not result:
            return
        self.owner.result_queue.put(result)


class TaskHandler(_BaseHandler):
    def handle(self):
        task = self.owner.task_queue.get()

        try:
            judge_machine = self.owner.available_judges.get(timeout=1.0)

        # No judge machine is available
        # And judge at local
        except queue.Empty:
            threading.Thread(
                target=self._judge_local,
                args=(task,),
            )

        # Send the task to a judge machine
        else:
            self.owner.judging_tasks.add_task(task)
            self.owner.message_queue.send(
                judge_machine,
                task.to_json().encode()
            )

    def _judge_local(self, task: Task):
        results = judge(
            source_code=task.source_code,
            language_suffix=SUPPORTED_LANGUAGE_SUFFIXES[task.compiler][0],
            **task.problem.get_problem_config()
        )
        result = Result(
            judge_id=task.judge_id,
            *results
        )
        self.owner.result_queue.put(result)


class ResultHandler(_BaseHandler):
    def handle(self):
        result = self.owner.result_queue.get()

        record = self._generate_record(
            **self._generate_full_judge_information(result)
        )

        record.save()

    def _generate_full_judge_information(self, result: Result) -> dict:
        """Generate full judge information from the result and original task.

        Raise KeyError if the original task is not exist.
        """
        original_task = self.owner.judging_tasks.pop_task(result.judge_id)

        res = {
            'user': original_task.user,
            'source_code': original_task.source_code,
            'compiler': original_task.compiler,
            'problem': original_task.problem,
            'result': result,
        }

        return res

    def _generate_record(self,
                         user: User,
                         source_code: str,
                         compiler: str,
                         problem: Problem,
                         result: Result) -> Record:
        """Generate record from problem and source code."""
        accepted_flag = all(
            map(
                lambda res: res == 0,
                result.results
            )
        )

        record = Record(
            user=user,
            problem=problem,
            compiler=compiler,
            source_code=source_code,
            accepted_flag=accepted_flag,
            # TODO Add running time and memory cost
            # running_time = models.DurationField(editable=False)
            # memory_cost = models. ...
        )

        # Add result for per test_case
        if result.is_compilation_error():
            self._add_ce_result(record)
        else:
            self._add_results(
                record,
                result.results,
                problem.testcase_set.all()
            )

        return record

    @staticmethod
    def _add_ce_result(record: Record):
        record.testcaseresult_set.create(
            result_code=JudgeResult.CE.value,
            test_case=None,
        )

    @staticmethod
    def _add_results(record: Record, judge_results, test_cases):
        assert len(judge_results) == len(test_cases)
        for result, case in zip(judge_results, test_cases):
            record.testcaseresult_set.create(
                result_code=result.value,
                test_case=case,
            )
