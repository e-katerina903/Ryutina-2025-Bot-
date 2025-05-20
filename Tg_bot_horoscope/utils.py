import requests

def get_daily_horoscope(sign: str, day: str) -> dict:
    """
    Получает ежедневный гороскоп для указанного знака зодиака и дня.

    :param sign: Знак зодиака (например, 'Aries', 'Taurus')
    :param day: День ('today', 'tomorrow', 'yesterday' или дата в формате 'YYYY-MM-DD')
    :return: Словарь с данными гороскопа
    """
    url = f"https://aztro.sameerkumar.website/?sign={sign}&day={day}"
    response = requests.post(url)
    if response.status_code == 200:
        return {"data": response.json()}
    else:
        raise Exception(f"Ошибка при получении гороскопа: {response.status_code}")
