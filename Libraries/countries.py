from bs4 import BeautifulSoup
import requests
import csv

alpha_2_to_3_map = {}
alpha_3_to_2_map = {}
countries = {}
subregions = {}

#################### FUNCTIONS ####################
# Alpha-2 and alpha-3
def convert_alpha_2_to_3(alpha2):
    return alpha_2_to_3_map[alpha2]

def convert_alpha_3_to_2(alpha3):
    return alpha_3_to_2_map[alpha3]

def get_alpha_2_list():
    return list(alpha_2_to_3_map.keys())

def get_alpha_3_list():
    return list(alpha_3_to_2_map.keys())

# Europe subregions
def get_subregion(country):
    for subregion in subregions.keys():
        if country in subregions[subregion]:
            return subregion
    return None

def get_subregions():
    return list(subregions.keys())

def get_subregions_data():
    return subregions

def get_countries_in_subregion(subregion):
    return subregions[subregion]

# Countries
def get_countries():
    return list(countries.keys())

def get_country_data(country): # Note: this returns a Country object
    return countries[country]

#################### CLASSES ####################
class Country:
    def __init__(self, name, alpha2, alpha3, subregion):
        self.name = name
        self.alpha2 = alpha2
        self.alpha3 = alpha3
        self.subregion = subregion

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

#################### WEBCRAWLING/WEBSCRAPING ####################
# Europe subregions
def webscrape():
    # Use global variables
    global alpha_2_to_3_map
    global alpha_3_to_2_map
    global countries
    global subregions

    # Get data
    print("Getting Europe subregions...")
    url_list = "https://www.cia.gov/the-world-factbook/field/location/"
    req = requests.get(url_list)
    source = req.text
    soup_list = BeautifulSoup(source, 'html.parser')

    url_eu = "https://www.cia.gov/the-world-factbook/countries/european-union/"
    req = requests.get(url_eu)
    source = req.text
    soup_eu = BeautifulSoup(source, 'html.parser')

    countries_eu_div = soup_eu.find('div', attrs={
        'class': 'category_data'
    })
    countries_eu = countries_eu_div.find_all('li')
    countries_eu = sorted([country.text.split(' - ')[0] for country in countries_eu])

    subregions = {}
    countries_url = "https://www.cia.gov/the-world-factbook/countries/"
    for country in countries_eu:
        country_url = countries_url+country.lower()
        req = requests.get(country_url)
        source = req.text
        soup_country = BeautifulSoup(source, 'html.parser')
        geography_div = soup_country.find('div', attrs={
            'id': 'geography'
        })
        location_data = geography_div.find_all('p')[0].text # Find the data from the first <p> element
        subregion = location_data.split(',')[0]
        if ':' in subregion: # To avoid problems with France
            subregion = subregion.split(': ')[1]
        elif country == 'Slovenia':
            subregion = 'Central Europe'

        if country == "Czechia":
            country = "Czech Republic"

        if subregion not in subregions.keys():
            subregions[subregion] = []
        subregions[subregion].append(country)

    # ISO codes
    print("Getting ISO data...")
    url = "https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=141329"
    req = requests.get(url)
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')

    alpha_2_elmts = soup.find_all('td', attrs={
        'headers': 'un_3'
    })

    alpha_3_elmts = soup.find_all('td', attrs={
        'headers': 'un_4'
    })

    N = len(alpha_2_elmts)
    alpha_2_to_3_map = {}
    alpha_3_to_2_map = {}
    for i in range(N):
        alpha_2_to_3_map[alpha_2_elmts[i].text] = alpha_3_elmts[i].text
        alpha_3_to_2_map[alpha_3_elmts[i].text] = alpha_2_elmts[i].text

    # Countries
    countries_eu = [country.replace('Czechia', 'Czech Republic') for country in countries_eu]
    countries = {}
    for i in range(len(countries_eu)):
        country = countries_eu[i]
        alpha2 = alpha_2_elmts[i].text
        alpha3 = alpha_3_elmts[i].text
        subregion = get_subregion(country)
        countries[country] = Country(country, alpha2, alpha3, subregion)

    # Save to csv
    print("Saving to csv...")
    with open('Libraries/countries.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Country', 'Alpha-2', 'Alpha-3', 'Subregion'])
        for country in countries.keys():
            writer.writerow([country, countries[country].alpha2, countries[country].alpha3, countries[country].subregion])

#################### MAIN ####################
# Check if countries.csv exists, if it does, build variables from it
# if not webscrape() and build variables from webscraping
try:
    with open('Libraries/countries.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) # Skip header
        for row in reader:
            country = row[0]
            alpha2 = row[1]
            alpha3 = row[2]
            subregion = row[3]
            countries[country] = Country(country, alpha2, alpha3, subregion)
            alpha_2_to_3_map[alpha2] = alpha3
            alpha_3_to_2_map[alpha3] = alpha2
            if subregion not in subregions.keys():
                subregions[subregion] = []
            subregions[subregion].append(country)
except FileNotFoundError:
    print("countries.csv not found, webscraping...")
    webscrape()

if __name__ == "__main__":
    print(countries)
    print(subregions)