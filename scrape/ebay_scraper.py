import csv
import re
from dataclasses import asdict
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from dataset.model.jacket_announcement_dto import JacketAnnouncementDto
from scrape.scraper import Scraper

class EbayScraper(Scraper):
    WEBSITE = "https://www.ebay.com/sch/i.html?_nkw=leather+jacket+man&_sacat=0&_from=R40&_pgn="
    PAGES_TO_PARSE = 150
    RAW_DATA_FILE = 'ebay_jackets_data_raw.csv'

    def scrape(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0...")
            page = context.new_page()

            all_jackets = []

            for pgn in range(1, self.PAGES_TO_PARSE + 1):
                try:
                    url = f"{self.WEBSITE}{pgn}"
                    print(f"Processing page №{pgn}...")

                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_timeout(2000)
                    html = page.content()

                    dtos = self.parse_html_to_dto(html)
                    all_jackets.extend(dtos)
                    print(f"Collected {len(dtos)} announcements from page {pgn}")

                except Exception as e:
                    print(f"❌ Error on page {pgn}: {e}")
                    continue

            browser.close()

        if all_jackets:
            self.save_to_csv(all_jackets)

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

    def save_to_csv(self, data):
        with open(self.RAW_DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(data[0]).keys())
            writer.writeheader()
            for dto in data:
                writer.writerow(asdict(dto))
        print(f"Collected: {len(data)} announcements.")

ebay_scraper = EbayScraper()
ebay_scraper.scrape()
