import re

from bs4 import BeautifulSoup

from dataset.model.jacket_announcement_dto import JacketAnnouncementDto
from scrape.scraper import Scraper


class EbayScraper(Scraper):
    """Scrapes and saves data from ebay. Request on the site is <leather jacket man>"""
    WEBSITE = "https://www.ebay.com/sch/i.html?_nkw=leather+jacket+man&_sacat=0&_from=R40&_pgn="
    PAGES_TO_PARSE = 150
    RAW_DATA_FILE = 'ebay_jackets_data_raw.csv'

    def parse_html_to_dto(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        items = soup.find_all("li", class_="s-card")
        page_dtos = []

        for item in items[2:]:
            title_tag = item.find("div", role="heading")
            price_tag = item.find("span", class_="s-card__price")

            if title_tag and price_tag:
                title = title_tag.get_text(strip=True).replace("Opens in a new window or tab", "")

                price = price_tag.get_text(strip=True)

                condition = (item.find("div", class_="s-card__subtitle")
                             .get_text(strip=True)) if item.find("div", class_="s-card__subtitle") else "N/A"

                location = item.find(string=re.compile("Located in"))

                page_dtos.append(JacketAnnouncementDto(
                    title=title,
                    condition=condition,
                    price=price,
                    location=location
                ))
        return page_dtos
