import streamlit as st
from modules import questions
from modules import visualizations
from modules import ai_chatbot
from modules import guidance
from modules import admin
from modules import db
from time import sleep

#st.set_page_config(layout="wide")
if st.session_state['logged_in']:
    username = st.session_state['current_user']
    
    # Add username to sidebar
    with st.sidebar:
        st.markdown(f"""
            <div style='
                padding: 8px; 
                text-color: #f0f2f6;
                text-align: left; 
                font-weight: bold;
                border-bottom: 2px solid #f0f2f6;
                margin-bottom: 10px;'>
                👤 Welcome {username}!
            </div>
        """, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown(f"""
            <div style='
                padding: 8px; 
                text-color: #f0f2f6;
                text-align: left; 
                font-weight: bold;
                border-bottom: 2px solid #f0f2f6;
                margin-bottom: 10px;'>
                🔆 MindPath: Your Path To Better Health!
            </div>
        """, unsafe_allow_html=True)
        
def main_page():
    import streamlit as st
    print(st.session_state.get("current_user", None))
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
        - Track daily activities

        """


    )


if st.session_state.get("current_user", None):
    col3,spacer, col4 = st.columns([6, 0.5,1])  

    with col3:
        # Add custom CSS for rainbow text
        st.markdown(
            """
            <style>
            .rainbow-title {
                font-size: 30px;
                font-weight: bold;
                text-align: left;
                background: linear-gradient(90deg, red, orange, yellow, green,blue);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            </style>
            """,
            unsafe_allow_html=True
            #blue, indigo, violet
        )

        # Use the rainbow text class
        #st.markdown("🧠 <div class='rainbow-title'>MindPath:Path To Better Health</div>", unsafe_allow_html=True)
        st.title("**🧠 :rainbow[MindPath:To Better Health]**")

    with col4:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.session_state.page = "login"
            st.switch_page("login.py")

    page_names_to_funcs = {
        #"Login": st.switch_page("pages/login.py"),
        "🏠 Home": main_page,
        "📝 Mental Health Diagnosis": questions.ask_questions,
        "📊 Visualization": visualizations.show_visualization,
        "✨ Chat With AI Therapist": ai_chatbot.ai_therepist,
        "⛹🏾 Track Activities":questions.track_activities,
        "✨ Guidance": guidance.show_guidance,
        #"Admin": admin.admin_page,
    }
    if st.session_state.get("current_user", None)=='admin':
        page_names_to_funcs["Admin"] = admin.admin_page

    #demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    demo_name = st.sidebar.radio("Select an option", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()

    
else:
    st.switch_page("login.py")

url = "https://telemanas.mohfw.gov.in/home"
with st.sidebar:
    st.markdown(f"""
        <div style='
            padding: 8px; 
            text-color: #f0f2f6;
            text-align: left; 
            font-weight: bold;
            border-bottom: 2px solid #f0f2f6;
            margin-bottom: 10px;'>
            🚨 Get more help on Govt of India National Tele MANAS helpline <a href="https://telemanas.mohfw.gov.in/home">telemanas</a>
        </div>
    """, unsafe_allow_html=True)

#trigger_page()
