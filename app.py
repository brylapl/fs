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

    

    driver = web_driver()

    driver.get('https://www.flashscore.pl/')
    st.write(driver.title)
    all_match = driver.find_elements(By.XPATH,'//*[@title="Zobacz szczegóły meczu!"]')
    ilosc = len(all_match)
    st.write(ilosc)
    data = '2025-02-21
    tabela = []

    for mecz in all_match[0:6]:
            liga = mecz.find_element(By.XPATH,'./preceding::div[contains(@class,"wclLeagueHeader")][1]/div[2]/div[1]/div[2]/span[1]').text
            rozgrywki = mecz.find_element(By.XPATH,'./preceding::div[contains(@class,"wclLeagueHeader")][1]/div[2]/div[1]/div[2]/a').text
            id = mecz.find_element(By.XPATH,'./..')
            id = id.get_attribute('id')
            id = id[4:]
            ilosc -= 1
            url = f'https://www.flashscore.pl/mecz/{id}/#/zestawienie-kursow/kursy-1x2/koniec-meczu'
            time = mecz.find_element(By.XPATH,'./following-sibling::div[1]').text
            home = mecz.find_element(By.XPATH,'./following-sibling::div[2]').text
            away = mecz.find_element(By.XPATH,'./following-sibling::div[3]').text
            stats = {
                'data': data,
                'time':time,
                'home': home,
                'away': away,
                'Url':url,
                }
            tabela.append(stats)
    df = pd.DataFrame(tabela)

    records_home = df.to_records(index=False)
    list_of_tuples_home = list(records_home)

    c.executemany('INSERT INTO match (data, time, home, away, url) VALUES (?,?,?,?,?)',list_of_tuples_home)
    conn.commit()

    try:
        # Example query
        c.execute("SELECT * FROM match")
        result = c.fetchone()
        st.write('Data:', result[3])
        st.write('Home:', result[4])
    except:
        st.write('Brak danych')

    # Close the cursor and connection
    c.close()
    conn.close()
    st.write("Connection closed.")

except Exception as e:
    st.write(f"Failed to connect: {e}")

st.title('Test')
