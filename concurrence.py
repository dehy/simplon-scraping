import requests
from bs4 import BeautifulSoup
from pyexcel_ods3 import save_data
import datetime

# We will store all items in this List
items = [["Type", "Name", "Price"]]

# We found that all categories had the same base url
base_url = "https://www.webscraper.io/test-sites/e-commerce/allinone"

for page_url in ["/computers/laptops", "/computers/tablets", "/phones/touch"]:
    # We concatenate base_url with the pages urls
    url = f"{base_url}{page_url}"
    response = requests.get(url)
    if (response.status_code != 200):
        print(f"Page not fetched correcly. Code {response.status_code}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    items_soup = soup.find_all('a', {'class': 'title'})
    for item_soup in items_soup:
        item = []
        item.append(page_url)

        name = item_soup['title']
        item.append(name)

        price_soup = item_soup.parent.previous_sibling.previous_sibling
        price = price_soup.string[1:]
        item.append(price)

        items.append(item)

now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
filename = f"concurrence-{now}.ods"
save_data(filename, {'Feuille 1': items})
print(f'Ding ! Le fichier Spreadsheet est prêt ! ./{filename}')
