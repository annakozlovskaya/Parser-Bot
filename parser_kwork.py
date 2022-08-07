import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

def parser_kwork():
    HOST_KWORK = 'https://kwork.ru'
    URL_KWORK = 'https://kwork.ru/projects?c=41'

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(options=option)
    driver.get(URL_KWORK)
    time.sleep(2)
    items = driver.find_elements(By.CLASS_NAME, 'card__content')

    task_kwork_dict = {}
    for item in items:
        title = item.find_element(By.CLASS_NAME, 'wants-card__header-title').text
        link = item.find_element(By.CLASS_NAME, 'wants-card__header-title').find_element(By.TAG_NAME, 'a').get_attribute('href')
        price = item.find_element(By.CLASS_NAME, 'wants-card__header-price').text

        task_id = link.split('/')[-1]

        task_kwork_dict[task_id] = {
            'title': title,
            'link': link,
            'price': price
        }

    with open('task_kwork_dict.json', 'w', encoding='utf-8') as file:
        json.dump(task_kwork_dict, file, indent=4, ensure_ascii=False)


def check_new_task_kwork():
    with open('task_kwork_dict.json', encoding='utf-8') as file:
        task_kwork_dict = json.load(file)

    HOST_KWORK = 'https://kwork.ru'
    URL_KWORK = 'https://kwork.ru/projects?c=41'

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(options=option)
    driver.get(URL_KWORK)
    time.sleep(2)
    items = driver.find_elements(By.CLASS_NAME, 'card__content')

    fresh_task = {}

    for item in items:
        link = item.find_element(By.CLASS_NAME, 'wants-card__header-title').find_element(By.TAG_NAME, 'a').get_attribute('href')
        task_id = link.split('/')[-1]

        if task_id in task_kwork_dict:
            continue
        else:
            title = item.find_element(By.CLASS_NAME, 'wants-card__header-title').text
            link = item.find_element(By.CLASS_NAME, 'wants-card__header-title').find_element(By.TAG_NAME,'a').get_attribute('href')
            price = item.find_element(By.CLASS_NAME, 'wants-card__header-price').text

            task_kwork_dict[task_id] = {
                    'title': title,
                    'link': link,
                    'price': price
                }

            fresh_task[task_id] = {
                'title': title,
                'link': link,
                'price': price
            }
    with open('task_kwork_dict.json', 'w', encoding='utf-8') as file:
        json.dump(task_kwork_dict, file, indent=4, ensure_ascii=False)

    return fresh_task


def main():
    # parser_kwork()
    check_new_task_kwork()

if __name__ =='__main__':
    main()