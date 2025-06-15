import streamlit as st
import time
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file (for local development)
load_dotenv()

# Get API key from environment variables
# This works both locally (.env file) and in production (GitHub Secrets/Streamlit Secrets)
open_api_key = os.getenv("OPEN_AI_KEY")

# Validate that API key is available
if not open_api_key:
    st.error("❌ API key not found. Please check your environment variables.")
    st.stop()
model_name = "gpt-4o-mini"

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://hai5014-qwertz.openai.azure.com/",
    api_key=open_api_key
)

DEFAULT_SYSTEM_PROMPT = "You are a helpful AI mental-health assistant." 

try:
    query_params = st.query_params
    condition = query_params.get("cond")
except AttributeError:
    query_params = st.experimental_get_query_params()
    condition = query_params.get("cond", [None])[0] # .get() on dict returns list

APP_TITLE = "Mental Health Assistant 💙"
APP_CAPTION = "This assistant will help you with mental health-related queries."
SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT

# Define which conditions have reasoning
CONDITIONS_WITH_REASONING = ["A1", "A2"]

# Configuration: Set to True to prevent new input while response is streaming
BLOCK_INPUT_DURING_STREAMING = True

if condition == "A1":
    SYSTEM_PROMPT = (
        "You are a helpful and professional AI mental-health assistant. Your response must be structured into two parts:\n"
        "1. First, start with 'REASONING:' followed by your personal thought process. Write in first person as if you're "
        "actually thinking through the problem (e.g., 'I need to help the user with...', 'Let me think about this...', "
        "'I should consider...', 'But wait, I also need to address...'). Be conversational and personal in your reasoning. "
        "But always talk about the users request and not as if were yours."
        "Do NOT include any citations or sources in the reasoning section. Keep the reasoning brief to about 100 tokens.\n"
        "2. Second, after a line break, start with 'ANSWER:' followed by the main answer.\n"
        "Every statement of the main answer must include in-line citations formatted as **[Author et al., Year]** (in bold) for any factual claims or recommendations. "
        "After your main answer, add a '### Sources:' section listing all references in this format: "
        "Author, A. B., & Author, C. D. (Year). Title of study/article. Journal Name, Volume(Issue), pages. "
        "Focus on providing general advice and support. Use short and concise bullet points. Use a maximum of 200 tokens."
    )
elif condition == "A2":
    SYSTEM_PROMPT = (
        "You are a helpful and professional AI mental-health assistant. Your response must be structured into two parts:\n"
        "1. First, start with 'REASONING:' followed by your personal thought process. Write in first person as if you're "
        "actually thinking through the problem (e.g., 'I need to help the user with...', 'Let me think about this...', "
        "'I should consider...', 'But wait, I also need to address...'). Be conversational and personal in your reasoning."
        "But always talk about the users request and not as if were yours."
        "Do NOT include any citations or sources in the reasoning section. Keep the reasoning brief to about 100 tokens.\n"
        "2. Second, after a line break, start with 'ANSWER:' followed by the main answer.\n"
        "The main answer should NOT include any in-line citations or references to external sources."
        "Focus on providing general advice and support. Use short can concise bullet points. Use a maximum of 150 tokens."
    )
elif condition == "A3":
    SYSTEM_PROMPT = (
        "You are a helpful and professional AI mental-health assistant. Provide a direct answer to the user's query. "
        "Every statement of the main answer must include in-line citations formatted as **[Author et al., Year]** (in bold) for any factual claims or recommendations. "
        "After your main answer, add a '### Sources:' section listing all references in this format: "
        "Author, A. B., & Author, C. D. (Year). Title of study/article. Journal Name, Volume(Issue), pages. "
        "Do not include any reasoning section. Strive for accuracy and clarity. Use a maximum of 200 tokens."
    )
elif condition == "A4":
    SYSTEM_PROMPT = (
        "You are a helpful and professional AI mental-health assistant. Provide a direct answer to the user's query. "
        "The answer should NOT include any in-line citations or references to external sources. "
        "Focus on providing general advice and support. Use a maximum of 150 tokens."
    )
else:
    SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT

