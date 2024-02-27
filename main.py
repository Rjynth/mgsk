import requests
import json


def get_vacancies(keyword):
    url = "https://api.hh.ru/vacancies"


    areas = [1, 2]

    all_vacancies = []

    for area in areas:
        params = {
            "text": keyword,
            "area": area,
            "per_page": 100,
        }
        headers = {
            "User-Agent": "Your User Agent",
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("items", [])
            for vacancy in vacancies:

                title_element = vacancy.get("name").lower()
                if 'django' or 'flask' in title_element:
                    vacancy_id = vacancy.get("id")
                    vacancy_url = vacancy.get("alternate_url")
                    company_name = vacancy.get("employer", {}).get("name")
                    city = vacancy.get("area", {}).get("name")
                    salary = vacancy.get("salary")
                    if salary:
                        salary_from = salary.get("from")
                        salary_to = salary.get("to")
                        salary_currency = salary.get("currency")
                    else:
                        salary_from = salary_to = salary_currency = None

                    all_vacancies.append({
                        'id': vacancy_id,
                        'title': title_element,
                        'company': company_name,
                        'city': city,
                        'salary_from': salary_from,
                        'salary_to': salary_to,
                        'salary_currency': salary_currency,
                        'url': vacancy_url
                    })
        else:
            print(f"Request failed with status code: {response.status_code}")

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(all_vacancies, f, ensure_ascii=False, indent=4)


get_vacancies("python developer")
