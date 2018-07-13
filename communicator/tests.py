import json
import uuid
from unittest.mock import MagicMock

import zmq
from django.test import TestCase

from common.judge import JudgeResult
from problems.models import Problem
from users.models import User
from .message_queue import MessageQueue
from .result_queue import Result
from .task_queue import Task


# TODO Add HandleTest


class MessageQueueTest(TestCase):
    """Test Message Queue.

    Testing MessageQueue needs permission to listen port 9999 on 127.0.0.1.
    """

    def setUp(self):
        address = "127.0.0.1"
        port = "9999"

        self.message_queue = MessageQueue(
            address,
            port
        )
        self.message_queue.start()

        class TestClient:
            """Test Client.

            Emulate a judge machine.
            """

            def __init__(self):
                self.context = zmq.Context()
                self.socket = self.context.socket(zmq.REQ)
                self.socket.connect(f"tcp://{address}:{port}")

            def send(self, content: bytes):
                self.socket.send(content)

            def recv(self) -> bytes:
                return self.socket.recv()

        self.client = TestClient()

    def test_message_queue(self):
        # Send INIT message
        self.client.send(b'[]')

        # Receive the INIT message
        socket_id1, init_message = self.message_queue.recv()
        self.assertEqual(init_message, b'[]')

        # Send JUDGE message
        self.message_queue.send(
            socket_id1,
            b''
        )

        # Receive the JUDGE message
        judge_message = self.client.recv()
        self.assertEqual(judge_message, b'')

        # Send RESULT message
        self.client.send(b'[-1]')

        # Receive the RESULT message
        socket_id2, result_message = self.message_queue.recv()
        self.assertEqual(socket_id1, socket_id2)
        self.assertEqual(result_message, b'[-1]')


class TaskTest(TestCase):
    def setUp(self):
        fake_user: User = MagicMock()
        fake_user.username = 'username'

        fake_problem: Problem = MagicMock()
        fake_problem.get_problem_config.return_value = {
            'input_file_name': "input.in",
            'output_file_name': "output.out",
            'test_cases': [
                ["", ""]
            ],
            'time_limit': 1.0,
            'memory_limit': 128.0,
            'stdio_flag': True,
            'optimize_flag': False,
        }

        self.fake_user = fake_user
        self.fake_problem = fake_problem
        self.task = Task(
            user=fake_user,
            source_code="int main() { return 0; }\n",
            compiler="g++",
            problem=fake_problem,
        )
        self.judge_id = self.task.judge_id

    def test_to_json(self):
        self.assertDictEqual(
            json.loads(
                self.task.to_json()
            ), {
                'judge_id': self.judge_id.hex,
                'user': 'username',

                'source_code': "int main() { return 0; }\n",

                'input_file_name': "input.in",
                'output_file_name': "output.out",
                'test_cases': [
                    ["", ""]
                ],
                'compiler': "g++",
                'time_limit': 1.0,
                'memory_limit': 128.0,
                'stdio_flag': True,
                'optimize_flag': False,
            }
        )


class ResultTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.AC = JudgeResult.AC
        cls.WA = JudgeResult.WA
        cls.CE = JudgeResult.CE

    def setUp(self):
        self.ac_result = Result(
            uuid.uuid1(),
            *[self.AC, self.AC, self.AC, self.AC]
        )

        self.wa_result = Result(
            uuid.uuid1(),
            *[self.WA, self.WA, self.WA, self.WA]
        )

        self.ce_result = Result(
            uuid.uuid1(),
            *[self.CE]
        )

    def test_is_accept(self):
        self.assertTrue(self.ac_result.is_accept())
        self.assertFalse(self.wa_result.is_accept())
        self.assertFalse(self.ce_result.is_accept())

    def test_is_compilation_error(self):
        self.assertFalse(self.ac_result.is_compilation_error())
        self.assertFalse(self.wa_result.is_compilation_error())
        self.assertTrue(self.ce_result.is_compilation_error())

    def test_from_json(self):
        judge_id = uuid.uuid1()
        result_json_content = {
            'judge_id': judge_id.hex,
            'results': [1, 1, 1, 1],
        }
        result = Result.from_json(
            json.dumps(result_json_content)
        )

        self.assertFalse(result.is_accept())
        self.assertFalse(result.is_compilation_error())
        self.assertEqual(result.judge_id, judge_id)
        self.assertListEqual(result.results, [1, 1, 1, 1])
