import streamlit as st
from openai import OpenAI

MAX_QUERIES=2

def main():
    st.set_page_config(
        page_title="Chatbot",
        page_icon=":smiley:",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.title("Chatbot")

    model_configs = {
        "OpenAI GPT-4.1 Nano": {
            "api_key": st.secrets['OPENAI_API_KEY'],
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4.1-nano"
        },
        "Grok-3 Mini": {
            "api_key": st.secrets['GROK_API_KEY'],
            "base_url": "https://api.x.ai/v1",
            "model": "grok-3-mini"  # Adjust to actual model name if different
        }
    }

    with st.sidebar:
        selected_model = st.selectbox(
            'Select a model',
            model_configs.keys(),
            )
        st.sidebar.markdown(f"**Queries used:** {st.session_state.query_count} / {MAX_QUERIES}")

    config = model_configs[selected_model]
    client = OpenAI(

            api_key=config['api_key'],
            base_url=config['base_url'])

    if 'query_count' not in st.session_state:
        st.session_state.query_count = 0
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'model' not in st.session_state:
        st.session_state.model = selected_model

    if 'active_model' not in st.session_state:
        st.session_state.active_model = selected_model
    
    if st.session_state.active_model != selected_model:
        st.session_state.active_model = selected_model
    
    if st.session_state.query_count >= MAX_QUERIES:
        st.warning("You’ve reached the maximum number of queries for this session.")
        st.stop()

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    
    if prompt := st.chat_input("What's up?"):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
            stream = client.chat.completions.create(
                model=config['model'],
                messages=[
                    {'role': m['role'], 'content': m['content']}
                    for m in st.session_state.messages
                ],
                stream=True
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({'role': 'assistant', 'content': response})

if __name__ == "__main__":
    main()
    