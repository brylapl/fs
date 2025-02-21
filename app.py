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
from time import sleep
import time
from datetime import datetime
from datetime import timedelta

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

    open_flashscore = st.button("Otwórz Flashscore", type="primary")
    tabela = []
    if open_flashscore:
        driver = web_driver()
        driver.get('https://www.flashscore.pl/')
        try:
            cookies = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')))
            cookies.click()
        except:
            pass
        st.write(driver.title)

        date_page = st.checkbox("I agree")
            if date_page:
            st.write("Wybierz ilośćdni do przodu. 1: jutro, 2:pojutrze, 3" za 3 dni itd.")
            number = st.number_input("Dni do porzodu",min_value=1, max_value=7, step=1)
            st.write("Wybrna ilość dni do przodu:", number)
            
            open_date = st.button("Otwórz wybraną datę", type="primary")
            if open_date:
                date_picker = driver.find_element(By.XPATH,'//button[@id="calendarMenu"]')
                date_picker.click()
                data = driver.find_element(By.XPATH,'//li[@class="calendar__listItem"]/button[contains(text(),"Dzisiaj")]/../following-sibling::li[number]')
                data.click()
                data_txt = data.text
                st.write(data_txt)
        
        
        
    
        
        # all_match = driver.find_elements(By.XPATH,'//*[@title="Zobacz szczegóły meczu!"]')
        # data = driver.find_element(By.XPATH,'//button[@id="calendarMenu"]').text

        # data = data.split(' ')[0]
        # data = f'{data}/2025'
        # data = datetime.strptime(data, "%d/%m/%Y")
        # data = data.strftime("%Y-%m-%d")
        # ilosc = len(all_match)
        # for mecz in all_match:
        #     liga = mecz.find_element(By.XPATH,'./preceding::div[contains(@class,"wclLeagueHeader")][1]/div[2]/div[1]/div[2]/span[1]').text
        #     rozgrywki = mecz.find_element(By.XPATH,'./preceding::div[contains(@class,"wclLeagueHeader")][1]/div[2]/div[1]/div[2]/a').text
        #     id = mecz.find_element(By.XPATH,'./..')
        #     id = id.get_attribute('id')
        #     id = id[4:]
        #     ilosc -= 1
        #     url = f'https://www.flashscore.pl/mecz/{id}/#/zestawienie-kursow/kursy-1x2/koniec-meczu'
        #     time = mecz.find_element(By.XPATH,'./following-sibling::div[1]').text
        #     home = mecz.find_element(By.XPATH,'./following-sibling::div[2]').text
        #     away = mecz.find_element(By.XPATH,'./following-sibling::div[3]').text
        #     stats = {
        #         'data': data,
        #         'time':time,
        #         'liga': liga,
        #         'rozgrywki':rozgrywki,
        #         'home': home,
        #         'away': away,
        #         'url':url,
        #         }
        #     tabela.append(stats)

        # df = pd.DataFrame(tabela)
        # records_home = df.to_records(index=False)
        # list_of_tuples_home = list(records_home)
        # c.executemany('INSERT INTO upcoming_match (data, time, liga, rozgrywki, home, away, url) VALUES (%s, %s, %s, %s, %s, %s, %s)', list_of_tuples_home)
        # conn.commit()
        
        c.close()
        conn.close()
        st.write("Connection closed.")

except Exception as e:
    st.write(f"Failed to connect: {e}")

st.title('Test')