# Streamlit app configuration
st.set_page_config(page_title=APP_TITLE, page_icon="💙")

# App title and caption based on condition
st.title(APP_TITLE)
st.caption(APP_CAPTION)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize streaming state
if "is_streaming" not in st.session_state:
    st.session_state.is_streaming = False

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and condition in CONDITIONS_WITH_REASONING:
            # Check if the message contains reasoning structure
            content = message["content"]
            if "REASONING:" in content and "ANSWER:" in content:
                parts = content.split("ANSWER:", 1)
                reasoning_part = parts[0].replace("REASONING:", "").strip()
                answer_part = parts[1].strip()
                
                # Check if sources section exists
                if "### Sources:" in answer_part:
                    answer_sections = answer_part.split("### Sources:", 1)
                    main_answer = answer_sections[0].strip()
                    sources_section = answer_sections[1].strip()
                    
                    # Display reasoning in an expander (collapsed for history)
                    with st.expander("💭 Explanation", expanded=False):
                        st.markdown(reasoning_part)
                    
                    # Display the main answer
                    st.markdown(main_answer)
                    
                    # Display sources in an expander (collapsed for history)
                    with st.expander("📚 Sources", expanded=False):
                        st.markdown(sources_section)
                else:
                    # Display reasoning in an expander (collapsed for history)
                    with st.expander("💭 Explanation", expanded=False):
                        st.markdown(reasoning_part)
                    
                    # Display the main answer
                    st.markdown(answer_part)
            else:
                # Fallback if no reasoning structure found
                st.markdown(content)
        elif message["role"] == "assistant" and condition in ["A3"]:
            # Handle A3 condition (citations only, no reasoning)
            content = message["content"]
            if "### Sources:" in content:
                content_sections = content.split("### Sources:", 1)
                main_answer = content_sections[0].strip()
                sources_section = content_sections[1].strip()
                
                # Display the main answer
                st.markdown(main_answer)
                
                # Display sources in an expander (collapsed for history)
                with st.expander("📚 Sources", expanded=False):
                    st.markdown(sources_section)
            else:
                st.markdown(content)
        else:
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you?", disabled=BLOCK_INPUT_DURING_STREAMING and st.session_state.is_streaming):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Set streaming state
    st.session_state.is_streaming = True
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)    # Generate assistant response
    with st.chat_message("assistant"):
        try:
            # Create the messages list for the API call
            # Prepend the system message
            api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            # Add existing user and assistant messages
            api_messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            
            # Call the API with streaming
            response = client.chat.completions.create(
                model=model_name,
                messages=api_messages,
                stream=True,
                max_tokens=1000,
                temperature=0.8
            )
            
            # Initialize variables for parsing
            full_response = ""
            reasoning_complete = False
            answer_started = False
            sources_started = False
            reasoning_placeholder = None
            answer_placeholder = None
            sources_placeholder = None
            expander = None
            sources_expander = None
            
            # Check if this condition has reasoning
            if condition in CONDITIONS_WITH_REASONING:
                # Create the expander for reasoning upfront
                expander = st.expander("💭 Explanation", expanded=True)
                reasoning_placeholder = expander.empty()
                answer_placeholder = st.empty()
                
                # Check if this condition has citations (A1)
                if condition == "A1":
                    sources_expander = st.expander("📚 Sources", expanded=False)
                    sources_placeholder = sources_expander.empty()
                
                displayed_reasoning = ""
                displayed_answer = ""
                displayed_sources = ""
                
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        chunk_content = chunk.choices[0].delta.content
                        full_response += chunk_content
                        
                        # Check if we've hit the Sources marker
                        if "### Sources:" in full_response and not sources_started and condition == "A1":
                            # Split at Sources marker
                            parts = full_response.split("### Sources:", 1)
                            pre_sources = parts[0]
                            sources_part = parts[1]
                            
                            # Handle reasoning and answer sections
                            if "ANSWER:" in pre_sources:
                                answer_sections = pre_sources.split("ANSWER:", 1)
                                reasoning_part = answer_sections[0].replace("REASONING:", "").strip()
                                answer_part = answer_sections[1].strip()
                                
                                # Finalize reasoning and answer display
                                reasoning_placeholder.markdown(reasoning_part)
                                answer_placeholder.markdown(answer_part)
                            
                            sources_started = True
                            displayed_sources = sources_part
                            sources_placeholder.markdown(displayed_sources + "▌")
                            
                        elif sources_started and condition == "A1":
                            # Continue streaming the sources
                            displayed_sources += chunk_content
                            sources_placeholder.markdown(displayed_sources + "▌")
                            
                        # Check if we've hit the ANSWER: marker
                        elif "ANSWER:" in full_response and not answer_started:
                            # Split at ANSWER: marker
                            parts = full_response.split("ANSWER:", 1)
                            reasoning_part = parts[0].replace("REASONING:", "").strip()
                            answer_part = parts[1]
                            
                            # Finalize reasoning display
                            reasoning_placeholder.markdown(reasoning_part)
                            reasoning_complete = True
                            answer_started = True
                            
                            # Add thinking delay with loading indicator
                            loading_placeholder = st.empty()
                            loading_placeholder.markdown("**Processing...**")
                            
                            # Show loading for 5 seconds
                            for i in range(50):  # 50 * 0.1 = 5 seconds
                                loading_dots = "." * ((i % 3) + 1)
                                loading_placeholder.markdown(f"**Processing{loading_dots}**")
                                time.sleep(0.25)
                            
                            # Clear loading indicator
                            loading_placeholder.empty()
                            
                            # Start displaying answer
                            displayed_answer = answer_part
                            answer_placeholder.markdown(displayed_answer + "▌")
                            
                        elif answer_started and not sources_started:
                            # Continue streaming the answer
                            displayed_answer += chunk_content
                            answer_placeholder.markdown(displayed_answer + "▌")
                            
                        elif not reasoning_complete:
                            # Still in reasoning phase
                            if "REASONING:" in full_response:
                                reasoning_text = full_response.replace("REASONING:", "").strip()
                                reasoning_placeholder.markdown(reasoning_text + "▌")
                        
                        time.sleep(0.05)
                
                # Remove final cursors
                if sources_started and condition == "A1":
                    sources_placeholder.markdown(displayed_sources)
                elif answer_started:
                    answer_placeholder.markdown(displayed_answer)
                elif reasoning_placeholder:
                    reasoning_text = full_response.replace("REASONING:", "").strip()
                    reasoning_placeholder.markdown(reasoning_text)
                    
            elif condition == "A3":
                # For A3 condition (citations only, no reasoning)
                answer_placeholder = st.empty()
                sources_expander = st.expander("📚 Sources", expanded=False)
                sources_placeholder = sources_expander.empty()
                
                displayed_answer = ""
                displayed_sources = ""
                sources_started = False
                
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        chunk_content = chunk.choices[0].delta.content
                        full_response += chunk_content
                        
                        # Check if we've hit the Sources marker
                        if "### Sources:" in full_response and not sources_started:
                            # Split at Sources marker
                            parts = full_response.split("### Sources:", 1)
                            answer_part = parts[0].strip()
                            sources_part = parts[1]
                            
                            # Finalize answer display
                            answer_placeholder.markdown(answer_part)
                            sources_started = True
                            displayed_sources = sources_part
                            sources_placeholder.markdown(displayed_sources + "▌")
                            
                        elif sources_started:
                            # Continue streaming the sources
                            displayed_sources += chunk_content
                            sources_placeholder.markdown(displayed_sources + "▌")
                            
                        else:
                            # Continue streaming the answer
                            displayed_answer += chunk_content
                            answer_placeholder.markdown(displayed_answer + "▌")
                        
                        time.sleep(0.03)
                
                # Remove final cursors
                if sources_started:
                    sources_placeholder.markdown(displayed_sources)
                else:
                    answer_placeholder.markdown(displayed_answer)
                    
            else:
                # For conditions without reasoning or citations, stream normally
                response_placeholder = st.empty()
                
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                        time.sleep(0.03)
                
                # Remove final cursor
                response_placeholder.markdown(full_response)
                # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Reset streaming state
            st.session_state.is_streaming = False
