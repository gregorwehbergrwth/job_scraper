from functions.content_scraper import *
from functions.extract import *
from functions.handling import *
from functions.frequency import *

url = "https://www.wg-gesucht.de/wg-zimmer-in-Aachen.1.0.1.0.html?offer_filter=1&city_id=1&sort_order=0&noDeact=1&categories%5B%5D=0&rMax=500"

with open("wg_gesucht_page.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')

posts = soup.find_all('div', {'class': 'wgg_card offer_list_item'})

data = []
for script in posts:

    try:
        data.append(json.loads(script.string))
    except json.JSONDecodeError:
        print("jsondecodeerror")
        pass

collection_page = next(
    item for item in data if item.get("@type") == "CollectionPage"
)

print(collection_page["name"])
print(collection_page["description"])
print(collection_page["publisher"]["legalName"])
