import streamlit as st
from back import ask_the_graph

st.set_page_config(page_title="Neo4j AI Agent", layout="wide")
st.title("🧠 Neo4j Graph AI Assistant")

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Ask your graph question...")

if user_input:
    # show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # run your chain
        result = ask_the_graph(user_input)

        # extract output safely
        answer = result.get("result") if isinstance(result, dict) else str(result)

        # show assistant response
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.error(error_msg)
    