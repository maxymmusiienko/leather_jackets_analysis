from bs4 import BeautifulSoup

from dataset.model.jacket_announcement_dto import JacketAnnouncementDto
from scrape.scraper import Scraper


class OlxScraper(Scraper):
    """Scrapes and saves data from olx. Olx is a Ukrainian community marketplace(like ebay).
    Request on the site is <Чоловіча шкіряна куртка>"""

    WEBSITE = "https://m.olx.ua/uk/moda-i-stil/muzhskaya-odezhda/verhnyaya-odezhda/q-%D1%87%D0%BE%D0%BB%D0%BE%D0%B2%D1%96%D1%87%D0%B0-%D1%88%D0%BA%D1%96%D1%80%D1%8F%D0%BD%D0%B0-%D0%BA%D1%83%D1%80%D1%82%D0%BA%D0%B0/?currency=UAH&page="
    PAGES_TO_PARSE = 25
    RAW_DATA_FILE = "olx_jackets_data_raw.csv"
    COUNTRY = "Ukraine"

    def parse_html_to_dto(self, html):
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", class_="css-1sw7q4x")
        page_dtos = []

        for item in items:
            try:
                title_el = item.find("h4", class_="css-hzlye5")
                price_el = item.find("p", class_="css-blr5zl")
                cond_span_el = item.find("span", class_="css-1mqzepw")

                if not title_el or not price_el:
                    continue

                condition_text = "N/A"
                if cond_span_el:
                    inner_span = cond_span_el.find("span")
                    if inner_span:
                        condition_text = inner_span.get_text(strip=True)

                page_dtos.append(JacketAnnouncementDto(
                    title=title_el.get_text(strip=True),
                    price=price_el.get_text(strip=True),
                    condition=condition_text,
                    location=self.COUNTRY
                ))
            except AttributeError as e:
                print(f"skipped announcement: {e}")
                continue

        return page_dtos
