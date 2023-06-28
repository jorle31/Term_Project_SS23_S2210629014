"""
File that contains the main application.
"""
from typing import List

import streamlit as st
from langchain.docstore.document import Document

from src.logic.keyword_generation import KeywordGenerator
from src.data.sources.news_extraction import NewsExtractor
from src.logic.risk_analysis import RiskAnalysis
from src.logic.feedback_loop import FeedbackLoop
from src.logic.helper_functionality.news_check.news_checklist import NewsChecklist
from src.logic.helper_functionality.text_summarization import TextSummarizer
from src.logic.helper_functionality.document_indexation import Indexer

import src.logic.config.secrets as config_secrets

import os
import dotenv
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = config_secrets.read_openai_credentials()

st.set_page_config(page_title="Risky Business", page_icon="📈")

# define the singletons
keyword_generator = KeywordGenerator()
news_extractor = NewsExtractor()
index = Indexer()
news_checklist = NewsChecklist()
text_summarizer = TextSummarizer()
risk_analysis = RiskAnalysis()

# define the session state
if "news" not in st.session_state:
    st.session_state.news = []
    st.session_state.disabled = False

if "keywords" not in st.session_state:
    st.session_state.keywords = []
    st.session_state.disabled = False

if "keyword_num" not in st.session_state:
    st.session_state.keyword_num = 0
    st.session_state.disabled = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""
    st.session_state.disabled = False

st.header('Risky Business!')

# form for the company name
st.write("""Please provide the following information to conduct a risk analysis:""")
company = st.text_input('Company:', '') 
st.write('The company that is analysed for risks is: ', company)
st.markdown("""---""")
        
# generate keywords for a company
st.header('1. Generate Keywords')
st.write("""The first step in the pipeline is to generate keywords for the company. This is done by using the
        company name as a seed for an agent implementing the ChatGPT-API amongst a variety of tools. The agent
        generates a list of keywords that are relevant to the company and its operations/products.""")
number_input_keywords = st.number_input('Please forward how many keywords you would like to generate', max_value=50, min_value=1, value=10, step=1, format='%d')
generate_keywords = st.button('Generate keywords!')
if generate_keywords:
    st.session_state.keywords = keyword_generator.generate_keywords(company = company, n = number_input_keywords)
    st.write(st.session_state.keywords)
st.markdown("""---""")

# extract news based on the keywords 
st.header('2. Fetch News')
st.write("""The second step featured in the pipeline is to extract news based on the keywords. This is done 
        by using the Newsapi.ai news API and more specific their very own Python SDK: https://newsapi.ai/intro-python.""")
fetch_news = st.button('Fetch news!')
if fetch_news:
    st.session_state.news = news_extractor.get_news(keywords = st.session_state.keywords, max_articles = 1)
    if len(st.session_state.news) > 1:
        st.write(f"News successfully fetched: {len(st.session_state.news)} articles retrieved.")
        for article in st.session_state.news:
            st.write(article["title"])
    elif len(st.session_state.news) == 1:
        st.write(f"News successfully fetched: {len(st.session_state.news)} article retrieved.")
        st.write(st.session_state.news[0]["title"])
        st.write(st.session_state.news[0]["body"])
    else:
        st.write("No articles retrieved.")
st.markdown("""---""")

# filter news based on relevancy and reliability
st.header('3. Filter News')
st.write("""The third step in the pipeline is to filter the news based on relevancy. This is done by implementing an 
agent to check whether the news is relevant to the company. If so the news are added to the stack of news that are 
to be analyzed.""")
filter_news = st.button('Filter news!')
if filter_news:
    news_cleaned = []
    for article in st.session_state.news:
        article["body"] = text_summarizer.summarize_text(raw_text = article["body"], max_tokens = 3500)
        news_verified: bool = news_checklist.checklist(news = article, company = company)  
        if news_verified == 1:
            st.write(f"News verified: False, for: {article['title']}")
        else:
            st.write(f"News verified: True, for: {article['title']}")
        if news_verified == 0:
            news_cleaned.append(article)
        st.session_state.news = news_cleaned   
st.markdown("""---""")

