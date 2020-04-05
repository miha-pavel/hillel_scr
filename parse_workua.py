import time
import json

import requests
import sqlite3
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from utils import random_sleep, save_info


conn = sqlite3.connect('workua_data.sqlite')
cursor = conn.cursor()


try:
    cursor.execute('''CREATE TABLE workua_data (
        title text,
        salary text,
        company text,
        location text,
        condition text,
        phone text,
        description longtext)''')
except:
    pass

# global variables
HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'


def main():
    page = 1
    result = []
    result_list = []
    while True:
        page += 1
        payload = {
            'ss': 1,
            'page': page,
        }
        user_agent = generate_user_agent()
        headers = {
            'User-Agent': user_agent,
        }

        response = requests.get(HOST + ROOT_PATH, params=payload, headers=headers)
        response.raise_for_status()
        random_sleep()

        if response.status_code != 200:
            print('something wrong!')
            break

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        class_ = 'card card-hover card-visited wordwrap job-link'
        cards = soup.find_all('div', class_=class_)
        if not cards:
            cards = soup.find_all('div', class_=class_ + ' js-hot-block')

        if not cards:
            break

        for card in cards:
            tag_a = card.find('h2').find('a')
            title = tag_a.text
            href = tag_a['href']

            # get vacancy full info
            vacancy_url = HOST + href
            response = requests.get(vacancy_url, headers=headers)
            print('vacancy_url: ', vacancy_url)
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # Salary
            salary_data = ''
            try:
                salary_block = soup.findAll("span", {"class": "glyphicon-hryvnia"})[0].parent
                salary_data = salary_block.findAll("b", {"class": "text-black"})[0].string
            except:
                salary_data = None
            #Company
            company_data = ''
            try:
                company_block = soup.findAll("span", {"class": "glyphicon-company"})[0].parent
                company_data = company_block.findAll("b")[0].string
            except:
                company_data = None
            #Location
            location_data = ''
            try:
                location_block = soup.findAll("span", {"class": "glyphicon-map-marker"})[0].parent
                location_data = location_block.contents[2].strip()
            except:
                location_data = None
            #Condition
            condition_data = ''
            try:
                condition_block = soup.findAll("span", {"class": "glyphicon-tick"})[0].parent
                condition_data = " ".join(condition_block.contents[2].split())
            except:
                condition_data = None
            #Phone
            phone_data = ''
            contact_phone = soup.find(id="contact-phone")
            if contact_phone:
                webdriver_options = Options()
                driver = webdriver.Chrome(options=webdriver_options)
                driver.get(vacancy_url)
                WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.ID, 'contact-phone')))
                driver.find_element_by_class_name('js-get-phone').click()
                opened_phone = driver.find_element_by_id('contact-phone')
                try:
                    phone_data = opened_phone.find_element_by_tag_name('a').text
                except:
                    phone_data = opened_phone.text
                driver.close()
            #Description
            description_data = ''
            try:
                description_block = soup.find(id="job-description")
                description_data = " ".join(description_block.get_text().split())
            except:
                description_data = None
            # Load data
            result.append({
                'title': title,
                'salary': salary_data,
                'company': company_data,
                'location': location_data,
                'condition': condition_data,
                'phone': phone_data,
                'description': description_data,
                })
            result_list.append((title, salary_data, company_data, location_data, condition_data, phone_data, description_data))

    cursor.executemany(f'INSERT INTO workua_data (title, salary, company, location, condition, phone, description) VALUES (?, ?, ?, ?, ?, ?, ?)', result_list)
    conn.commit()
    cursor.close()
    conn.close()
        
    with open('workua_data.txt', 'w') as outfile:
        json.dump(result, outfile, ensure_ascii=False)


if __name__ == "__main__":
    main()