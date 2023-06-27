"""
File that contains the custome LangChain tool original_question.
"""
import logging

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone 
from langchain.agents import tool

from src.logic.config import secrets as config_secrets

global company_question
global risk_analysis_question

@tool
def original_question_scoring(question: str) -> str: 
    """
    This function is the original question that is used to get the original question. Input is the question what the original
    question is about. Output is the original question.
    """
    original_question = f"""You are a helpful assistant. An initial risk assessment for the company 
        {company_question} identified potential risk types. Your job is to calculate a risk score for each identified risk type based on the
        initial assessment: {risk_analysis_question}. Explain how you awarded the risk scores. Do not create more than 4 steps."""
    return original_question

def fill_question(company: str, risk_analysis: str) -> None:
    """
    This function fills the company and risk_analysis variables with the correct values.
    """
    company_question = company
    risk_analysis_question = risk_analysis
