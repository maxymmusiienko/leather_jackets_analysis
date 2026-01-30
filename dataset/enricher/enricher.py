from abc import ABC, abstractmethod


class Enricher(ABC):
    @abstractmethod
    def extract_price(self, price_data : str) -> float:
        if not price_data:
            return 0.0
        clean = price_data.replace(',', '.').replace('€', '').strip()
        try:
            return float(clean)
        except ValueError:
            return 0.0

    @abstractmethod
    def extract_country(self, location : str) -> str:
        return location

    @abstractmethod
    def extract_condition(self, condition_data : str) -> str:
        pass
