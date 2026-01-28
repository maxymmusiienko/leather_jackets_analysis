from abc import ABC, abstractmethod

class Scraper(ABC):
    """This method gets and saves list of announcements from website"""
    @abstractmethod
    def scrape(self):
        pass
