import os
import setuptools  # PATCH FOR PYTHON 3.14+

from django.core.management.base import BaseCommand
from core.models import JobPost

# Selenium library components
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # ,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc

# Other libraries
import time
import re
import random
from core.utils import clean_salary
# import pandas as pd


class Command(BaseCommand):
    help = "Scrapes Python roles and saves them to the database."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Selenium Scraper Started!"))


        # # Headless or Run chrome invisibly without opening the chrome tab
        # chrome_options = Options()
        # chrome_options.add_argument("--headless=new")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")

        # # Initialize the browser
        # driver = webdriver.Chrome(options=chrome_options)

        # Initialize undetected_chromedriver options cleanly
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu") 

        # Boot the patched stealth browser instance
        driver = uc.Chrome(options=chrome_options, headless=True, version_main=149)  
        

        # Helper function to get text or return "N/A"
        def get_text_safe(element, selector):
            try:
                return element.find_element(By.CSS_SELECTOR, selector).text.strip()
            except NoSuchElementException:
                return "N/A"

        try:
            target_url = os.environ.get('SCRAPER_TARGET_URL')
            driver.get(target_url)
            driver.maximize_window()

            # Find the search job and click
            search_job = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "jobkeyword"))
                )
            search_job.click()

            # Input skill (Human-like typing delay)
            skill = 'python'
            for char in skill:
                search_job.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))

            # Entering (Random delay)
            search = driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-rounded btn-primary text-uppercase']")
            time.sleep(random.uniform(1, 2))
            search.send_keys(Keys.ENTER)

            # # Find the total jobs available and shown in the site
            # jobs = driver.find_element(By.XPATH, "//p[@class='fs-12']").text
            # values = re.findall(r'\d+', jobs)

            page = 1
            max_pages = 10
            consecutive_duplicates = 0
            while page <= max_pages:
                print(f"Scraping page {page}...")

                # Scroll down gradually like a human reading
                total_height = int(driver.execute_script("return document.body.scrollHeight"))
                for i in range(1, total_height, random.randint(300, 600)):
                    driver.execute_script(f"window.scrollTo(0, {i});")
                    time.sleep(random.uniform(0.1, 0.3))

                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #Auto Scroll


                job_cards = driver.find_elements(By.CLASS_NAME, "jobpost-cat-box")
                for card in job_cards:

                    # Safely extract text for search field
                    title = get_text_safe(card, ".fs-16.fw-700")
                    date = get_text_safe(card, ".fs-13.mb-0")
                    salary = get_text_safe(card, ".row.fs-14.no-gutters.align-items-top.mt-2.mb-2.mt-sm-0.mb-sm-0")

                    cleaned_salary_data = clean_salary(salary)

                    badge_elements = card.find_elements(By.CSS_SELECTOR, ".job-tag a.badge")
                    
                    # Clean and filter out any empty strings from the badges
                    skills_list = [b.text.strip() for b in badge_elements if b.text.strip()]
                    
                    # If the list has items, join them. Otherwise, mark as "N/A"
                    if skills_list:
                        required_skill = ", ".join(skills_list)
                    else:
                        required_skill = "N/A"
                    
                    # Safely get attribute
                    try:
                        link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    except NoSuchElementException:
                        self.stdout.write(self.style.WARNING(f"⚠️ Could not find link for job card. Skipping."))
                        continue

                    obj, created = JobPost.objects.get_or_create(
                        link=link,
                        defaults={
                            'title': title,
                            'raw_salary': salary,
                            'raw_date_posted': date,
                            'required_skills': required_skill,
                            'min_salary': cleaned_salary_data['min_salary'],
                            'max_salary': cleaned_salary_data['max_salary'],
                            'currency': cleaned_salary_data['currency'],
                            'salary_period': cleaned_salary_data['salary_period'],
                        }
                    )

                    if created:
                        self.stdout.write(f"Added: {title}")
                        consecutive_duplicates = 0
                    else:
                        self.stdout.write(f"Skipped (Duplicate): {title}")
                        consecutive_duplicates += 1

                    # Break inner loop if we hit the cap
                    if consecutive_duplicates >= 5:
                        break

                # If hit 5 old jobs in a row, stop the entire pipeline early
                if consecutive_duplicates >= 5:
                    self.stdout.write(self.style.SUCCESS("✨ Caught up to previously scraped jobs. Stopping early to save bandwidth!"))
                    break


                # Checks if the next button is still available
                next_btns = driver.find_elements(By.CSS_SELECTOR, "li[aria-label='Next'] a")
                if next_btns:
                    next_btns[0].click()
                    page += 1
                    # Random wait between 4 to 8 seconds
                    time.sleep(random.uniform(4.0, 8.0))
                else:
                    print("No more pages.")
                    break

            # name_csv = 'python_jobs_try.csv'
            # df = pd.DataFrame(results)
            # df.to_csv(name_csv, index=False)
            # print(f"Scraping complete. Saved to {name_csv}")

        finally:
            driver.quit()
        
        
        self.stdout.write(self.style.SUCCESS("🎉 Scraping Complete!"))