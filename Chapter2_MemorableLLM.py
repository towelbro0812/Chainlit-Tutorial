from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig
import chainlit as cl
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE

def get_history_table(message_history):
    table = Table(show_header=True, header_style="bold magenta",box=SQUARE)
    table.add_column("角色", style="cyan")
    table.add_column("內容", style="white")
    for message in message_history:
        table.add_row(message["role"], message["content"])
        if message["role"] == "assistant":
            table.add_row("-"*10,"–" * 100)
    return table

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("message_history",[])
    model = ChatOllama(model = "llama3.1",
                       keep_alive = 300,
                       temperture = 0,
                       base_url='http://host.docker.internal:11434',
                       callbacks=[cl.LangchainCallbackHandler()],
                       )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a professional programming expert skilled in using various algorithms to solve complex technical problems. Your task is to design solutions that meet specified requirements using the designated programming language, ensuring optimal performance and efficiency. Please maintain code readability and maintainability while minimizing unnecessary complexity and duplication. Additionally, respond to users in their selected language (such as English or Traditional Chinese) and ensure that responses are clear and understandable in both languages."
            ),
            MessagesPlaceholder(variable_name="history"),
        ]
    )
    chain = prompt | model | StrOutputParser()

    cl.user_session.set("chain", chain)
    await cl.Message(content="你好，我是你的程式小助手，有需要詢問什麼有關於程式碼的問題都可以問我喔!").send()


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})
    msg = cl.Message(content="")
    
    async for chunk in chain.astream(
        input={"history": message_history},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()])
        ):
        # print(chunk)
        await msg.stream_token(chunk)
    
    message_history.append({"role": "assistant", "content": msg.content})
    console = Console()
    console.print(get_history_table(message_history))
    await msg.send()

