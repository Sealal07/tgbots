import requests
from bs4 import BeautifulSoup
from database import SessionLocal, Brand, Car

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

def get_cars(brand_name=''):
    db = SessionLocal()
    url = f'https://auto.drom.ru/{brand_name.lower() if brand_name else ''}'
    try:
        brand = db.query(Brand).filter(Brand.name == brand_name).first()
        if not brand:
            brand = Brand(name=brand_name if brand_name else 'Все марки')
            db.add(brand)
            db.commit()
            db.refresh(brand)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cars = soup.find_all('a', {'data-ftid': 'bull_title'}) or \
               soup.select('a[class*="css-"]')
        results = []
        for car in cars[:10]:
            car_data = parse_car_data(car)
            if not car_data:
                continue
            existing_car = db.query(Car).filter(Car.link == car_data['link']).first()
            if not existing_car:
                new_car = Car(
                    title=car_data['title'],
                    price=car_data['price'],
                    params=car_data['params'],
                    link=car_data['link'],
                    brand_id=brand.id
                )
                db.add(new_car)
            results.append(car_data)
        db.commit()
        return results
    except Exception as e:
        print(f'Ошибка парсинга или БД {e}')
        return []
    finally:
        db.close()

def parse_car_data(car_link_elem):
    try:
        link = car_link_elem.get('href')
        title = car_link_elem.text.strip()
        parent = car_link_elem.find_parent('div').find_parent('div')
        price_elem = parent.find_parent('div').find('span', {'data-ftid': 'bull_price'})
        price = price_elem.text.replace('\xa0', ' ') if price_elem else "Цена не указана"
        desc_elem = parent.find('div', {'data-ftid': 'component_inline-bull-description'})
        params = desc_elem.text.strip() if desc_elem else 'Параметры не указаны'
        return {
            'title': title,
            'price': price,
            'params': params,
            'link': link
        }
    except Exception as e:
        print(f'ошибка при разборе элемента {e}')
        return None