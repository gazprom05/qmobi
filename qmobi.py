import requests
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string.encode(encoding='utf_8'))



def get_api():
    get_xml = requests.get(
        'https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=4144e47adc138e225437493b8bc21b73')
    if get_xml.status_code == 200:
        print('Все в норме! 200')
    if get_xml.status_code == 404:
        print('Страница не существует! 404')

    response = json.loads(get_xml.text)
    usd = response['data']['USDRUB']
    return usd


try:
    full_rate = float(get_api())
    rate = round(full_rate, 2)

    try:
        quantity_usd = int(input('Введите сумму в долларах для конвертации в рубли'))
    except ValueError:
        quantity_usd = 1
        print('Ошибка формата ввода. В расчёт подставлена единица.')

    if quantity_usd < 1:
        quantity_usd = 1
        print('Ошибка формата ввода. В расчёт подставлена единица.')
    quantity_rub = quantity_usd * rate
    print(f'Дата: {time.strftime("%d.%m.%y")}. Время: {time.strftime("%X")}. Курс рубля к доллару {full_rate}:1.'
          f' При обмене {quantity_usd} долларов вы получите {int(quantity_rub)} руб. '
          f'{int(quantity_rub % int(quantity_rub) * 100)} коп.')

    message = {
        "Exchange": {
            "Currency_1": "USD",
            "Currency_2": "RUB",
            "Quantity": quantity_usd,
            "Result": quantity_rub,
            "Date": time.strftime("%d.%m.%y"),
            "Time": time.strftime("%X"),
        }
    }

except Exception:
    print('Не удалось достать информацию о курсе')
    message = {
        "Error": "We couldn’t get the dollar rate data. Also, we couldn’t write this text in Russian"
    }

json_string = json.dumps(message)
httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()









