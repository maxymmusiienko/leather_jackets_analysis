import re

class PriceProcessor:
    @staticmethod
    def extract_price(price_str : str) -> float:
        try:
            num_str = re.sub(r'[^\d.]', '', price_str.replace(',', ''))
            return float(num_str)
        except ValueError:
            return 0.0
