import streamlit as st
from groq import Groq
import os

# Set page config
st.set_page_config(
    page_title="Nightbot Groq AI",
    page_icon="🤖",
    layout="wide"
)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title and description
st.title("🤖 Nightbot Groq AI")
st.markdown("Chat with Groq AI powered chatbot")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.selectbox(
        "Select Model",
        ["mixtral-8x7b-32768", "llama-3.1-70b-versatile", "llama-3.1-8b-instant"]
    )
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7)
    max_tokens = st.slider("Max Tokens", 100, 4000, 1024)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Groq
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                assistant_message = response.choices[0].message.content
                st.markdown(assistant_message)
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Powered by Groq AI | Running on Streamlit Cloud")
