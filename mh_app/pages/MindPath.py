import streamlit as st
from modules import questions
from modules import visualizations
from modules import ai_chatbot
from modules import guidance
from modules import admin
from modules import db
from time import sleep

#st.set_page_config(layout="wide")

def main_page():
    import streamlit as st

    st.write("# Welcome to MindPath! 👋")
    #st.sidebar.success("Select an option.")
    sidebar_logo = "images/logo.png"
    #st.logo(sidebar_logo, icon_image=sidebar_logo)
    with st.sidebar:
        st.image(sidebar_logo)

    st.markdown(
        """
        Welcome to MindPath – your personal companion for mental well-being. MindPath is a comprehensive mental health tracker and support tool, designed to help you better understand and manage your thoughts, emotions, and daily experiences using scientifically-backed Cognitive Behavioral Therapy (CBT) techniques.

With MindPath, you can track your moods, uncover patterns in your mental health journey, and practice proven CBT exercises to shift negative thought patterns and build resilience. Whether you're managing stress, working through anxiety, or simply aiming to boost your overall mental wellness, MindPath is here to guide you every step of the way. Start your journey towards a clearer, calmer mind today!
    """
    )
    st.markdown(
        """
        ## Features:
        - Current Mental health tracking with QnA.
        - Visualization of the mental health data over time.
        - Personalized Guidance based on current mental health.
        - Chat with AI Therapist.

        """


    )



page_names_to_funcs = {
    #"Login": st.switch_page("pages/login.py"),
    "Home": main_page,
    "Mental Health Diagnosis": questions.ask_questions,
    "Visualization": visualizations.show_visualization,
    "Chat With AI Therepist": ai_chatbot.ai_therepist,
    "Guidance": guidance.show_guidance,
    "Admin": admin.admin_page,
}

#demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
demo_name = st.sidebar.radio("Select an option", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

#trigger_page()
