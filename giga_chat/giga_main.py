from config import SBER_AUTH_KEY
from gigachat import GigaChat

"""
Часть кода отвечающая за формирование запроса к gigachat
формирует запрос из:
    - сообщение пользователя
    - файл с данными о проектах
    - промт задающий поведение нейронной сети
"""


def giga_message_response(message: str) -> str:
    giga = GigaChat(
        credentials=f"{SBER_AUTH_KEY}",
        verify_ssl_certs=False,
    )
    with open('files/data.txt', 'r', encoding="utf-8") as file:
        data = file.read()

    SYSTEM_PROMPT = f"""
            Ты — ассистент компании. Отвечаешь ТОЛЬКО на основе приложенного документа. 
            Правила:
            файл - {data}
            запрос пользователя - {message}
            1. Если вопрос не относится к документу — отвечай: "Это вне моей компетенции".
            2. Будь вежливым, но лаконичным.
            3. Не выдумывай факты.
            4. Цитируй разделы документа при ответе.
            5. Для расчетов используй только данные из файла.
            6. Вставь 1-2 ссылки на проекты которые лежат в файле, если того требует клиент
            7. Не упоминай никакой документ, говори будто ты человек
            8. Ответ не должен превышать 350 символов
        """
    response = giga.chat(SYSTEM_PROMPT)
    answer = response.choices[0].message.content
    print(response.choices[0].message.content)
    return answer
