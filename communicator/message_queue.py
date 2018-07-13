import zmq


class MessageQueue:
    def __init__(self, address, port):
        self.address = address
        self.port = port

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)

    def start(self):
        self.socket.bind(f"tcp://{self.address}:{self.port}")

    def send(self, socket_id: bytes, task: bytes):
        """Send a message to client(*socket_id*).

        The format should be like this: ::

          +-------------+
          |  SOCKET ID  |
          +-------------+
          |     b""     |
          +-------------+
          | TASK (json) |
          +-------------+
        """
        self.socket.send_multipart([
            socket_id,
            b'',
            task,
        ])

    def recv(self) -> tuple:
        """Receive a message from ZMQ Socket.

        The format should be like this: ::

          +---------------+
          |   SOCKET ID   |
          +---------------+
          |      b""      |
          +---------------+
          | RESULT (json) |
          +---------------+
        """
        socket_id, _, result = self.socket.recv_multipart()
        return socket_id, result


def _read_config():
    try:
        from . import settings
    except ImportError:
        raise ImportError("Cannot read config file.")
    return {
        'address': settings.LISTENING_ADDRESS,
        'port': settings.LISTENING_PORT,
    }


def get_message_queue():
    return MessageQueue(**_read_config())
