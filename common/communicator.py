"""Low-level communication library."""
import abc
import typing

import zmq


class Communicator(abc.ABC):
    def __init__(self, socket_type, address, port):
        self.socket_type = socket_type
        self.address = address
        self.port = port

        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)

        self.started = False

    @abc.abstractmethod
    def start(self):
        self.started = True

    @abc.abstractmethod
    def recv(self) -> bytes:
        pass

    @abc.abstractmethod
    def send(self, message: typing.List[bytes]):
        pass
