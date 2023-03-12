import platform
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import asyncio
import aiohttp
import schedule

from loader import db

ua = UserAgent()
headers = {'user-agent': ua.firefox}


async def get_page_data(session, page, headers):
    url = f'https://codeforces.com/problemset/page/{page}?order=BY_SOLVED_DESC&locale=ru'

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        response_text = ''.join(line.strip() for line in response_text.split("\n"))

        soup = bs(response_text, 'html.parser')

        for task in soup.find('table', class_='problems').find_all('tr')[1:]:
            themes = task.find_all('td')[1].find(
                'div', style='float: right; font-size: 1.1rem; padding-top: 1px; text-align: right;').text.strip()
            amount_of_decided = task.find_all('td')[4].text.strip()
            name = task.find_all('td')[1].find(
                'div', style='float: left;').text.strip()
            number = task.find_all('td')[0].text.strip()
            name_and_number = f'{name} + {number}'
            complexity = task.find_all('td')[3].text.strip()

            db.add_row(themes, amount_of_decided,
                       name_and_number, complexity)


async def gather_data(url, headers):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)

        response_text = await response.text()
        response_text = ''.join(line.strip() for line in response_text.split("\n"))

        soup = bs(response_text, 'html.parser')

        pages_amount = int(
            soup.find('div', class_='pagination').find_all('li')[-2].text)

        tasks = []

        for page in range(1, pages_amount + 1):
            task = asyncio.create_task(get_page_data(session, page, headers))
            tasks.append(task)

        await asyncio.gather(*tasks)


def start():
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(gather_data(
        'https://codeforces.com/problemset/page/1?order=BY_SOLVED_DESC&locale=ru', headers))
    
    db.close_connection()
    print('Parsing finished')


if __name__ == '__main__':
    start()

    schedule.every().hour.do(start)

    while True:
        schedule.run_pending()
        time.sleep(1)
