import streamlit as st
from modules import db



if "reg_submitted" not in st.session_state:
    st.session_state["reg_submitted"] = None
    
def submitted():
    print("In reg submitted")
    st.session_state.reg_submitted = True
    
def reset():
    st.session_state.reg_submitted = False
    
def register_page():
    #st.session_state.page = "reg"
    st.title("Register as a New User")
    sidebar_logo = "images/logo.png"
    #st.logo(sidebar_logo, icon_image=sidebar_logo)
    with st.sidebar:
        st.image(sidebar_logo)

    #submit_reg = ""
    #with placeholder2.form("RegisterUser"):
    st.markdown("#### Enter your credentials")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit = st.button("Register")

    #if st.button("Register"):
    print("Before submit_reg")
    if new_username and new_password and confirm_password:
        if submit: #submit_reg:
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
                st.switch_page("login.py")
                #placeholder2.empty()
                #st.session_state.page = "login"
                #if st.button("Login Page"):
                #    print("triggering page with login")
                #    trigger_page()
                
register_page()