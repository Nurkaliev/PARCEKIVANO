import requests
import csv
from bs4 import BeautifulSoup
URL = 'https://www.kivano.kg/noutbuki'
CSV = 'kivano_noutbuki.csv'
HOST = 'https://www.kivano.kg/'
HEADERS = {
    'user_agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
}
def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params, verify=False)
    return r
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    i = soup.findAll('div', class_="item product_listbox oh")
    laptops = []
    for item in i:
        laptops.append({
            'название' : item.find('div', class_='listbox_title oh').get_text(),
            'описание' : str(item.find('div', class_='product_text pull-left').get_text()).split('\n')[-1],
            'фото' : 'https://kivano.kg' + item.find('img').get_text('src'),
            'цена': item.find('div', class_='listbox_price text-center').get_text(),
            'подробнее': item.find('div', class_='listbox_title oh').find('a').get('href'),
            'наличие': item.find('div', class_='listbox_motive text-center').get_text()
        })
    return laptops
def save(i, path):
    with open('path.csv', 'w') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['название', 'описание', 'фото', 'цена', 'подробнее', 'наличие'])
        for item in i:
            writer.writerow([item['название'], item['описание'], item['фото'], item['цена'], item['подробнее'], item['наличие']])
def parser():
    pagenation = int(input('введите номер страницы: ').strip())
    html = get_html(URL)
    if html.status_code == 200:
        new_list = []
        for page in range(1, pagenation+1):
            print(f'страница{page}готова')
            html = get_html(URL, params={'page': page})
            new_list.extend(get_content(html.text))
        save(new_list, CSV)
        print('завершено')
    else:
        print('нет соединении')
if __name__ == '__main__':
    parser()
