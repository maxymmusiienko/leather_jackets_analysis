import csv
from abc import ABC, abstractmethod
from dataclasses import asdict

from playwright.sync_api import sync_playwright


class Scraper(ABC):
    PAGES_TO_PARSE : int
    WEBSITE : str
    RAW_DATA_FILE : str

    @abstractmethod
    def parse_html_to_dto(self, html):
        pass

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
                    print(f"Error on page {pgn}: {e}")
                    continue

            browser.close()

        if all_jackets:
            self.save_to_csv(all_jackets, self.RAW_DATA_FILE)

    @staticmethod
    def save_to_csv(data, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(data[0]).keys())
            writer.writeheader()
            for dto in data:
                writer.writerow(asdict(dto))
        print(f"Collected: {len(data)} announcements.")
