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
    options = webdriver.ChromeOptions()
    options.add_argument('--verbose')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--enable-javascript")
    options.add_argument("--incognito")
    options.add_argument("--nogpu")
    options.add_argument("--window-size=1920x1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
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
        all_match = driver.find_elements(By.XPATH,'//*[@title="Zobacz szczegóły meczu!"]')
        for match in all_match:
            liga = mecz.find_element(By.XPATH,'./preceding::div[contains(@class,"wclLeagueHeader")][1]/div[2]/div[1]/div[2]/span[1]').text
            st.write(liga)
        c.close()
        conn.close()
        st.write("Connection closed.")



except Exception as e:
    st.write(f"Failed to connect: {e}")

st.title('Test')