# embed risk types
st.header('4. Embed Risk Types')
st.write("""The fourth step includes embedding the risk types. This is needed to give the agent counducting
        the risk analysis a better understanding of the risk types the user wants to work with and to keep it from hallucinating
        as well as to create a framework of ideas the actor should work with. This algorithm either creates a new pinecone
        vectorstore or adds content to an already existing one, based on the user's input (if a vectorstore with that
        name/namespace already exists). This step is optional. If there is no new content to be added and already an index
        in place, the user can skip this step.""")
with st.expander("Indexation Form"):
    with st.form(key = "risk_types_embedding_form"):
        index_name: str = st.text_input("Index name", value="index-risk")
        namespace: str = st.text_input("Namespace", value="risk-types")
        metric: str = st.selectbox("Metric", options=["cosine", "dotproduct", "euclidean"])
        pod_type: str = st.selectbox("Pod Type", options=["p1.x1", "p2.x1", "s1.x1"])
        uploaded_files = st.file_uploader("Choose a file", accept_multiple_files = True, type = ["txt", "csv"])
        click_embed = st.form_submit_button("Submit")
    if click_embed:
        concatenated_data = b""
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            concatenated_data += bytes_data
        data: str = concatenated_data.decode("utf-8")
        doc: List[Document] = [Document(page_content = data)]
        index.do_indexation(documents = doc, namespace = namespace, index_name = index_name, metric = metric, pod_type = pod_type)
st.markdown("""---""")

# analyse news
st.header('5. Conduct anaylsis')
st.write("""The fifth stepstep includes conducting a risk anaylsis identifying potential risks discussed in a news article.""")
click3 = st.button('Click me! to conduct a risk analysis')
if click3:
    content = text_summarizer.summarize_text(raw_text = st.session_state.news[0]["body"], max_tokens = 3500)
    analysis_result = risk_analysis.analysis(company = company, news = content)
    st.write(analysis_result)
st.markdown("""---""")

# feedback loop
st.header('6. Feedback Loop')
st.write("""The sixth step includes a feedback loop.""")
with st.form(key="feedback_form"):
    st.session_state.feedback = st.text_area('Feedback:', """""")
    form_submit = st.form_submit_button("Submit")
if form_submit:
    st.success("Thank you for your feedback!")
    feedback = FeedbackLoop()
    # task = "Please identify {n} keywords for the company {company}.".format(n = number_input_keywords, company = company)
    # result1 = feedback.main(task = task, company = company, problem = st.session_state.feedback, message_type = "keyword")
    task = "Please identify the key points of the following news article."
    result2 = feedback.main(task = task, company = company, problem = st.session_state.feedback, message_type = "analysis")
    st.write(result2)
st.markdown("""---""")

# rerun the pipeline
st.header('7. Rerun Pipeline')
st.write("""The seventh step includes rerunning the adapted pipeline.""")
rerun = st.button('Run Loop Again')
if rerun:
    st.session_state.news = []
    st.session_state.keywords = []
    st.session_state.keyword_num = 0
    st.session_state.feedback = ""
    st.session_state.keywords = keyword_generator.generate_keywords(company = company, num = number_input_keywords, message_type = "keyword")
    st.write(st.session_state.keywords)
    st.session_state.news = news_extractor.get_news(keywords = st.session_state.keywords, max_articles = 1)
    if len(st.session_state.news) > 1:
        st.write(f"News successfully fetched: {len(st.session_state.news)} articles retrieved.")
        for article in st.session_state.news:
            st.write(article["title"])
    elif len(st.session_state.news) == 1:
        st.write(f"News successfully fetched: {len(st.session_state.news)} article retrieved.")
        st.write(st.session_state.news[0]["title"])
        st.write(st.session_state.news[0]["body"])
    else:
        st.write("No articles retrieved.")
    news_cleaned = []
    for article in st.session_state.news:
        article["body"] = text_summarizer.summarize_text(raw_text = article["body"], max_tokens = 3500)
        news_verified: bool = news_checklist.checklist(news = article, company = company)  
        st.write(f"News verified: {news_verified}, for: {article['title']}")
        if news_verified == True:
            news_cleaned.append(article)
        st.session_state.news = news_cleaned
    result = RiskAnalysis.analysis(company = company, news = st.session_state.news[0], message_type="analysis")
    st.write(result)
