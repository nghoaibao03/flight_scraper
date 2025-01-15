import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from modules.vietjet_scraper import scrape_vietjet_data, setup_browser
from modules.data_processor import clean_data, save_to_csv

st.set_page_config(page_title="VietJet Scraper", layout="wide")

st.title("VietJet Flight Data Scraper 🚀")
nums_date = st.sidebar.slider("Select Number of Days to Scrape", 1, 30, 12)
if st.button("Start Scraping"):
    with st.spinner("Scraping data... This might take a while."):
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wait = WebDriverWait(browser, 10)
        setup_browser(browser, "https://www.vietjetair.com", wait)
        raw_data = scrape_vietjet_data(browser, nums_date)
        browser.quit()

        st.success("Scraping completed!")
        clean_df = clean_data(raw_data)
        save_to_csv(clean_df, "vietjet_data.csv")
        st.write(clean_df)
        st.download_button(
            label="Download Data as CSV",
            data=clean_df.to_csv(index=False).encode('utf-8'),
            file_name='vietjet_data.csv',
            mime='text/csv'
        )
