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

    europe = [
        'Austria',
        'Belgium',
        'Bulgaria',
        'Croatia',
        'Czechia',
        'Denmark',
        'Estonia',
        'Finland',
        'France',
        'Germany',
        'Greece',
        'Hungary',
        'Iceland',
        'Ireland',
        'Italy',
        'Latvia',
        'Lithuania',
        'Luxembourg',
        'Netherlands',
        'Norway',
        'Poland',
        'Portugal',
        'Romania',
        'Slovakia',
        'Slovenia',
        'Spain',
        'Sweden',
        'Switzerland',
        'Turkey-Turkiye',
        'United-Kingdom'
    ]

    # Get country ata
    subregions = {}
    countries_url = "https://www.cia.gov/the-world-factbook/countries/"
    for i, country in enumerate(europe):
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

        if country == "Turkey-Turkiye":
            country = "Turkey"
            subregion = "Southeastern Europe"

        if country == "United-Kingdom":
            country = "United Kingdom"

        europe[i] = country

        if subregion not in subregions.keys():
            subregions[subregion] = []
        subregions[subregion].append(country)

    # ISO codes
    print("Getting ISO data...")
    url = "https://www.iban.com/country-codes"
    req = requests.get(url)
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')

    rows = soup.find_all('tr')
    rows = rows[1:] # Remove the first row (header)

    alpha_2_list = []
    alpha_3_list = []
    europe_tmp = europe.copy()

    for row in rows:
        row = row.find_all('td')
        country = row[0].text
        alpha2 = row[1].text
        alpha3 = row[2].text

        if country == "Czechia":
            country = "Czech Republic"
        
        for i in range(len(europe)):
            if country in europe[i] or europe[i] in country:
                alpha_2_to_3_map[alpha2] = alpha3
                alpha_3_to_2_map[alpha3] = alpha2
                alpha_2_list.append(alpha2)
                alpha_3_list.append(alpha3)
                break

    # Countries
    countries = {}
    for i in range(len(europe)):
        country = europe[i]
        alpha2 = alpha_2_list[i]
        alpha3 = alpha_3_list[i]
        subregion = get_subregion(country)
        countries[country] = Country(country, alpha2, alpha3, subregion)

    # Save to csv
    print("Saving to csv...")
    global csvfile
    with open(csvfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Country', 'Alpha-2', 'Alpha-3', 'Subregion'])
        for country in countries.keys():
            writer.writerow([country, countries[country].alpha2, countries[country].alpha3, countries[country].subregion])

#################### MAIN ####################
# Check if countries.csv exists, if it does, build variables from it
# if not webscrape() and build variables from webscraping
if __name__ == '__main__':
    csvfile = 'Libraries/countries.csv'
else:
    csvfile = '../Libraries/countries.csv'
try:
    with open(csvfile, 'r') as csvfile:
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