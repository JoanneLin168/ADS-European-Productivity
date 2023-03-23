from bs4 import BeautifulSoup
import requests

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

#################### WEBSCRAPING ####################
# Countries, alpha-2 and alpha-3
print("Getting countries data...")
url = "https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=141329"
req = requests.get(url)
source = req.text
soup = BeautifulSoup(source, 'html.parser')

countries_elmts = soup.find_all('td', attrs={
    'headers': 'un_2'
})

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

# Europe subregions
print("Getting Europe subregions...")
url = "https://www.worldometers.info/population/europe/"
req = requests.get(url)
source = req.text
soup = BeautifulSoup(source, 'html.parser')

subregions_columns = soup.find_all('div', attrs={
    'class': 'col-md-6 noli'
})

subregions = {}
for col in subregions_columns:
    elmts = col.find_all('a')
    subregion_elmt = elmts[0]
    countries_elmt = elmts[1:]
    
    subregion = subregion_elmt.text
    subregions[subregion] = []
    for country_elmt in countries_elmt:
        country = country_elmt.text
        subregions[subregion].append(country)

# Countries
countries = {}
for i in range(N):
    country = countries_elmts[i].text
    alpha2 = alpha_2_elmts[i].text
    alpha3 = alpha_3_elmts[i].text
    if country == 'Ireland, Republic of (EIRE)':
        country = 'Ireland'
    subregion = get_subregion(country)
    countries[country] = Country(country, alpha2, alpha3, subregion)

print("Countries data loaded.")