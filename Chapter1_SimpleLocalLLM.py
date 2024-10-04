from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig
import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
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
                "您是一位專業的程式設計專家，善於利用各種演算法達成一系列需求。",
            ),
            ("human", "{question}"),
        ]
    )
    chain = prompt | model | StrOutputParser()

    cl.user_session.set("chain", chain)


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")  
    
    msg = cl.Message(content="")
    async for chunk in chain.astream(
        input={"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()])
        ):
        # print(chunk)
        await msg.stream_token(chunk)

    await msg.send()
