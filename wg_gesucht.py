from bs4 import BeautifulSoup
import json
import pprint
import requests



test = True




if test:
    with open("wg_gesucht_page.html", "r", encoding="utf-8") as file:
        html = file.read()
else:
    url_base = "https://www.wg-gesucht.de/wg-zimmer-in-Aachen.1.0.1.0.html?offer_filter=1&city_id=1&sort_order=0&noDeact=1&categories%5B%5D=0&rMax=500"

    page_appendix = "&pagination=0&pu="

    urls = []

    site_count = 2

    for i in range(site_count):
        urls.append(url_base + page_appendix.replace("0", str(i)))

    html = ""
    for i in range(site_count):
        url = urls[i]
        print(f"Fetching URL: {url}")
        page_html = requests.get(url).text
        html += page_html


soup = BeautifulSoup(html, 'lxml')

print(soup)
print("."*100)

# Find all JSON-LD scripts
scripts = soup.find_all("script", type="application/ld+json")

print(len(scripts))

print(scripts[2])

exit()

script = scripts[1]
# print(len(scripts))
listings = []

# for script in scripts:
    # print(script)
# try:
data = script.string.strip()[:-1]

# print(data)
try:
    # # Prüfen, ob der JSON-String ein Array ist
    # if data.startswith("[") and data.endswith("]"):
    #     json_objects = json.loads(data)
    # else:
    #     json_objects = [json.loads(data)]

    # for obj in json_objects:
    #     print(obj)
    data_json = json.loads(data)

except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    # print(data)

pprint.pprint(data_json)
print("marker2")
print(type(data_json))
print(len(data_json))
print(data_json[0].keys())
print(data_json[1].keys())
listings = data_json[1].get("mainEntity").get("itemListElement")
# print(listings[0])
# print(listings)
print(len(listings))


    # if isinstance(data, dict):
    #     listings.append(data)
    #     print(data)

# except (json.JSONDecodeError, TypeError):
# except Exception:
#     print("Typeerror")
#     print(type(data))
#     print(data)
    # continue

# print(listings)
print(len(listings))
results = []

for entry in listings:
    pprint.pprint(entry)




    # break

    item = entry["item"]

    results.append({
        "position": entry.get("position"),
        "title": item.get("name"),
        "url": item.get("url"),
        "price": item.get("offers", {}).get("price"),
        "currency": item.get("offers", {}).get("priceCurrency"),
        "image": item.get("image"),
        "provider": item.get("provider", {}).get("name"),
        "street": item.get("mainEntity", {})
                     .get("address", {})
                     .get("streetAddress"),
        "city": item.get("mainEntity", {})
                    .get("address", {})
                    .get("addressLocality"),
        "postal_code": item.get("mainEntity", {})
                           .get("address", {})
                           .get("postalCode"),
        "description": item.get("description")
    })

    # title, url, price, description

    # filter

blockwords = [
    "kathol",
    "verbindung"
]

blocked_addresses = [
    "Krefelder Str. 24",
    "Lousbergstraße 46",
    "Melatener Straße 48"
]

blocked_addresses = [
    "Lousbergstr. 44",       # Turnerschaft Rheno-Borussia Aachen :contentReference[oaicite:0]{index=0}
    "Turmstr. 4",            # Landsmannschaft Pomerania Halle-Aachen :contentReference[oaicite:1]{index=1}
    "Krefelder Str. 24",     # Aachener Burschenschaft Alania :contentReference[oaicite:2]{index=2}
    "Muffeter Weg 15",       # Brünner Burschenschaft Libertas :contentReference[oaicite:3]{index=3}
    "Salvatorstr. 38",       # Aachener Burschenschaft Teutonia :contentReference[oaicite:4]{index=4}
    "Am Weißenberg 48",      # Danziger Burschenschaft Alemannia :contentReference[oaicite:5]{index=5}
    "Hainbuchenstr. 23",     # Corps Delta :contentReference[oaicite:6]{index=6}
    "Salierallee 48",        # Corps Frankonia Fribergensis :contentReference[oaicite:7]{index=7}
    "Lütticher Str. 162",    # Corps Montania :contentReference[oaicite:8]{index=8}
    "Krefelder Str. 33",     # Corps Palaeo-Teutonia :contentReference[oaicite:9]{index=9}
    "Melatenerstr. 41",      # Corps Saxo-Montania :contentReference[oaicite:10]{index=10}
    "Moreller Weg 64",       # Corps Marko-Guestphalia :contentReference[oaicite:11]{index=11}
    "Kaiser-Friedrich-Allee 5", # Corps Saxonia Berlin :contentReference[oaicite:12]{index=12}
    "Nizzaallee 56",         # Corps Borussia Breslau :contentReference[oaicite:13]{index=13}
    "Junkerstr. 68",         # KDStV Ripuaria :contentReference[oaicite:14]{index=14}
    "Rütscherstr. 110",      # KDStV Baltia Danzig :contentReference[oaicite:15]{index=15}
    "Kruppstr. 8-10",        # KDStV Bergland :contentReference[oaicite:16]{index=16}
    "Ludwigsallee 101",      # KDStV Franconia :contentReference[oaicite:17]{index=17}
    "Hexenberg 10",          # KDStV Kaiserpfalz :contentReference[oaicite:18]{index=18}
    "Nizzaallee 4",          # KDStV Marchia (Breslau) :contentReference[oaicite:19]{index=19}
    "Krefelder Str. 24",
    "Lousbergstraße 46",
    "Melatener Straße 48"
]


for r in results:

    if any(bw in r.get("title", "").lower() for bw in blockwords):
        print(f"Blocked listing (blockwords): {r.get('title')}")
        continue

    if any(ba in r.get("street", "") for ba in blocked_addresses):
        print(f"Blocked listing (address): {r.get('street')}")
        continue

    print(r)
    # title, url, price, description
    #
    # print(r.get("title"))
    # # print(r.get("url"))
    # print(r.get("price"), r.get("currency"))
    # print(r.get("description"))


