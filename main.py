from dataset.brand_processor import BrandProcessor
from dataset.brand_storage import BrandStorage

test_announcement = "Шкіряна куртка stone island, нова неношена"

brand_storage = BrandStorage()
brands = brand_storage.get_brands()
brand_processor = BrandProcessor(brands)

print(brand_processor.extract_brand(test_announcement))
