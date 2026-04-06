import json
from pathlib import Path
from functions.handling import blockedwohnung
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True) # "autoreset=True" automatically resets the color after each print statement

# print(f"{Fore.RED}This text is red.")
# print(f"{Fore.GREEN}This text is green with a {Style.BRIGHT}{Fore.YELLOW}bright yellow word{Style.NORMAL} in it.")
# print("This text is back to the default color.")


def equality(w1, w2):
    same_counter = 0
    not_same_counter = 0
    for key in w1.keys():
        if key in ["blocked", "currency", "city"]:
            continue
        if w1.get(key, None) == w2.get(key, None):
            same_counter += 1
            # print(f"w1: {w1.get(key, None)}, w2: {w2.get(key, None)}")
        else:
            not_same_counter += 1
            # print(f"w1: {w1.get(key, None)}, w2: {w2.get(key, None)}")

    return not_same_counter


def wohnung_zusammenfassung(filepath="falcon/wg_gesucht.json"):
    def get_file(name):
        with open(name, "r") as file:
            return json.load(file)

    files = get_file(filepath)

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

    for duplicate in duplicates:
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
        print(f"{bucket:4d} - {bucket + (bucket_size - 1):4d} € ({'0' if histogram[bucket] < 10 else ''}{histogram[bucket]}) {bar}")
        send_text += f"\n{bucket:4d}-{bucket + (bucket_size - 1):4d} € ({'0' if histogram[bucket] < 10 else ''}{histogram[bucket]}) {bar}"

    print(send_text)
    return send_text


def filter_test():
    addresses = ["Kruppstr 12", "Kruppstraße 12", "Krupp Strasse 12", "Kruppstraße12", "  kruppstraße   12  ", "Kruppstrasse 12", "Krupp Str. 12", "Krupp Str 12", "Kruppstr.12"]
    print(len(addresses))
    counter = 0
    for address in addresses:
        counter += 1 if blockedwohnung("wg_gesucht", {"street": address}) else +0

    print(counter)


def makered(txt):
    return f"{Fore.RED}{txt}{Style.RESET_ALL}"

def makegreen(txt):
    return f"{Fore.GREEN}{txt}{Style.RESET_ALL}"


if __name__ == "__main__":
    # wohnung_zusammenfassung(filepath=str(Path.cwd().parent) + "\\" "falcon\\wg_gesucht.json")

    path = filepath = str(Path.cwd().parent) + "\\" "falcon\\wg_gesucht.json"

    def get_file(name):
        with open(name, "r") as file:
            return json.load(file)

    wohnungen = get_file(filepath)

    already_checked = []
    for i, wi in enumerate(wohnungen):
        for j, wj in enumerate(wohnungen):
            if i == j:
                continue
            if (j, i) in already_checked:
                continue
            elif (i, j) in already_checked:
                continue
            already_checked.append((i,j))
            differences = equality(wj, wi)

            # print(differences)

            if differences == 0:
                print("is the same")

                # for key in wj.keys():
                #     print(f"w1: {wj.get(key, None)}, w2: {wi.get(key, None)}")

            elif differences <= 3:
                print("possibly the same")


                for key in wj.keys():
                    if wj.get(key, None) == wi.get(key, None):
                        # print("gleich:   ", end="")
                        print(makered(f"w1: {wj.get(key, None)}, w2: {wi.get(key, None)}"))
                    else:
                        print(makegreen(f"w1: {wj.get(key, None)}, w2: {wi.get(key, None)}"))
                        # print("ungleich: ", end="")

                print("-_"*100)
                # print()
