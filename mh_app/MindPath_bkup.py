import streamlit as st
from modules import questions
from modules import visualizations
from modules import ai_chatbot
from modules import guidance
from modules import db
from time import sleep

st.set_page_config(layout="wide")

def main_page():
    import streamlit as st

    st.write("# Welcome to MindPath! 👋")
    #st.sidebar.success("Select an option.")
    sidebar_logo = "images/happy-face.png"
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

if "reg_submitted" not in st.session_state:
    st.session_state["reg_submitted"] = None
    
def submitted():
    print("In reg submitted")
    st.session_state.reg_submitted = True
    
def reset():
    st.session_state.reg_submitted = False
    
# Create an empty container
placeholder = st.empty()
placeholder2 = st.empty()
# Registration page
def register_page():
    st.session_state.page = "reg"
    st.title("Register as a New User")

    #submit_reg = ""
    #with placeholder2.form("RegisterUser"):
    st.markdown("#### Enter your credentials")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    #if st.button("Register"):
    print("Before submit_reg")
    if new_username and new_password and confirm_password:
        submit_reg = st.button("RegisterUser",on_click=submitted)
        if 'reg_submitted' in st.session_state: #submit_reg:
            print("passwords entered ",confirm_password,new_password)
            #reset()
            st.session_state.page = ""
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            elif db.validate_username(new_username):
                st.error("UserName Already Exist")
            else:
                print("passwords match ",confirm_password,new_password)
                db.register_user(new_username, new_password)
                st.success("Registration successful! Please Login.")
                #placeholder2.empty()
                st.session_state.page = "login"
                if st.button("Login Page"):
                    print("triggering page with login")
                    trigger_page()
    
    #if st.button("Back to Login"):
    #    st.session_state.page = ""
        #trigger_page()
    #    st.session_state.page = "login"
    #    print("triggering page with login 2")
    #    trigger_page()
    
def login_process():
    print("In login process")
    st.session_state.login_clicked = True
    

if "login_clicked" not in st.session_state:
    st.session_state["login_clicked"] = None

# Login page
def login_page():
    #st.title("Login Page")
    print("In login page")
    # Insert a form in the container
    if st.session_state["login_clicked"] == None:
        with placeholder:
            st.markdown("#### Enter your credentials")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if username and password:
                submit = st.button("Login",on_click=login_process)
                if st.session_state["login_clicked"] != None:
                    st.session_state.page = ""
                    if db.validate_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.success("Login successful!")
                        #placeholder.empty()
                        #sleep(0.01)
                        st.session_state.page = "main"
                        print("triggering page with main")
                        trigger_page()
                    else:
                        st.error("Invalid username or password.")
                st.session_state["login_clicked"] = None

    with placeholder2:
        placeholder.empty()
        st.button("Register here",on_click=register_page)

    #username = st.text_input("Username")
    #password = st.text_input("Password", type="password")

    #if st.button("Login"):

    

    #if st.button("Register here"):
        #placeholder.empty()
    #    st.session_state.page = ""
    #    st.session_state.page = "reg"
    #    print("trigger reg page")
    #    trigger_page()
    #    st.rerun()

def trigger_page():
    page = st.session_state.get("page", "login")  
    print(page)
    if(page=="main"):
        main_page()
    elif(page=="reg"):
        register_page()
    elif(page=="login"):
        login_page()

page_names_to_funcs = {
    "Login": login_page,
    "Home": main_page,
    "Mental Health Diagnosis": questions.ask_questions,
    "Visualization": visualizations.show_visualization,
    "Chat With AI Therepist": ai_chatbot.ai_therepist,
    "Guidance": guidance.show_guidance,
}

#demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
demo_name = st.sidebar.radio("Select an option", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

#trigger_page()
