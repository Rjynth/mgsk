import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json


def get_headers():
    return Headers(browser='chrome', os='win').generate()


url = 'https://hh.ru/search/vacancy'
params = {
    'area': (1, 2),
    'text': 'Flask, Django',
    'page': 0,
    'items_on_page': 20
}
parsed_data = []
pages_to_check = 10

while params['page'] < pages_to_check:
    hh_html = requests.get(url=url, params=params, headers=get_headers()).text
    hh_soup = BeautifulSoup(hh_html, 'lxml')
    tag_content = hh_soup.find('div', id='a11y-main-content')

    if tag_content is None:
        break

    div_item_tags = tag_content.find_all('div', class_='serp-item')

    for div_item_tag in div_item_tags:
        vacancy = div_item_tag.find('h3')
        link = vacancy.find('a').get('href')
        if div_item_tag.find('span', class_='bloko-header-section-2') is not None:
            salary = div_item_tag.find('span', class_='bloko-header-section-2').text
        else:
            salary = "Не указана"
        company = div_item_tag.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', '')
        city = div_item_tag.find('div', class_='vacancy-serp-item__info').contents[1].contents[0]
        parsed_data.append(
            {
                "Вакансия": vacancy.text,
                "Ссылка": link,
                "Зарплата": salary,
                "Название компании": company,
                "Город": city
            }
        )

    params['page'] += 1

with open('final_parced.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=5)