# AI Chatbot

This is an AI chatbot built using Python and Streamlit. It features user text input, a clear chat button, chat history, and integrates with both OpenAI API and Hugging Face models.

## Features

- User text input for sending messages
- Clear chat button to reset chat history
- Persistent chat history during the session
- Model selection between OpenAI and Hugging Face
- Responses generated using selected AI model

## Setup

1. Clone the repository or download the files.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   - Create a `.env` file in the project directory and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   - Or set it as an environment variable.

## Running the App

Run the Streamlit app:
```
streamlit run app.py
```

The app will open in your default web browser.

## Usage

1. Select the AI model (OpenAI or Hugging Face) from the sidebar.
2. Enter your message in the text input field.
3. Click "Send" to get a response from the chatbot.
4. View the chat history in the "Chat History" section.
5. Click "Clear Chat" to reset the conversation.

## Dependencies

- streamlit
- openai
- transformers
- torch

## Note

Make sure you have a valid OpenAI API key for the OpenAI model option. The Hugging Face model runs locally and doesn't require an API key.
