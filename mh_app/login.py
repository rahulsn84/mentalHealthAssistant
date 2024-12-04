import streamlit as st
from modules import db

def set_login():
    print("In set login")
    st.session_state.login_clicked = True
    
def reset_login():
    print("In reset login")
    st.session_state.login_clicked = False
    
if "login_clicked" not in st.session_state:
    st.session_state["login_clicked"] = None

placeholder = st.empty()
# Login page
def login_page():
    st.title("Login Page")
    sidebar_logo = "mh_app/images/logo.png"
    with st.sidebar:
        st.image(sidebar_logo)
    print("In login page")
    # Insert a form in the container
    #if st.session_state["login_clicked"] == None:
    #with placeholder:
    st.markdown("#### Enter your credentials")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    c1,c2 = st.columns([5,1],gap="large")
    #if username and password:
    if c1.button("Login",on_click=set_login):
        if st.session_state["login_clicked"] != None:
            st.session_state.page = ""
            if db.validate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("Login successful!")
                #placeholder.empty()
                #sleep(0.01)
                #st.session_state.page = "main"
                print("triggering page with main")
                st.switch_page("pages/MindPath.py")
                #trigger_page()
            else:
                st.error("Invalid username or password.")
    st.session_state["login_clicked"] = None

    if c2.button("Sign up"):
        st.switch_page("pages/Register.py")
            
login_page()
