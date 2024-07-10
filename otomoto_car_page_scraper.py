import re
import time
from dataclasses import dataclass
import sys
import os
import cloudscraper

from utils import write_url_to_file, DBConnector


@dataclass(frozen=True)
class Car:
    id: str
    price: int
    year: int
    mileage: int
    engine_capacity: int
    engine_power: int
    fuel_type: str
    transmission: str
    accident_free: bool
    origin: str
    four_wheel_drive: bool
    invoice_vat: bool
    estate: bool
    page_src: str = None

    def __str__(self):
        # no page_src
        return (f"Car(id={self.id}, price={self.price}, year={self.year}, mileage={self.mileage}, "
                f"engine_capacity={self.engine_capacity}, engine_power={self.engine_power}, fuel_type={self.fuel_type},"
                f" transmission={self.transmission}, accident_free={self.accident_free}, origin={self.origin}, "
                f"four_wheel_drive={self.four_wheel_drive}, invoice_vat={self.invoice_vat}, estate={self.estate})")

    def __repr__(self):
        return self.__str__()


def translate_fuel_type(fuel_type):
    if fuel_type == "Benzyna":
        return "Petrol"
    elif fuel_type == "Diesel":
        return "Diesel"
    else:
        return "Unknown"


def translate_transmission(transmission):
    if transmission == "Manualna":
        return "Manual"
    elif transmission == "Automatyczna":
        return "Automatic"
    else:
        return "Unknown"


def get_car_data(page_source, page_url):
    offer_id = re.search(r"-([^-.]+)\.html$", page_url).group(1)

    price = re.search(r'"rawPrice":"(\d+)"', page_source).group(1)
    price = int(price)
    year = re.search(r'"mainFeatures":\s*\["(\d{4})"', page_source).group(1)
    year = int(year)
    mileage = re.search(r'"mileage":"([\d ]+?) ?(km|")', page_source).group(1)
    mileage = int(mileage.replace(" ", ""))
    engine_capacity = re.search(r'"label":"(\d\s? \d{3}) cm3', page_source).group(1)
    engine_capacity = int(engine_capacity.replace(" ", ""))
    engine_power = re.search(r'"label":"Moc","value":"(\d+)', page_source).group(1)
    engine_power = int(engine_power)

    fuel_type = re.search(r'"label":"Rodzaj paliwa","value":"(\w+)', page_source).group(
        1
    )
    fuel_type = translate_fuel_type(fuel_type)

    transmission = re.search(
        r'"label":"Skrzynia biegów","value":"(\w+)', page_source
    ).group(1)
    transmission = translate_transmission(transmission)
    if accident_free := re.search(
        r'"label":"Bezwypadkowy","value":"(\w+)', page_source
    ):
        accident_free = accident_free.group(1)
    else:
        accident_free = "Nie"
    accident_free = accident_free == "Tak"
    if origin := re.search(r'"label":"Kraj pochodzenia","value":"(\w+)', page_source):
        origin = origin.group(1)
    else:
        origin = "Unknown"
    if four_wheel_drive := re.search(r'"label":"Napęd","value":"(.+?)"', page_source):
        four_wheel_drive = four_wheel_drive.group(1)
    else:
        four_wheel_drive = "Unknown"
    four_wheel_drive = "4x4" in four_wheel_drive

    if invoice_vat := re.search(r'"label":"Faktura VAT","value":"(\w+)', page_source):
        invoice_vat = invoice_vat.group(1)
    else:
        invoice_vat = "Nie"
    invoice_vat = invoice_vat == "Tak"

    estate = re.search(r'"Typ nadwozia","value":"(\w+)', page_source).group(1)

    estate = not estate == "Sedan"

    return Car(
        id=offer_id,
        price=price,
        year=year,
        mileage=mileage,
        engine_capacity=engine_capacity,
        engine_power=engine_power,
        fuel_type=fuel_type,
        transmission=transmission,
        accident_free=accident_free,
        origin=origin,
        four_wheel_drive=four_wheel_drive,
        invoice_vat=invoice_vat,
        estate=estate,
        page_src=page_source,
    )


def get_page_content(url):
    with cloudscraper.create_scraper() as scraper:
        response = scraper.get(url, timeout=15)
        response.raise_for_status()
    return response.text


def save_page_src_to_file(car):
    if not os.path.exists("SourceHtmls"):
        os.makedirs("SourceHtmls")
    with open(f"SourceHtmls/{car.id}.html", "w", encoding="utf-8") as f:
        f.write(car.page_src)


def load_urls(start_pos=0):

    with open("failed_urls.txt", "r", encoding="utf-8") as file:
        urls = file.read().splitlines()

    return urls[start_pos:]


def main():
    urls = load_urls(start_pos=0)
    db_connector = DBConnector()
    db_connector.connect()

    i = 0
    for url in urls:
        try:
            print(i, " ", url)

            content = get_page_content(url)
            car = get_car_data(content, url)
            print(car)
            save_page_src_to_file(car)
            db_connector.insert_car(car)
        except Exception as e:
            print(f"Error while processing url: {url}", e)
            write_url_to_file(url, failed=True)

        finally:
            time.sleep(5)
            i += 1
    db_connector.close()


if __name__ == "__main__":
    main()
