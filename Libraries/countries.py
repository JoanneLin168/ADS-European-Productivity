from bs4 import BeautifulSoup
import requests

############################################################################
def convert_iso_2_to_3(iso_2):
    return iso_2_to_3_map[iso_2]

def convert_iso_3_to_2(iso_3):
    return iso_3_to_2_map[iso_3]

def get_iso_2_list():
    return list(iso_2_to_3_map.keys())

def get_iso_3_list():
    return list(iso_3_to_2_map.keys())

############################################################################
# Get ISO-2 and ISO-3 data
print("Getting ISO-2 and ISO-3 data...")
url = "https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=141329"
req = requests.get(url)
source = req.text
soup = BeautifulSoup(source, 'html.parser')

iso_2_elmts = soup.find_all('td', attrs={
    'headers': 'un_3'
})

iso_3_elmts = soup.find_all('td', attrs={
    'headers': 'un_4'
})

N = len(iso_2_elmts)
iso_2_to_3_map = {}
iso_3_to_2_map = {}
for i in range(N):
    iso_2_to_3_map[iso_2_elmts[i].text] = iso_3_elmts[i].text
    iso_3_to_2_map[iso_3_elmts[i].text] = iso_2_elmts[i].text


# Get Europe subregions
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