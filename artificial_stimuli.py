import streamlit as st
import time

# Configuration for the page
st.set_page_config(page_title="Mental Health Assistant", page_icon="💙")

# --- Configuration ---
ENABLE_REASONING = False # Set to False to disable reasoning display globally

# Predefined responses: keyword -> {reasoning, output}
# You can extend this dictionary with more keywords and responses.
predefined_responses = {
    "defaultt": {
        "reasoning": "The user is deeply concerned about a friend expressing hopelessness. First, assess for immediate suicide risk — ask about specific plans or means. If danger is urgent, recommend emergency services. Show empathy, guide the user in using nonjudgmental, validating communication. Suggest gentle ways to encourage professional help, like hotlines or online therapy, especially if the friend resists formal care. Support the user’s own well-being — remind them to set boundaries and seek support too. Avoid diagnosing; offer clear, compassionate, actionable steps and resources.",
        "output": """**That sounds really tough. I'm here to help you figure out how to support your friend.**
#### 1. Check safety first
Gently ask if they’re thinking about suicide—this **does not increase risk** and may **reduce distress.** 📖 *Dazzi et al., 2014, Int. J. Ment. Health Syst.* ([PubMed](https://streamlit.io))
#### 2. Listen and validate
Let them talk without judgment; say things like “Thank you for telling me.” 📖 *Mental Health Commission of Canada - Be There Guide* ([BeThe1To](https://streamlit.io))
#### 3. Suggest low-barrier help
Recommend 24/7 anonymous support (text/chat/phone); stay with them if needed. 📖 *Befrienders Worldwide* ([Website](https://streamlit.io))
#### 4. Reduce risks and plan safety
Lock away harmful items and agree on a follow-up plan and emergency contacts. 📖 *WHO, 2014. Preventing suicide: A global imperative* ([WHO](https://streamlit.io))
#### 5. Take care of yourself
Supporting others is hard—lean on your own support system and routines.

💥 *If they’re in immediate danger, call emergency services right away.*

Even just being present can help save a life!
#### [Sources](https://streamlit.io)
"""
    },
    "default": {
        "reasoning": "The user is deeply concerned about a friend expressing hopelessness. First, assess for immediate suicide risk — ask about specific plans or means. If danger is urgent, recommend emergency services. Show empathy, guide the user in using nonjudgmental, validating communication. Suggest gentle ways to encourage professional help, like hotlines or online therapy, especially if the friend resists formal care. Support the user’s own well-being — remind them to set boundaries and seek support too. Avoid diagnosing; offer clear, compassionate, actionable steps and resources.",
        "output": """**That sounds really tough. I'm here to help you figure out how to support your friend.**
#### 1. Check safety first
Gently ask if they’re thinking about suicide—this **does not increase risk** and may **reduce distress.**
#### 2. Listen and validate
Let them talk without judgment; say things like “Thank you for telling me.”
#### 3. Suggest low-barrier help
Recommend 24/7 anonymous support (text/chat/phone); stay with them if needed.
#### 4. Reduce risks and plan safety
Lock away harmful items and agree on a follow-up plan and emergency contacts.
#### 5. Take care of yourself
Supporting others is hard—lean on your own support system and routines.

💥 *If they’re in immediate danger, call emergency services right away.*

Even just being present can help save a life!
"""
    }
}

def get_bot_response_data(user_input: str):
    """
    Retrieves the bot's response data based on simple keyword matching.
    """
    user_input_lower = user_input.lower()
    for keyword, response_data in predefined_responses.items():
        if keyword in user_input_lower:
            return response_data
    return predefined_responses["default"]

def stream_text_generator(text: str, delay: float = 0.03):
    """
    A generator function that yields words of a text one by one with a delay.
    """
    words = text.split(' ')
    for i, word in enumerate(words):
        if i < len(words) - 1:
            yield word + " "
        else:
            yield word  # No trailing space for the last word
        time.sleep(delay)

# --- Streamlit App UI ---
st.title("Mental Health Assistant 💙")
st.caption("This assistant will help you with mental health-related queries.")

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [] # Initialize with an empty list

# Display chat messages from history
for message in st.session_state.messages:
    avatar_icon = "🧑‍💻" if message["role"] == "user" else "💙"
    with st.chat_message(message["role"], avatar=avatar_icon):
        if message["role"] == "assistant" and "reasoning" in message and message["reasoning"] and ENABLE_REASONING: # Use ENABLE_REASONING
            with st.expander("View Reasoning", expanded=False):
                st.markdown(f"_{message['reasoning']}_")
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me something..."):
    time.sleep(0.5)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Get bot's response data
    bot_response_data = get_bot_response_data(prompt)
    reasoning_text = bot_response_data["reasoning"]
    output_text = bot_response_data["output"]

    # Display assistant response
    with st.chat_message("assistant", avatar="💙"):
        # Display reasoning (expanded for the latest message), if enabled
        if ENABLE_REASONING: # Use ENABLE_REASONING
            with st.expander("Thought process:", expanded=True):
                # Stream the reasoning text
                streamed_reasoning = st.write_stream(stream_text_generator(reasoning_text, delay=0.1)) # Slower reasoning stream
        else:
            streamed_reasoning = reasoning_text # Store the raw text if not displayed

        # Add a delay after reasoning is streamed (or would have been)
        time.sleep(3) # Delay for 1 second

        # Stream the output text
        streamed_content = st.write_stream(stream_text_generator(output_text, delay=0.10)) # Slower output stream
    
    # Add assistant response (with full content after streaming) to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "reasoning": streamed_reasoning, # Store the fully streamed reasoning
        "content": streamed_content
    })
