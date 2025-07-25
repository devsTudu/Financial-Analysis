import streamlit as st
from src.statement_analyser import getFinancials
from src.LLM.agents import endpoint

# Main page content
st.markdown("# Managers' page 🎈")
st.sidebar.markdown("Logged In as a Manager🎈")

options = [
    "RELIANCE.NS",
    "JIOFIN",
    "NETWORK18",
    "RPOWER",
    "RIIL",
    "HATHWAY",
    "DEN",
    "JUSTDIAL",
]

selection = st.pills("Company", options, selection_mode="multi")


data = {}

with st.status(f"Records {len(selection)}"):
    for val in selection:
        st.write(f"Load {val} data")
        data[val] = getFinancials(val).to_json()

# Chat

# Initialise Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
if "queries" not in st.session_state:
    st.session_state.queries = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask me here "):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.queries.append(prompt)
    # Bot Response
    prev_messages = ",".join(st.session_state.queries)
    query = (f"Answer this query {prompt}, consider previous messages {prev_messages};")

    support_data = (
        f"Use these data {data} for calculation"
        "and analysis, search more data if not sufficient"
    )

    with st.spinner("AI is working ...", show_time=True):
        response = endpoint.run(query + support_data).content

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
