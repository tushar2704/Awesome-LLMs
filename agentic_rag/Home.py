import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai_tools import PDFSearchTool, tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
import requests

st.set_page_config(page_title="Agentic RAG System", layout="wide")

st.title("Agentic RAG Using CrewAI & LangChain")
st.markdown("#### Built by Tushar Aggarwal")

# API Key Input Section
with st.sidebar:
    st.header("API Configuration")
    groq_api = st.text_input("Enter your Groq API Key", type="password")
    tavily_api = st.text_input("Enter your Tavily API Key", type="password")
    
    if groq_api and tavily_api:
        os.environ['GROQ_API_KEY'] = groq_api
        os.environ['TAVILY_API_KEY'] = tavily_api
        st.success("API Keys set successfully!")

def initialize_llm():
    return ChatOpenAI(
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=os.environ.get('GROQ_API_KEY'),
        model_name="llama3-8b-8192",
        temperature=0.1,
        max_tokens=1000
    )

def setup_pdf():
    pdf_url = 'https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf'
    response = requests.get(pdf_url)
    with open('attention_is_all_you_need.pdf', 'wb') as file:
        file.write(response.content)
    return PDFSearchTool(
        pdf='attention_is_all_you_need.pdf',
        config=dict(
            llm=dict(
                provider="groq",
                config=dict(
                    model="llama3-8b-8192",
                ),
            ),
            embedder=dict(
                provider="huggingface",
                config=dict(
                    model="BAAI/bge-small-en-v1.5",
                ),
            ),
        )
    )

@tool
def router_tool(question):
    """Router Function"""
    if 'self-attention' in question:
        return 'vectorstore'
    else:
        return 'web_search'

def create_agents(llm):
    Router_Agent = Agent(
        role='Router',
        goal='Route user question to a vectorstore or web search',
        backstory="You are an expert at routing a user question to a vectorstore or web search.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    Retriever_Agent = Agent(
        role="Retriever",
        goal="Use the information retrieved from the vectorstore to answer the question",
        backstory="You are an assistant for question-answering tasks.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    Grader_agent = Agent(
        role='Answer Grader',
        goal='Filter out erroneous retrievals',
        backstory="You are a grader assessing relevance of a retrieved document to a user question.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    hallucination_grader = Agent(
        role="Hallucination Grader",
        goal="Filter out hallucination",
        backstory="You are a hallucination grader assessing whether an answer is grounded in facts.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    answer_grader = Agent(
        role="Answer Grader",
        goal="Filter out hallucination from the answer.",
        backstory="You are a grader assessing whether an answer is useful to resolve a question.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return Router_Agent, Retriever_Agent, Grader_agent, hallucination_grader, answer_grader

def create_tasks(Router_Agent, Retriever_Agent, Grader_agent, hallucination_grader, answer_grader):
    router_task = Task(
        description="Analyse the keywords in the question {question}",
        expected_output="Give a binary choice 'websearch' or 'vectorstore' based on the question",
        agent=Router_Agent,
        tools=[router_tool]
    )
    
    retriever_task = Task(
        description="Based on the response from the router task extract information for the question {question}",
        expected_output="Return a clear and concise text as response",
        agent=Retriever_Agent,
        context=[router_task]
    )
    
    grader_task = Task(
        description="Based on the response from the retriever task for the question {question}",
        expected_output="Binary score 'yes' or 'no'",
        agent=Grader_agent,
        context=[retriever_task]
    )
    
    hallucination_task = Task(
        description="Based on the response from the grader task for the question {question}",
        expected_output="Binary score 'yes' or 'no'",
        agent=hallucination_grader,
        context=[grader_task]
    )
    
    answer_task = Task(
        description="Based on the response from the hallucination task for the question {question}",
        expected_output="Return a clear and concise response",
        context=[hallucination_task],
        agent=answer_grader
    )
    
    return router_task, retriever_task, grader_task, hallucination_task, answer_task

def main():
    if not (os.environ.get('GROQ_API_KEY') and os.environ.get('TAVILY_API_KEY')):
        st.warning("Please enter your API keys in the sidebar to continue.")
        return
    
    st.header("Ask your question")
    user_question = st.text_input("Enter your question:")
    
    if st.button("Get Answer"):
        if user_question:
            with st.spinner("Processing your question..."):
                try:
                    llm = initialize_llm()
                    rag_tool = setup_pdf()
                    web_search_tool = TavilySearchResults(k=3)
                    
                    agents = create_agents(llm)
                    tasks = create_tasks(*agents)
                    
                    rag_crew = Crew(
                        agents=list(agents),
                        tasks=list(tasks),
                        verbose=True
                    )
                    
                    result = rag_crew.kickoff(inputs={"question": user_question})
                    
                    st.success("Answer generated successfully!")
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
