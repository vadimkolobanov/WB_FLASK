import requests
from retry import retry

# Парсер функции
def get_catalogs_wb() -> dict:
    url = 'https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v2.json'
    headers = {'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    return requests.get(url, headers=headers).json()

def get_data_category(catalogs_wb: dict) -> list:
    catalog_data = []
    if isinstance(catalogs_wb, dict) and 'childs' not in catalogs_wb:
        catalog_data.append({
            'name': f"{catalogs_wb['name']}",
            'shard': catalogs_wb.get('shard', None),
            'url': catalogs_wb['url'],
            'query': catalogs_wb.get('query', None)
        })
    elif isinstance(catalogs_wb, dict):
        catalog_data.extend(get_data_category(catalogs_wb['childs']))
    else:
        for child in catalogs_wb:
            catalog_data.extend(get_data_category(child))
    return catalog_data

def get_data_from_json(json_file: dict) -> list:
    data_list = []
    for data in json_file['data']['products']:
        data_list.append({
            'id': data.get('id'),
            'name': data.get('name'),
            'price': int(data.get("priceU") / 100),
            'salePriceU': int(data.get('salePriceU') / 100),
            'sale': data.get('sale'),
            'brand': data.get('brand'),
            'rating': data.get('rating'),
            'feedbacks': data.get('feedbacks'),
            'reviewRating': data.get('reviewRating'),
            'link': f'https://www.wildberries.ru/catalog/{data.get("id")}/detail.aspx?targetUrl=BP'
        })
    return data_list

@retry(Exception, tries=5, delay=2)
def scrap_page(page: int, shard: str, query: str, low_price: int, top_price: int, discount: int = None) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.wildberries.ru",
        'Content-Type': 'application/json; charset=utf-8',
        'Transfer-Encoding': 'chunked',
        "Connection": "keep-alive",
        'Vary': 'Accept-Encoding',
        'Content-Encoding': 'gzip',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }
    url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub' \
          f'&dest=-1257786' \
          f'&locale=ru' \
          f'&page={page}' \
          f'&priceU={low_price * 100};{top_price * 100}' \
          f'&sort=popular&spp=0' \
          f'&{query}' \
          f'&discount={discount}'
    r = requests.get(url, headers=headers)
    print(f'Статус: {r.status_code} Страница {page} Идет сбор...')
    return r.json()
