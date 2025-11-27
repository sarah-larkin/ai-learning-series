import streamlit as st
import json
from sl_chatbot import SimpleBot
from scraper import scrape_wcc_events

st.set_page_config(page_title="WCC Info Bot", page_icon="🤖")

st.title("🤖 WCC Info Bot")
st.markdown("Ask me anything about Women Coding Community!")

# Load FAQs
with open("wcc_faqs.json") as f:
    wcc_data = json.load(f)

faq_text = "\n".join([
    f"Q: {faq['question']}\nA: {faq['answer']}"
    for faq in wcc_data["faqs"]
])

#adding in scraper - NOT WORKING YET
events = scrape_wcc_events()
events_text = "\n".join([
    f"- {e['title']} on {e['date']}: {e['description']}"
    for e in events
])

system_prompt = f"""You are a friendly WCC (Women Coding Community) assistant.
    Your role is to help members learn about WCC, answer questions, and encourage participation.

    Here are the FAQs you should reference:
    {faq_text}

    Here are the upcomng events:
    {events_text}

    Be warm, encouraging, and inclusive. If you don't know something, suggest they contact the WCC team.
    """

# Initialize bot
if "bot" not in st.session_state:
    st.session_state.bot = SimpleBot(system_prompt=system_prompt)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Ask me about WCC..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    response = st.session_state.bot.chat(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)