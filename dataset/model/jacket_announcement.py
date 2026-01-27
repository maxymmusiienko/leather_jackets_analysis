class JacketAnnouncement:
    __price : float
    __country : str
    __brand : str
    __condition : str
    __store : str
    __store_type : str
    __title : str

    def __init__(self, price: float, country: str, brand: str, condition: str, store: str, store_type: str, title: str):
        self.__price = price
        self.__country = country
        self.__brand = brand
        self.__condition = condition
        self.__store = store
        self.__store_type = store_type
        self.__title = title

    def get_price(self) -> float:
        return self.__price

    def get_country(self) -> str:
        return self.__country

    def get_brand(self) -> str:
        return self.__brand

    def get_condition(self) -> str:
        return self.__condition

    def get_store(self) -> str:
        return self.__store

    def get_store_type(self) -> str:
        return self.__store_type

    def get_title(self) -> str:
        return self.__title
