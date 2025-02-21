import streamlit as st
import psycopg2
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = st.secrets["postgresql"]["user"]
PASSWORD = st.secrets["postgresql"]["password"]
HOST = st.secrets["postgresql"]["host"]
PORT = st.secrets["postgresql"]["port"]
DBNAME = st.secrets["postgresql"]["dbname"]

def web_driver():
    options = Options()
    options.add_argument('--verbose')
    options.add_argument('--no-sandbox')
    options.add_argument("--headless=new")
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920x1080")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
    driver = webdriver.Chrome(options=options)
    return driver

# Connect to the database
try:
    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    st.write("Connection successful!")
    # Create a cursor to execute SQL queries
    c = conn.cursor()

    start_button = st.button("Uruchom", type="primary")
    if start_button:
        driver = web_driver()
        driver.get('https://www.flashscore.pl/')
        try:
            cookies = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')))
            cookies.click()
        except:
            pass
    
        st.write(driver.title)
        all_match = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Zobacz szczegóły meczu!"]')))
        ilosc = len(all_match)
        st.write(ilosc)

except Exception as e:
    st.write(f"Failed to connect: {e}")

finally:
    c.close()
    conn.close()
    st.write("Connection closed.")
    

st.title('Test')
