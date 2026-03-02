import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

url = "https://auto.drom.ru/toyota/"


def parse_drom():
    try:
        response = requests.get(url, headers=headers)
        # response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        cars = soup.find_all('a', {'data-ftid': 'bull_title'}) or \
               soup.select('a[class*="css-"]')

        for car in cars[:5]:
            try:
                link = car.get('href')
                title = car.find('span', {'data-ftid': 'bull_title'}).text.strip() if car.find('span', {
                    'data-ftid': 'bull_title'}) else car.text.strip()

                parent = car.find_parent('div')
                grand_parent = parent.find_parent('div') if parent else None

                price_elem = None
                if grand_parent:
                    price_elem = grand_parent.find('span', {'data-ftid': 'bull_price'})

                price = price_elem.text.replace('&nbsp;', ' ') if price_elem else "Цена не указана"

                desc_elem = None
                if grand_parent:
                    desc_elem = grand_parent.find('div', {'data-ftid': 'component_inline-bull-description'})

                description = desc_elem.text.strip() if desc_elem else "Описание не найдено"

                print(title)
                print(price)
                print(description)
                print(link)

            except Exception as e:
                print(f"Ошибка: {e}")
                continue

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    parse_drom()