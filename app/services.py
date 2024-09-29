import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

logging.basicConfig(filename="scraping.log", level=logging.INFO)

def scrape_linkedin_jobs(job_title: str, location: str, pages: int = None) -> list:
    logging.info(f'Starting LinkedIn job scrape for "{job_title}" in "{location}"...')
    
    pages = pages or 1
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Firefox(options=options)
    driver.get(f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}")

    for i in range(pages):
        logging.info(f"Scrolling to bottom of page {i+1}...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/section[2]/button"))
            )
            element.click()
        except Exception:
            logging.info("Show more button not found, retrying...")

        time.sleep(random.choice(list(range(3, 7))))

    jobs = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_listings = soup.find_all(
        "div",
        class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card"
    )

    try:
        for job in job_listings:
            job_title = job.find("h3", class_="base-search-card__title").text.strip()
            job_company = job.find("h4", class_="base-search-card__subtitle").text.strip()
            job_location = job.find("span", class_="job-search-card__location").text.strip()
            apply_link = job.find("a", class_="base-card__full-link")["href"]

            driver.get(apply_link)
            time.sleep(random.choice(list(range(5, 11))))

            try:
                description_soup = BeautifulSoup(driver.page_source, "html.parser")
                job_description = description_soup.find(
                    "div", class_="description__text description__text--rich"
                ).text.strip()
            except AttributeError:
                job_description = None
                logging.warning("AttributeError occurred while retrieving job description.")

            jobs.append({
                "title": job_title,
                "company": job_company,
                "location": job_location,
                "link": apply_link,
                "description": job_description,
            })
            logging.info(f'Scraped "{job_title}" at {job_company} in {job_location}...')

    except Exception as e:
        logging.error(f"An error occurred while scraping jobs: {str(e)}")
        return jobs

    driver.quit()
    return jobs


if __name__ == "__main__":
    data = scrape_linkedin_jobs("Werkstudent", "berlin", 1)
    print(data)
