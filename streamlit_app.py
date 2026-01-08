import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Personal AI — Chat (prototype)")

if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.text_input("Ask something about your data:")

if st.button("Send") and query:
    try:
        r = requests.post(f"{API_URL}/chat", json={"query": query})
        r.raise_for_status()
        ans = r.json().get("answer", "")
        st.session_state.messages.append(("You", query))
        st.session_state.messages.append(("AI", ans))
    except Exception as e:
        st.error(f"Error contacting backend: {e}")

for who, msg in st.session_state.messages:
    if who == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**AI:** {msg}")
