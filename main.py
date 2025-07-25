import os
from dotenv import load_dotenv

import streamlit as st

load_dotenv()


# Auth
username = st.sidebar.text_input("username", type="default")
password = st.sidebar.text_input("password", type="password")
st.sidebar.divider()

# Define the Pages
main_page = st.Page("pages\\mainPage.py", title="Guest Page", icon="🏠")
analyst_page = st.Page("pages\\analystPage.py", title="Analyst", icon="🕵🏻")
manager_page = st.Page("pages\\managerPage.py", title="Manager", icon="👨🏻‍💼")


log_in = main_page
if username == password:
    if username == "analyst":
        log_in = analyst_page
    elif username == "manager":
        log_in = manager_page


pg = st.navigation([log_in])
pg.run()


# LLM
st.sidebar.divider()
st.sidebar.text("Please provide anyone API Key Here")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password")

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
if gemini_api_key:
    os.environ["GOOGLE_API_KEY"] = gemini_api_key
