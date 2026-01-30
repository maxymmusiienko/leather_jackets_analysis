class BrandStorage:
    __FILE_PATH = '/brands.txt'
    __brands = []

    def __init__(self):
        self.__brands = self.__extract_brand(self.__FILE_PATH)

    def get_brands(self):
        return self.__brands

    def __extract_brand(self, file_path) -> list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                brands = [line.strip() for line in f if line.strip()]
            return brands
        except FileNotFoundError:
            print(f"Помилка: Файл '{file_path}' не знайдено.")
            return []
