import streamlit as st
import pandas as pd
import openai
from modules import db
import tabulate
import sqlite3
from groq import Groq
import os

DATABASE_PATH = "./database/mental_health.db"
GROQ_MODEL = 'mixtral-8x7b-32768'
TIMEOUT = 120
groq_client = Groq(
    api_key=os.getenv('GROQ_API_KEY'),
)
# Authenticate with the OpenAI API
openai.api_key = "xxx"

def show_guidance():
    st.write("## Mental Health Guidances")

    # Retrieve the data from the database
    conn = conn = sqlite3.connect('database/mental_health.db') #db.create_connection()
    df = pd.read_sql_query("SELECT * FROM mental_health ORDER BY date DESC", conn)

    # Generate the prompt string
    dataframe_string = tabulate.tabulate(df.head(), headers='keys', tablefmt='pipe', showindex=False)
    print(dataframe_string)
    prompt = f"""
            Data:

            {dataframe_string}

            You are a Mental Health Therapist . Analyze the data given to provide mental health guidance.
            """
 

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
        st.download_button(
                label="Export Guidance",
                data=guidance,
                file_name="Guidance.txt")
