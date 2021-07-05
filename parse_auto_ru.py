import requests
import re


def parse_auto_ru(mark, model):

    url = 'https://auto.ru/-/ajax/desktop/listing/'
    mark = mark.upper()
    model = model.upper()

    params = {
        'catalog_filter': [{'mark': mark, 'model': model}],
        'section': 'new',  # "all",
        # 'category': 'cars',
        # 'sort': 'fresh_relevance_1-desc',
        'page': 1
    }

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Content-Length': '137',
        'content-type': 'application/json',
        'Cookie': '_csrf_token=1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24; autoru_sid=a%3Ag5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270%7C1580931467355.604800.8HnYnADZ6dSuzP1gctE0Fw.cd59AHgDSjoJxSYHCHfDUoj-f2orbR5pKj6U0ddu1G4; autoruuid=g5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270; suid=48a075680eac323f3f9ad5304157467a.bc50c5bde34519f174ccdba0bd791787; from_lifetime=1580933172327; from=yandex; X-Vertis-DC=myt; crookie=bp+bI7U7P7sm6q0mpUwAgWZrbzx3jePMKp8OPHqMwu9FdPseXCTs3bUqyAjp1fRRTDJ9Z5RZEdQLKToDLIpc7dWxb90=; cmtchd=MTU4MDkzMTQ3MjU0NQ==; yandexuid=1758388111580931457; bltsr=1; navigation_promo_seen-recalls=true',
        'Host': 'auto.ru',
        'origin': 'https://auto.ru',
        'Referer': 'https://auto.ru/moskva/cars',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'x-client-app-version': '202002.03.092255',
        'x-client-date': '1580933207763',
        'x-csrf-token': '1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24',
        'x-page-request-id': '60142cd4f0c0edf51f96fd0134c6f02a',
        'x-requested-with': 'fetch'
    }

    req = requests.post(url, json=params, headers=headers)  # Делаем post запрос на url
    data = req.json()['offers']  # Переменная data хранит полученные объявления

    car_list = []

    for i in data[:5]:
        mark = i['vehicle_info']['mark_info']['name']
        model = i['vehicle_info']['model_info']['name']
        #price = i['price_info']['price']
        price = re.sub('(\d)(?=(\d{3})+(?!\d))', r'\1,', '%d' % i['price_info']['price'])
        year = i['documents']['year']
        complectation = i['vehicle_info']['complectation']['name']
        dealer = i['seller']['name']
        region = i['seller']['location']['region_info']['name']

        try:
            discount = re.sub('(\d)(?=(\d{3})+(?!\d))', r'\1,', '%d' % i['discount_options']['max_discount'])
        except KeyError:
            discount = 'Нет'

        car_list.append({
            'mark': str(mark),
            'model': str(model),
            'price': str(price),
            'year': str(year),
            'complectation': str(complectation),
            'dealer': str(dealer),
            'region': str(region),
            'discount': str(discount)
        })

    return car_list


# print(parse_auto_ru('kia', 'rio'))