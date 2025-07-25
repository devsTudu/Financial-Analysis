import streamlit as st
import os

# Define the Pages
main_page = st.Page("pages\\mainPage.py",
                        title="Main Page",
                        icon="🏠")
analyst_page = st.Page("pages\\analystPage.py",
                        title="As Analyst",
                        icon="🕵🏻")
manager_page = st.Page("pages\\managerPage.py",
                        title="As Manager", 
                        icon="👨🏻‍💼")

pg = st.navigation([main_page, analyst_page, manager_page])
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
