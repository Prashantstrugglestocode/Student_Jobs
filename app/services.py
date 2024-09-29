import pandas as pd
import time
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scrape_jobs(work_position: str, location: str):
    # Get the base URL from environment variables
    url = os.getenv('url')
    
    # Ensure the URL is valid
    if not url:
        print("Base URL not found in environment variables.")
        return

    # Modify the URL with the work position and location
    modified_url = f"{url}?keywords={work_position}&location={location}"
    
    # Set up the Firefox browser options
    options = webdriver.FirefoxOptions()
    # Uncomment the line below to run the browser in headless mode
    # options.add_argument("-headless")
    
    # Initialize the Firefox WebDriver
    driver = webdriver.Firefox(options=options)
    
    # Open the modified URL
    driver.get(url=modified_url)

    # You can add more code here to wait for elements or scrape job data
    
    # Close the driver after scraping
    driver.quit()

if __name__ == "__main__":
    # Call the function with specific parameters
    scrape_jobs("Work Students", "Berlin")
