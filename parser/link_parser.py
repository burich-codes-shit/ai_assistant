import random
import time
from requests import Session
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import logging


"""
Пожалуй самая интересная часть когда, которая отвечает
за парсинг информации со страниц проектов компании EORA
для удобства отслеживания работы скрипта было использовано логирование
Также для обхода защиты сайта от парсеров использовал 
    - fake_useragent
    - задержку между запросами
    - прокси сервер
"""
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def link_parser():
    session = Session()

    # Настройка адаптера с повторными попытками
    adapter = HTTPAdapter(
        max_retries=3,
        pool_connections=10,
        pool_maxsize=10
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        with open('../files/links.txt', 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logger.error("Файл links.txt не найден")
        return

    for url in urls:
        try:
            ua = UserAgent()
            # Генерируем новые заголовки для каждого запроса
            headers = {
                "User-Agent": ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Connection": "keep-alive"
            }
            proxies = {
                "http": "http://177.234.224.75:3128",
                "https": "http://177.234.224.75:3128"
            }

            # Добавляем случайную задержку
            delay = random.uniform(1.5, 4.0)
            time.sleep(delay)

            logger.info(f"Обрабатываю URL: {url}")

            response = session.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=10
            )

            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, 'html.parser')
            meta_desc = soup.find('meta', attrs={'name': 'description'})

            if meta_desc:
                data_frame = meta_desc.get('content')
                logger.info(f"Найдено описание: {data_frame[:50]}...")

                # Записываем в файл с добавлением
                with open('../files/tester.txt', 'a', encoding='utf-8') as file:
                    file.write(f"{url}|{data_frame}\n")

                logger.info(f'Успешно спарсил - {url}\n')
            else:
                logger.warning(f"Мета-описание не найдено для {url}")

        except Exception as e:
            logger.error(f"Ошибка при обработке {url}: {str(e)}")
            continue

link_parser()



