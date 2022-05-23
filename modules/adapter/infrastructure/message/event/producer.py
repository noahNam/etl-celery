from modules.adapter.infrastructure.message.broker.redis import redis
from modules.adapter.infrastructure.message.dto.message_dto import MessageDto
from modules.adapter.infrastructure.message.event.interface import MessageProducer
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class RedisMessageProducer(MessageProducer):
    def __init__(self):
        self.__producer = redis

    def send_message(
        self, topic: str | None, msg: MessageDto, key: str, logging: bool = False
    ):
        try:
            self.__producer.set(value=msg.to_dict(), key=key)
        except Exception as e:
            logger.error(
                "[RedisMessageProducer][send_message][Exception] {0}".format(e)
            )
            logger.error(
                "[RedisMessageProducer][send_message][Msg] {0}".format(msg.to_dict())
            )
            return

        if logging:
            logger.info("🚀[RedisMessageProducer][Send] {0}".format(msg.to_dict()))
