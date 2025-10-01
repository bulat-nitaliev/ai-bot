from config import settings
from langchain_community.chat_message_histories import RedisChatMessageHistory
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def get_redis_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        session_id=session_id, url=settings.REDIS_URL
    )