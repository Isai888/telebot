import requests
import json
from config import API_KEY, currencies


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_convert(curr_from, curr_to, amount):
        try:
            curr_from_key = currencies[curr_from]
        except KeyError:
            raise APIException(f'Валюта {curr_from} не найдена!\nСписок доступных валют см. /values')
        try:
            curr_to_key = currencies[curr_to]
        except KeyError:
            raise APIException(f'Валюта {curr_to} не найдена!\nСписок доступных валют см. /values')
        if curr_from_key == curr_to_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {curr_from}')
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        url = f"https://min-api.cryptocompare.com/data/price?fsym={curr_from_key}&tsyms={curr_to_key}"

        headers = {"Authorization": f"Apikey {API_KEY}"}
        r = requests.get(url, headers=headers)
        resp = json.loads(r.content)
        result = resp[curr_to_key]
        return round(result * amount, 3)
