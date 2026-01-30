from flashtext import KeywordProcessor

class BrandProcessor:
    __brands : list
    __keyword_processor : KeywordProcessor

    def __init__(self, brands : list):
        self.__brands = brands
        self.__keyword_processor = KeywordProcessor(case_sensitive=False)
        self.__keyword_processor.add_keywords_from_list(self.__brands)

    def extract_brand(self, text:str) -> str:
        brands = self.__keyword_processor.extract_keywords(text)
        if len(brands) > 0:
            return brands[0]
        return 'Other'
