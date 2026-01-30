from dataset.enricher.conditidion_type import ConditionType
from dataset.enricher.enricher import Enricher


class VintedEnricher(Enricher):
    __CURRENCY_EURO_TO_USD = 1.19

    def extract_country(self, location : str) -> str:
        return location

    def extract_price(self, price_data : str) -> float:
        if not price_data:
            return 0.0
        clean = price_data.replace(',', '.').replace('€', '').strip()
        try:
            return round(float(clean) * self.__CURRENCY_EURO_TO_USD, 2)
        except ValueError:
            return 0.0


    def extract_condition(self, condition_data : str) -> str:
        if "nuovo" in condition_data.strip().lower():
            return ConditionType.NEW.value
        return ConditionType.USED.value
