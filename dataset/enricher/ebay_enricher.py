import re

from dataset.enricher.conditidion_type import ConditionType
from dataset.enricher.enricher import Enricher
from dataset.enricher.store_type import StoreType


class EbayEnricher(Enricher):
    def extract_condition(self, condition_data : str) -> str:
        if "new" in condition_data.lower():
            return ConditionType.NEW.value
        return ConditionType.USED.value

    def extract_price(self, price_data : str) -> float:
        try:
            price = float(price_data.replace("$", ""))
            return price
        except ValueError:
            return 0

    def extract_country(self, location : str) -> str:
        match = re.search(r"Located in\s+(.*)", location, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return "Unknown"

    def get_store_type(self) -> StoreType:
        return StoreType.INTERNATIONAL
