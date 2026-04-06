import requests
from bs4 import BeautifulSoup
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_city(address):
    match = re.search(r"\d{2}-\d{3}\s+(.+)", address)
    if match:
        return match.group(1).strip()
    return None

def get_cf_data():

    cf_data = []
    cf_all_cities = requests.get('https://cityfit.pl/nasze-kluby/')
    cf_all_cities_doc = BeautifulSoup(cf_all_cities.text, 'html.parser')
    for city in cf_all_cities_doc.select('div.our-clubs__item'):
        cf_data.append({
            'address': city['data-address'],
            'lat': city['data-lat'],
            'lng': city['data-lng'],
            'open_hours': '24/7',
            'gym': 'CityFit',
            'city': extract_city(city['data-address'])
        })
    return cf_data

cf_data = get_cf_data()

def get_zf_data():

    zf_all_cities = requests.get('https://zdrofit.pl/kluby-fitness')
    zf_all_cities_doc = BeautifulSoup(zf_all_cities.text, 'html.parser')
    zf_links = []
    zf_data = []

    for city in zf_all_cities_doc.select('section ul li div'):
        if city.find('small', string='Wkrótce otwarcie') or city.find('small', string='Wkrótce otwarcie / karnety "plus"') or city.find('small', string='Klub tymczasowo zamknięty"'):
            pass
        else: zf_links.append("https://zdrofit.pl" + city.find('a')['href'])
    
    for link in zf_links:
        open_hours_ls = []
        zf_club = requests.get(link)
        zf_club_doc = BeautifulSoup(zf_club.text, 'html.parser')
        if zf_club_doc.find('h4', string="Godziny otwarcia").parent.find('p'):
            open_hours_ls.append('24/7')
        else:
            open_hours = zf_club_doc.find('h4', string="Godziny otwarcia").parent.find_all('dd')
            if len(open_hours) == 1:
                one_open_hours = zf_club_doc.find('h4', string="Godziny otwarcia").parent.find('dd')
                open_hours_ls.append(one_open_hours.text.strip())        
            else:
                one_open_hours = zf_club_doc.find('h4', string="Godziny otwarcia").parent.find('dd')
                open_hours_ls.append(one_open_hours.text.strip())
                two_open_hours = one_open_hours.find_next('dd')
                open_hours_ls.append(two_open_hours.text.strip()) 
        address = zf_club_doc.find('address').get_text(separator=' ', strip=True)
        lat = zf_all_cities_doc.find('a', href=link.removeprefix('https://zdrofit.pl')).parent.parent.get('data-lat')
        lng = zf_all_cities_doc.find('a', href=link.removeprefix('https://zdrofit.pl')).parent.parent.get('data-lng')
        city = zf_all_cities_doc.find('a', href=link.removeprefix('https://zdrofit.pl')).parent.parent.get('data-city')
        zf_data.append({
            'address': address,
            'lat': lat,
            'lng': lng,
            'open_hours': open_hours_ls,
            'gym': 'ZdroFit',
            'city': city.replace("_", " ")
        })

    return zf_data

zf_data = get_zf_data()

data = pd.DataFrame(cf_data + zf_data)
data = data.to_dict(orient='records')

@app.get("/data")
def get_data():
    return data
