from functions.content_scraper import *
from functions.extract import *
from functions.handling import *
from functions.frequency import *



# link = "https://www.wg-gesucht.de/wg-zimmer-in-Aachen.1.0.1.0.html"
url = "https://www.wg-gesucht.de/wg-zimmer-in-Aachen.1.0.1.0.html?offer_filter=1&city_id=1&sort_order=0&noDeact=1&categories%5B%5D=0&rMax=500"

# response = requests.get(url)
# html = response.text
# print("-_"*100)
# print(html)
# print("-_"*100)

# save to file
# with open("wg_gesucht_page.html", "w", encoding="utf-8") as file:
#     file.write(html)

with open("wg_gesucht_page.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')

# print("-_"*100)
# print(soup)
# print("-_"*100)


posts = soup.find_all('div', {'class': 'wgg_card offer_list_item'})

# for post in posts:

    # print("-_" * 50)
    # print(post.text.strip())
    # print("-_" * 50)
    #
    #
    # import requests
    # import json
    # from bs4 import BeautifulSoup

# url = "https://www.wg-gesucht.de/wg-zimmer-in-Aachen.1.0.1.0.html"
#
# html = requests.get(url, timeout=10).text
# soup = BeautifulSoup(html, "html.parser")
#
# scripts = soup.find_all("script", type="application/ld+json")
# print(len(scripts))
data = []
for script in posts:
    try:
        data.append(json.loads(script.string))
    except json.JSONDecodeError:
        print("jsondecodeerror")
        pass

# Example: filter for CollectionPage
collection_page = next(
    item for item in data if item.get("@type") == "CollectionPage"
)

print(collection_page["name"])
print(collection_page["description"])
print(collection_page["publisher"]["legalName"])

#
#
#     # try:
#     title = post.find('h3', {'class': 'truncate_title noprint'}).text.strip()
#     print(title)
#     size = post.find('div', {'class': 'col-xs-3 text-right'}).text.strip()
#     print(size)
#     price = post.find('div', {'class': 'col-xs-3'}).text.strip()
#     print(price)
#     flatmate = post.find('span', {'class': 'noprint'}).attrs.get('title', '').strip()
#     print(flatmate)
#     available = post.find('div', {'class': 'col-xs-5 text-center'}).text.strip()
#     print(available)
#     available = ' '.join(available.split())
#     print(available)
#
#     # Get link
#     h3 = post.find('h3', {'class': 'truncate_title noprint'})
#     a_tag = h3.find('a')
#     href = a_tag.get('href')
#     link = "https://www.wg-gesucht.de" + href
#
#     # Get address
#     div = post.find('div', {'class': 'col-xs-11'})
#     address = div.find('span').text.strip()
#
#     # Remove unnecessary spaces
#     address = ' '.join(address.split())[9:].strip()
#     author = post.find('span', {'class': 'ml5'}).text.strip()
#     online = post.find('span', attrs={'style': 'color: #218700;'}).text
#     online = online[8:]
#
#     msg = ''
#
#     try:
#         data = [title, address, price, size, flatmate, available, online, author, link]
#         query = 'INSERT INTO wg_berlin(data_id, title, address, price, size, ' \
#                 'flatmate, available, on_since, author, link) ' \
#                 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#         # res = db_query(query, data)
#
#         msg += "Title: {}\n" \
#                "Address: {}\n" \
#                "Price: {}\n" \
#                "Size: {}\n" \
#                "Flatmate: {}\n" \
#                "Availability: {}\n" \
#                "Online: {}\n" \
#                "Author: {}\n" \
#                "Link: {}\n\n".format(*data[1:])
#     except Exception as e:
#         print("Error:", e)
#         # print line in which the  error happened
#
#
#
#
#     # except Exception as e:
#     #     print("Error:", e)
#
#
# # {
# #     "@type": "ListItem",
# #     "position": 3,
# #     "item": {
# #         "@type": "RealEstateListing",
# #         "name": "Möbliertes WG-Zimmer mit großem Wohnzimmer in Uninähe",
# #         "url": "https://www.wg-gesucht.de/wg-zimmer-in-Aachen-Aachen.12906738.html",
# #         "description": "3er WG  ",
# #         "datePosted": "2026-01-20",
# #         "offers": {
# #             "@type": "Room",
# #             "price": "472.00",
# #             "priceCurrency": "EUR",
# #             "availability": "https://schema.org/InStock"
# #         },
# #         "provider": {
# #             "@type": "RealEstateAgent",
# #             "name": "Peter"
# #         },
# #         "mainEntity": {
# #             "@type": "Offer",
# #             "address": {
# #                 "@type": "PostalAddress",
# #                 "streetAddress": "Couvenstraße",
# #                 "addressLocality": "Aachen",
# #                 "addressRegion": "Aachen",
# #                 "postalCode": "52062",
# #                 "addressCountry": "Deutschland"
# #             }
#
#
