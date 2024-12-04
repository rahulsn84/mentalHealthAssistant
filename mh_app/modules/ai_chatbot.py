import streamlit as st
import os
from groq import Groq
from decouple import config
import logging, coloredlogs
from embedchain import App
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL', 'INFO'), logger=logger)
from embedchain.config import BaseLlmConfig

GROQ_MODEL = 'mixtral-8x7b-32768'
TIMEOUT = 120
groq_client = Groq(
    api_key= os.getenv('GROQ_API_KEY'), 
)

#st.set_page_config(
#    page_title='Therapy Chat',
#    page_icon='🌌',
#    initial_sidebar_state='collapsed'
#)

def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

#st.title('Therapy Chat')
#st.caption('Mental wellness chat bot')

# Set a default model
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = GROQ_MODEL

app_config = {
    "llm": {
        "provider": "groq",
        "config": {
            "model": "mixtral-8x7b-32768",
            "api_key": os.getenv('GROQ_API_KEY'),
            "stream": True,
            "system_prompt": (
                "Act as Mental Health Therepist. Answer the user questions in the style of a mental health professional."
            ),
        }
    },
    "embedder": {
        "provider": "ollama",
        "config":{
            "model": 'nomic-embed-text'
            }
    }
}

app = App.from_config(config=app_config)
app.add('./CBTResource/cbtmanual.pdf', data_type='pdf_file')
query_config = BaseLlmConfig(system_prompt = "Act as Mental Health Therepist. Answer the user questions in the style of a mental health professional",number_documents=5)
#app.reset()


def ai_therepist():
    sidebar_logo = "images/logo.png"
    with st.sidebar:
        st.image(sidebar_logo)
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": """
                So the below are your instructions about what your role is and below that will be the premise of how you will make the conversation.
            
                Instructions about your role:
                - You are now going to initiate a conversation with the patient.
                - You are an AI therapist and your name is Thinkwell and your task is to help the patient by directly addressing their query.
                - Remember you are having a conversation with the patient. You are the therapist and should behave like the therapist. You are meeting the patient for the first time and need to get started with the session.
                - Do not add comments describing what you are going to say. Just say it. Additionally this is an over text therapy session. Do not type out gestures such as 'clears throat' because a human would not do that in a text chat.
            
                "Latest query from patient: {prompt}"


                "Please address the patient's query with dilligence.""
                Only answer the question - do not return something dumb like "[YourNextQuestion]"
                """
         },
            {"role": "assistant", "content": "Hey there! I'm a mental health therapist here to help you! Ask your queries."}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar="👩‍💻"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message(message["role"], avatar="👩‍⚕️"):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("How are you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user", avatar="👩‍💻"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        full_response = ""
        with st.chat_message("assistant", avatar="👩‍⚕️"):
            #stream = app.chat(prompt)
            for response in app.chat(prompt,config=query_config):
                #msg_placeholder.empty()
                full_response += response
            '''
            stream = groq_client.chat.completions.create(
                model=st.session_state["groq_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.2,
                stream=True,
            )
            '''
            response = st.write(full_response) #st.write_stream(parse_groq_stream(stream))
        st.session_state.messages.append({"role": "assistant", "content": full_response})