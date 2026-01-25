import json
from pathlib import Path
from functions.handling import blocked
def wohnung_zusammenfassung():
    def get_file(name):
        with open(name, "r") as file:
            return json.load(file)

    # files = get_file(str(Path.cwd().parent) + "\\" "buzzard\\wg_gesucht.json")
    files = get_file("falcon/wg_gesucht.json")

    seen = set()
    seen2 = set()
    seen3 = set()
    duplicates = []
    for file in files:
        street = file.get("street", "")
        provider = file.get("provider", "")
        price = file.get("price", "")
        print(f"street: {street}, provider: {provider}")
        if street in seen and provider in seen2 and price in seen3:
            duplicates.append(file)
        else:
            seen.add(street)
            seen2.add(provider)
            seen3.add(price)
    print(f"Found {len(duplicates)} duplicate entries.")

    for duplicate in  duplicates:
        print(duplicate)

    rents = []
    for file in files:
        if not file.get("blocked"):
            price_str = file.get("price", "").replace("€", "").replace(",", "").strip()
            try:
                price = float(price_str)
                if price < 300:
                    print(f"price very low: {file.get('title', 'N/A')} - {price} €")
                rents.append(price)
            except ValueError:
                print("Valueerror")
                continue
        else:
            print(f"Blocked entry: {file.get('title', 'N/A')}")


    average_rent = sum(rents) / len(rents) if rents else 0
    median_rent = sorted(rents)[len(rents) // 2] if rents else 0

    print(f"Average rent (excluding blocked): {average_rent:.2f} €")
    print(f"Median rent (excluding blocked): {median_rent:.2f} €")
    send_text = f"Average rent: {average_rent:.2f} €\nMedian rent: {median_rent:.2f} €"

    bucket_size = 40
    histogram = {}
    for rent in rents:
        bucket = int(rent // bucket_size) * bucket_size
        histogram[bucket] = histogram.get(bucket, 0) + 1

    print("Rent Distribution Histogram:")
    for bucket in sorted(histogram.keys()):
        bar = '|' * histogram[bucket]
        print(f"{bucket:4d} - {bucket + (bucket_size-1):4d} € ({'0' if histogram[bucket] < 10 else ''}{histogram[bucket]}) {bar}")
        send_text += f"\n{bucket:4d}-{bucket + (bucket_size-1):4d} € ({'0' if histogram[bucket] < 10 else ''}{histogram[bucket]}) {bar}"

    print(send_text)
    return send_text

def filter_test():
    addresses = ["Kruppstr 12", "Kruppstraße 12", "Krupp Strasse 12", "Kruppstraße12", "  kruppstraße   12  ", "Kruppstrasse 12", "Krupp Str. 12", "Krupp Str 12", "Kruppstr.12"]
    print(len(addresses))
    counter = 0
    for address in addresses:
        counter += 1 if blocked("wg_gesucht", {"street": address}) else +0

    print(counter)



if __name__ == "__main__":
    wohnung_zusammenfassung()



