from bs4 import BeautifulSoup
from dataset.model.jacket_announcement_dto import JacketAnnouncementDto
from scrape.scraper import Scraper


class VintedScraper(Scraper):
    WEBSITE = "https://www.vinted.it/catalog?search_text=giacca%20di%20pelle%20da%20uomo&page="
    PAGES_TO_PARSE = 10
    RAW_DATA_FILE = "vinted_jackets_data_raw.csv"
    COUNTRY = "Italy"

    def parse_html_to_dto(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        items = soup.find_all("div", class_="feed-grid__item")
        page_dtos = []

        for item in items:
            try:
                desc_el = item.find_all("div", class_="new-item-box__description")
                if not desc_el: continue

                title_and_condition = ""
                for el in desc_el:
                    title_and_condition_el = el.find("p")
                    title_and_condition += title_and_condition_el.text.strip()
                    title_and_condition += " "

                price_el = item.find("div", class_="new-item-box__title")

                if not price_el:
                    continue

                parsed_parts = self.parse_title_and_condition(title_and_condition)

                if len(parsed_parts) >= 2:
                    title = parsed_parts[0]
                    condition = parsed_parts[1]
                else:
                    title = parsed_parts[0]
                    condition = "N/A"

                page_dtos.append(JacketAnnouncementDto(
                    title=title,
                    condition=condition,
                    location=self.COUNTRY,
                    price=price_el.get_text(strip=True)
                ))
            except AttributeError as e:
                print(f"skipped announcement: {e}")
                continue
        return page_dtos

    @staticmethod
    def parse_title_and_condition(title_and_condition):
        text = title_and_condition.strip()
        return text.rsplit(' · ', 1)

vinted_scraper = VintedScraper()
vinted_scraper.scrape()
