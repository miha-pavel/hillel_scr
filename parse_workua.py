import time
from user_agent import generate_user_agent
from utils import random_sleep, save_info

import requests
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait



# # Указываем название файла базы данных
# conn = sqlite3.connect('work_data.sqlite')
# cursor = conn.cursor()

# # Создаем таблицу pyblog с двумя полями - title и article
# try:
#     cursor.execute('''CREATE TABLE work_data (title text, article longtext)''')
# except:
#     pass

# Вставляем в таблицу pyblog первую запись со значениями title и article
# cursor.execute("INSERT INTO pyblog (title, article) VALUES ('Название статьи','Длинный текст статьи')")
# conn.commit()

# # Вставляем в таблицу pyblog вторую запись со значениями title и article
# cursor.execute("INSERT INTO pyblog (title, article) VALUES ('Название второй статьи','Еще более длинный текст статьи')")
# conn.commit()

# # Делаем выборку всех имеющихся в таблице записей и в цикле печатаем их значения
# cursor.execute('SELECT * FROM pyblog')
# row = cursor.fetchone()
# while row is not None:
#    print(row[0])
#    print(row[1]+'\n')
#    row = cursor.fetchone()

# # Закрываем соединение с базой данных
# cursor.close()
# conn.close()




# global variables
HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'


def main():
    page = 1
    # while True:
    #     page += 1
    payload = {
        'ss': 1,
        'page': page,
    }
    user_agent = generate_user_agent()
    headers = {
        'User-Agent': user_agent,
    }

    # print(f'PAGE: {page}')
    response = requests.get(HOST + ROOT_PATH, params=payload, headers=headers)
    response.raise_for_status()
    # random_sleep()

    # if response.status_code != 200:
    #     print('something wrong!')
    #     break

    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    class_ = 'card card-hover card-visited wordwrap job-link'
    cards = soup.find_all('div', class_=class_)
    if not cards:
        cards = soup.find_all('div', class_=class_ + ' js-hot-block')

    result = []
    # if not cards:
    #     break

    # print('cards: ', cards)
    for card in cards:
        tag_a = card.find('h2').find('a')
        title = tag_a.text
        href = tag_a['href']
        result.append([title, href])

        # get vacancy full info
        vacancy_url = HOST + href
        response = requests.get(vacancy_url, headers=headers)
        print('vacancy_url: ', vacancy_url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # # Salary
        # salary_data = ''
        # try:
        #     salary_block = soup.findAll("span", {"class": "glyphicon-hryvnia"})[0].parent
        #     salary_data = salary_block.findAll("b", {"class": "text-black"})[0].string
        #     print('salary_data: ', salary_data)
        # except:
        #     salary_data = None
        #     print('salary_data: ', salary_data)
        # #Company
        # company_data = ''
        # try:
        #     company_block = soup.findAll("span", {"class": "glyphicon-company"})[0].parent
        #     company_data = company_block.findAll("b")[0].string
        # except:
        #     company_data = None
        # #Location
        # location_data = ''
        # try:
        #     location_block = soup.findAll("span", {"class": "glyphicon-map-marker"})[0].parent
        #     location_data = location_block.contents[2]
        # except:
        #     location_data = None
        # #Conditions
        # condition_data = ''
        # try:
        #     condition_block = soup.findAll("span", {"class": "glyphicon-tick"})[0].parent
        #     condition_data = " ".join(condition_block.contents[2].split())
        # except:
        #     condition_data = None
        # # #Phone
        # phone_data = ''
        # contact_phone = soup.find(id="contact-phone")
        # if contact_phone:
        #     webdriver_options = Options()
        #     # webdriver_options.add_argument('--headless')
        #     driver = webdriver.Chrome(options=webdriver_options)
        #     driver.get(vacancy_url)
        #     WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.ID, 'contact-phone')))
        #     driver.find_element_by_class_name('js-get-phone').click()
        #     opened_phone = driver.find_element_by_id('contact-phone')
        #     phone_data = opened_phone.find_element_by_tag_name('a').text
        #     driver.close()
        # #Description
        # description_data = ''
        # try:
        #     description_block = soup.find(id="job-description")
        #     description_data = " ".join(description_block.get_text().split())
        # except:
        #     description_data = None

    save_info(result)



if __name__ == "__main__":
    main()

# 1 parse vacancy details - 6
# 2 save all info to sqlite database (CREATE TABLE, INSERT VALUES INTO TABLE) - 2
# 3 save to json file! vacancy.json [{}, {}, {}] - 2