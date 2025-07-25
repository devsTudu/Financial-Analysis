import streamlit as st

# Sidebar
st.sidebar.markdown("# Here all the investigations are done")

# Main page content
st.markdown("# Analyst page 👨🏻‍🔬")

## Chat

# Initialise Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask me here "):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    # Bot Response

    response = f"You want to know {prompt}"

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({
        "role":"assistant",
        "content":response
    })
    