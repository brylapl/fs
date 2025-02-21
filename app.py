import streamlit as st

import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = st.secrets["postgresql"]["user"]
PASSWORD = st.secrets["postgresql"]["password"]
HOST = st.secrets["postgresql"]["host"]
PORT = st.secrets["postgresql"]["port"]
DBNAME = st.secrets["postgresql"]["dbname"]
st.write(HOST)

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    st.write("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT * FROM match")
    result = cursor.fetchone()
    st.write('Data:', result[3])
    st.write('Home:', result[4])

    # Close the cursor and connection
    cursor.close()
    connection.close()
    st.write("Connection closed.")

except Exception as e:
    st.write(f"Failed to connect: {e}")

st.title('Test')
