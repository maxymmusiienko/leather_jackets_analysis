import re

from dataset.enricher.conditidion_type import ConditionType
from dataset.enricher.enricher import Enricher


class OlxEnricher(Enricher):
    __CURRENCY_USD_TO_UAH = 42.9

    def extract_country(self, location : str) -> str:
        return location

    def extract_condition(self, condition_data : str) -> str:
        if condition_data.strip() == "Нове":
            return ConditionType.NEW.value
        return ConditionType.USED.value

    def extract_price(self, price_data: str) -> float:
        if not price_data:
            return 0.0
        clean_number = re.sub(r'\D', '', price_data)
        if not clean_number:
            return 0.0
        price_in_target_currency = float(clean_number) / self.__CURRENCY_USD_TO_UAH
        return round(price_in_target_currency, 2)
