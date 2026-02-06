import streamlit as st
import openai
from transformers import pipeline
import os

# Set page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        if model_choice == "OpenAI":
            if not openai.api_key:
                st.error("Please set your OpenAI API key in the environment variables.")
            else:
                try:
                    response = openai.ChatCompletion.create(
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
