import re
from bs4 import BeautifulSoup

def extract_rwth_job_infos(content):
    """Extract job information from the fetched content."""
    soup = BeautifulSoup(content, 'lxml')
    listings = soup.find_all('li')
    jobs = []

    for listing in listings:
        if "veröffentlicht" in listing.text:
            try:
                link = "https://www.rwth-aachen.de" + listing.find('a').get('href')
                txt = listing.text
                deadline = txt.split("\n")[3]
                title = txt[:txt.find("[")].replace("\n", "")
                listing_number = re.findall(r'V\d{9}', txt)[0]
                pub_date = re.findall(r'veröffentlicht am \d{2}\.\d{2}\.\d{4}', txt)[0]
                location = txt.split("\n")[2]

                individual_job_dict = {
                    "link": link,
                    "title": title,
                    "listing_number": listing_number,
                    "deadline": deadline,
                    "pub_date": pub_date,
                    'location': location,
                }
                jobs.append(individual_job_dict)
            except Exception as e:
                print(f"Error parsing listing: {e}")

    return jobs
