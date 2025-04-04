import streamlit as st
import requests
import dotenv
import os

dotenv.load_dotenv()

#API URL
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

#API key
API_KEY = os.getenv("HF_API_KEY")

#API Headers
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Function to query the chatbot
def query_chatbot(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        try:
            return response.json()[0]['generated_text']
        except (KeyError, IndexError):
            return "Error: Unexpected response format."
    else:
        return f"Error: {response.status_code} - {response.text}"

#streamlit UI
st.title("Streamlit Chatbot")
st.markdown("Ask anything here!")

#initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

#chat input box
user_input = st.chat_input("Type your message here...")

if user_input:
    #display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from AI API
    response = query_chatbot(user_input)

    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
