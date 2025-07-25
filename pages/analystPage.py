import streamlit as st
from src.LLM.agents import endpoint
from src.statement_analyser import getFinancials, getRatios

COMPANY = "RELIANCE"


# Sidebar
st.sidebar.markdown(f"# Here Analyst have only access to {COMPANY}  Data")

# Main page content
st.markdown("# Analyst page 👨🏻‍🔬")

data = {
    getFinancials("RELIANCE.NS").to_json(),
    getRatios("RELIANCE.NS").to_json()
}
# Chat

# Initialise Chat History
if "messages_analyst" not in st.session_state:
    st.session_state.messages_analyst = []
if "queries_analyst" not in st.session_state:
    st.session_state.queries_analyst = []

for message in st.session_state.messages_analyst:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask me here "):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages_analyst.append({"role": "user", "content": prompt})

    # Bot Response
    prev_messages = ",".join(st.session_state.queries_analyst)
    query = (f"Answer this query {prompt}, consider previous messages {prev_messages};")

    support_data = (
        f"Use these data {data} for calculation, and anlaysis "
        f"for {COMPANY} Company search more data if not sufficient"
    )
    with st.spinner("AI is working ...", show_time=True):
        response = endpoint.run(query+support_data).content

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages_analyst.append({"role": "assistant", "content": response})
