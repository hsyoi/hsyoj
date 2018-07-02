from django.apps import AppConfig


def start_message_queue():
    pass


class CommunicatorConfig(AppConfig):
    name = 'communicator'

    @staticmethod
    def ready():
        start_message_queue()
