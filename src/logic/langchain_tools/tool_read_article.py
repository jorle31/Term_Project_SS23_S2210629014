"""
File that contains the custome LangChain tool read_Article.
"""
import logging
from typing import Literal

from langchain.agents import tool
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from src.logic.config import secrets as config_secrets
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

@tool
def read_article(news: str) -> str:
    """
    Useful for when you need to read an article and understand its key points. 
    Input is the text of a news article. Output are the key points of the article.
    """
    system_template: Literal = """You are a helpful assistant. Your job is to read a news article and return its key point."""
    system_message_prompt: SystemMessagePromptTemplate = SystemMessagePromptTemplate.from_template(system_template)
    human_template: Literal = """Please identify the key points of the following news article: {news}"""
    human_message_prompt: HumanMessagePromptTemplate = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    llm: ChatOpenAI = ChatOpenAI(
        temperature=0, 
        client=chat_prompt, 
        openai_api_key=config_secrets.read_openai_credentials()
    )
    llm_chain: LLMChain = LLMChain(llm=llm, prompt=chat_prompt)
    key_points: str = llm_chain.run(news=news)
    logging.info("Done reading article.")
    return key_points