import time

import cloudscraper
from bs4 import BeautifulSoup

from utils import write_url_to_file


def get_cars_links(category_page_source):
    soup = BeautifulSoup(category_page_source, 'html.parser')

    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith("https://www.otomoto.pl/osobowe/oferta/"):
            links.add(href)
    print("Found links: ", len(links))
    return links


def get_page_source(url, page_number):
    try:
        with cloudscraper.create_scraper() as scraper:
            response = scraper.get(f"{url}{page_number}", timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error getting page src: {e}")
        return None


def main():
    url = ('https://www.otomoto.pl/osobowe/uzywane/volkswagen/passat?'
           'search[filter_enum_generation]=gen-b8-2014&search[order]=created_at_first:desc&page=')

    curr_page = 1
    max_page = 66

    while curr_page <= max_page:
        try:
            print("Current page: ", curr_page)
            page_source = get_page_source(url, curr_page)
            if page_source:
                links = get_cars_links(page_source)
                write_url_to_file(links)
                curr_page += 1
        except Exception as e:
            print(f"Error while processing page: {curr_page}", e)
        finally:
            time.sleep(5)


if __name__ == '__main__':
    main()
