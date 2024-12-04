import streamlit as st
import pandas as pd
import openai
from modules import db
import tabulate
import sqlite3
from groq import Groq
import os
from datetime import datetime

DATABASE_PATH = "./database/mental_health.db"
GROQ_MODEL = 'mixtral-8x7b-32768'
TIMEOUT = 120
groq_client = Groq(
    api_key=os.getenv('GROQ_API_KEY'),
)
# Authenticate with the OpenAI API

def show_guidance():
    sidebar_logo = "images/logo.png"
    with st.sidebar:
        st.image(sidebar_logo)
    st.write("## Your Mental Health Guidances")
    # Retrieve the data from the database
    conn = conn = sqlite3.connect('database/mental_health.db') #db.create_connection()
    df = pd.read_sql_query("SELECT * FROM mental_health where username='"+st.session_state.get("current_user", None)+"' ORDER BY date DESC", conn)
    df2 = pd.read_sql_query("SELECT * FROM activities where username='"+st.session_state.get("current_user", None)+"' ORDER BY date DESC", conn)

    # Generate the prompt string
    dataframe_string = tabulate.tabulate(df.head(), headers='keys', tablefmt='pipe', showindex=False)
    dataframe_string_activities = tabulate.tabulate(df2.head(), headers='keys', tablefmt='pipe', showindex=False)

    print(dataframe_string)
    prompt = f"""
             You are a Mental Health Therapist. I have been tracking my mental health metrics (serenity, sleep quality, productivity, and enjoyment) and activities (e.g., exercise, meditation, socializing) over the last 5 days.

            Metrics:
            {dataframe_string}

            Activities:
            {dataframe_string_activities}

            Please provide insights into patterns or trends in my data and give actionable tips to improve my serenity, sleep quality, productivity, and enjoyment. Additionally, suggest how I can optimize my activities for better well-being.

            """
    print(prompt)
    # Add a button to generate guidance
    if st.button("Generate guidance"):
        # Call the OpenAI API to generate guidance
        '''
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        '''

        response = groq_client.chat.completions.create(
                model='mixtral-8x7b-32768',
                messages=[
                        # Set an optional system message. This sets the behavior of the
                        # assistant and can be used to provide specific instructions for
                        # how it should behave throughout the conversation.
                        {
                            "role": "system",
                            "content": "you are a helpful AI therepist."
                        },
                        # Set a user message for the assistant to respond to.
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                temperature=0.2,
                stream=False,
            )

        # Display the response to the user
        #guidance = response.choices[0].text.strip()
        guidance = response.choices[0].message.content
        st.write(guidance)
        url = "https://telemanas.mohfw.gov.in/home"
        st.write("#### Get more help on GOI National Tele MANAS helpline [telemanas](%s)" % url)
        filename = datetime.now().strftime("%Y%m%d")
        guidance_ouput = "Guidance_"+filename+".txt"
        st.download_button(
                label="Export Guidance",
                data=guidance,
                file_name=guidance_ouput)
