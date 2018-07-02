import typing

import zmq

from common.communicator import Communicator


class _MesageQueue(Communicator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.task_list = []

    def start(self):
        super().start()
        self.socket.bind(f"tcp://{self.address}:{self.port}")

    def recv(self) -> bytes:
        pass

    def send(self, message: typing.List[bytes]):
        pass

    def add_judge_task(self):
        pass


def _read_config():
    try:
        from . import settings
    except ImportError:
        raise ImportError("Cannot read config file.")
    return {
        'address': settings.LISTENING_ADDRESS,
        'port': settings.LISTENING_PORT,
    }


message_queue = _MesageQueue(socket_type=zmq.ROUTER, **_read_config())

__all__ = ['message_queue']
