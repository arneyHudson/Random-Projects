from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re

class UmpireCentreScraper:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = webdriver.Chrome()
        self.contacts_df = pd.DataFrame(columns=['Name', 'Phone Number'])

    def login(self):
        self.driver.get('https://www.umpirecentre.com/Login.aspx?')

        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Genericemail'))
        )
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Genericpassword'))
        )

        email_field.send_keys(self.email)
        password_field.send_keys(self.password)

        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ctl00_btnLoginRight'))
        )
        login_button.click()

        time.sleep(3)

        if "Login.aspx" not in self.driver.current_url:
            print("Login Successful!")
        else:
            print("Login Failed.")

    def scrape_contacts(self):
        url = 'https://www.umpirecentre.com/bRef_Pref_Phone.aspx'
        self.driver.get(url)

        table_container = self.driver.find_element('id', 'ctl00_ContentPlaceHolder1_pnlGrid')
        table = table_container.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.XPATH, './/tr')

        contacts = {}

        for row in rows[1:]:
            columns = row.find_elements(By.TAG_NAME, 'td')

            if len(columns) == 3:
                last_name = columns[0].find_element(By.TAG_NAME, 'span').text.strip()
                first_name = columns[1].find_element(By.TAG_NAME, 'span').text.strip()
                phone_number = columns[2].find_element(By.TAG_NAME, 'span').text.strip()

                # Check if names are single initials, capitalize both letters
                first_name = re.sub(r'[^\w\s-]', '', first_name)
                last_name = re.sub(r'[^\w\s-]', '', last_name)

                # Capitalize the first letter of each name part
                normalized_first_name = first_name.title()
                normalized_last_name = last_name.title()

                # Use regex to capitalize initials
                normalized_first_name = re.sub(r'\b([a-z]{2})\b', lambda x: x.group(1).upper(), normalized_first_name)
                normalized_last_name = re.sub(r'\b([a-z]{2})\b', lambda x: x.group(1).upper(), normalized_last_name)

                normalized_name = f"{normalized_first_name} {normalized_last_name} (Umpire)"

                if normalized_name != 'Hudson Arney (Umpire)':
                    contacts[normalized_name] = phone_number

        self.contacts_df = pd.DataFrame(contacts.items(), columns=['Name', 'Phone Number'])

    def save_contacts_csv(self, filename='contacts.csv'):
        self.contacts_df.to_csv(filename, index=False)

    def close_driver(self):
        self.driver.quit()

    @classmethod
    def main(cls):
        email = ''
        password = ''

        scraper = cls(email, password)
        scraper.login()
        scraper.scrape_contacts()
        scraper.save_contacts_csv()
        scraper.close_driver()

if __name__ == "__main__":
    UmpireCentreScraper.main()
