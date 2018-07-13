import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


def start_communicator():
    # TODO Start communicator
    logger.debug("Message queue started.")


class CommunicatorConfig(AppConfig):
    name = 'communicator'

    @staticmethod
    def ready():
        start_communicator()
