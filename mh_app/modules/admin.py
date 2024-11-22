import streamlit as st
from modules import db

c1,c2,c3,c4,c5,c6 = st.columns(6)


def logout():
    print("logout")
    



def delete_users():
    username = st.text_input("User to delete")
    if username:
        if st.button("Delete User"):
            db.delete_user(username)
            #st.success("User {username} deleted".format(username=username))

def show_users():
    if st.button("Show Registered Users"):
        db.show_users()

def admin_page():
    st.title("Admin Page")
    sidebar_logo = "images/logo.png"
    with st.sidebar:
        st.image(sidebar_logo)
        
    #c6.button("logout",on_click=logout)  
    show_users()
    delete_users()
    #with c6:
     #   st.button("logout")
        
#admin_page()
