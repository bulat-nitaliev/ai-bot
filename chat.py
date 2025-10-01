from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import GigaChat
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import settings
from utils import get_redis_history

# chat_history = InMemoryChatMessageHistory()



messages = [
    (
        "system",
        "Вы эксперт в {domain}. Ваша задача — ответить на вопрос как можно короче.",
    ),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
]
prompt = ChatPromptTemplate(messages)

trimmer = trim_messages(
    strategy="last",
    token_counter=len,
    max_tokens=10,
    start_on="human",
    end_on="human",
    include_system=True,
    allow_partial=False,
)

llm = GigaChat(
    credentials=settings.GIGACHAT_CREDENTIALS,
    scope="GIGACHAT_API_PERS",
    model="GigaChat-2-Pro",
    temperature=0.3,
    max_tokens=1000,
    verify_ssl_certs=False,
)

chain = prompt | trimmer | llm
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_redis_history,
    input_messages_key="question",
    history_messages_key="history",
)
final_chain = chain_with_history | StrOutputParser()
