import streamlit as st
from openai import OpenAI
from transformers import pipeline
import os
from dotenv import load_dotenv
import sys

# Load environment variables with encoding fallback
try:
    load_dotenv()  # Default UTF-8
except UnicodeDecodeError:
    try:
        load_dotenv(encoding='utf-16')  # Fallback to UTF-16
    except UnicodeDecodeError:
        print("Error: Unable to load .env file due to encoding issues. Please ensure the file is saved as UTF-8 without BOM.")
        sys.exit(1)

# Set page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key) if openai_api_key else None

# Sidebar for API key input if not set
if not client:
    st.sidebar.header("API Key Setup")
    api_key_input = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    if api_key_input:
        client = OpenAI(api_key=api_key_input)
        st.sidebar.success("API Key set successfully!")
    else:
        st.sidebar.warning("Please enter your OpenAI API Key to use the chatbot.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for model selection
st.sidebar.title("Settings")
model_choice = st.sidebar.selectbox("Choose AI Model", ["OpenAI", "Hugging Face"])
translate_response = st.sidebar.checkbox("Translate Response to French")

# Main title
st.title("🤖 AI Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response based on selected model
    with st.chat_message("assistant"):
        assistant_response = ""
        if model_choice == "OpenAI":
            if not client:
                st.error("Please set your OpenAI API key in the environment variables or sidebar.")
            else:
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=st.session_state.messages
                    )
                    assistant_response = response.choices[0].message.content
                except Exception as e:
                    assistant_response = f"Error: {str(e)}"
        elif model_choice == "Hugging Face":
            try:
                # Load conversational pipeline (cached for performance)
                if "hf_pipeline" not in st.session_state:
                    st.session_state.hf_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")
                conversation = st.session_state.hf_pipeline(st.session_state.messages[-1]["content"])
                assistant_response = conversation.generated_responses[-1]
            except Exception as e:
                assistant_response = f"Error: {str(e)}"

        # Display and add to history
        st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
