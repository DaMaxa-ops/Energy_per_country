import requests
import json
import csv

def get_energy_consumption():
    country_code = input("Введите код страны (например, US, RU, CN): ").upper()
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/EG.USE.PCAP.KG.OE?format=json&per_page=1000"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if len(data) > 1 and isinstance(data[1], list):
            all_years = [item['date'] for item in data[1] if item.get('value') is not None]
            print(f"{country_code}: {all_years}\n")

            year = int(input("Введите год из списка: "))
            records = []

            for item in data[1]:
                item_year = int(item['date'])
                value = item['value']

                if item_year == year:
                    record = {
                        "country": country_code,
                        "year": item['date'],
                        "energy_consumption": item['value'],
                        "unit": "kg of oil equivalent per capita"
                    }
                    records.append(record)

            if records:
                for record in records:
                    print(record)

                filename = f"{country_code}_energy_{year}.csv"
                with open(filename, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=records[0].keys())
                    writer.writeheader()
                    writer.writerows(records)

                print(f"Данные сохранены в файл: {filename}")


get_energy_consumption()
