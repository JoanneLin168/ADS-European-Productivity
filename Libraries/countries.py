from bs4 import BeautifulSoup
import requests

print("This may take some time...")

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

def convert_iso_2_to_3(iso_2):
    return iso_2_to_3_map[iso_2]

def convert_iso_3_to_2(iso_3):
    return iso_3_to_2_map[iso_3]

def get_iso_2_list():
    return list(iso_2_to_3_map.keys())

def get_iso_3_list():
    return list(iso_3_to_2_map.keys())