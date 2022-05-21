from abc import ABC

from modules.adapter.infrastructure.message.dto.message_dto import MessageDto


class MessageProducer(ABC):
    def send_message(
        self, topic: str, msg: MessageDto, key: str, logging: bool = False
    ):
        pass