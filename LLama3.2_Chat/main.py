##© 2024 Tushar Aggarwal. All rights reserved.(https://tushar-aggarwal.com)
import streamlit as st
from groq import Groq
import streamlit as st
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import os
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
# Initialize Groq clientload_dotenv()
load_dotenv()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Llama 3.2 Chat Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response from Llama 3.2
    response = client.chat.completions.create(
        model="llama-3.2-90b-text-preview",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        temperature=0.7,
        max_tokens=1000,
    )

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message.content)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})