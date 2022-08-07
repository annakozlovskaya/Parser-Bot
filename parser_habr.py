import requests
from bs4 import BeautifulSoup
import json

def parser_habr():

    HOST_HABR = 'https://freelance.habr.com'
    URL_HABR = 'https://freelance.habr.com/tasks?categories=development_backend%2Cdevelopment_bots%2Cdevelopment_games&page=1&q=python'
    HEADERS = {'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'}


    request = requests.get(URL_HABR, headers=HEADERS)


    soup = BeautifulSoup(request.text, 'html.parser')
    items = soup.find_all('article', class_='task task_list')
    task_dict = {}
    for item in items:
            title = item.find('div', class_='task__title').find('a').get_text(strip=True)
            link = HOST_HABR + item.find('div', class_='task__title').find('a').get('href')
            price = item.find('div', class_='task__price').get_text(strip=True)

            task_id = link.split('/')[-1]

            task_dict[task_id] = {
                'title': title,
                'link': link,
                'price': price
            }

    with open('task_habr_dict.json', 'w', encoding='utf-8') as file:
        json.dump(task_dict, file, indent=4, ensure_ascii=False)

def check_new_task_habr():
    with open('task_habr_dict.json', encoding='utf-8') as file:
        task_dict = json.load(file)

    HOST_HABR = 'https://freelance.habr.com'
    URL_HABR = 'https://freelance.habr.com/tasks?categories=development_backend%2Cdevelopment_bots%2Cdevelopment_games&page=1&q=python'
    HEADERS = {'accept': 'application/json, text/javascript, */*; q=0.01',
               'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'}

    request = requests.get(URL_HABR, headers=HEADERS)

    soup = BeautifulSoup(request.text, 'html.parser')
    items = soup.find_all('article', class_='task task_list')

    fresh_task = {}

    for item in items:
        link = HOST_HABR + item.find('div', class_='task__title').find('a').get('href')
        task_id = link.split('/')[-1]

        if task_id in task_dict:
            continue
        else:
            title = item.find('div', class_='task__title').find('a').get_text(strip=True)
            link = HOST_HABR + item.find('div', class_='task__title').find('a').get('href')
            price = item.find('div', class_='task__price').get_text(strip=True)

            task_dict[task_id] = {
                'title': title,
                'link': link,
                'price': price
            }

            fresh_task[task_id] = {
                'title': title,
                'link': link,
                'price': price
            }
    with open('task_habr_dict.json', 'w', encoding='utf-8') as file:
        json.dump(task_dict, file, indent=4, ensure_ascii=False)

    return fresh_task


def main():
    # parser_habr()
    check_new_task_habr()

if __name__ =='__main__':
    main()
