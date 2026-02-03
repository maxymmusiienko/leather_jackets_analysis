from typing import List

import pandas as pd

from dataset.enricher.brand_processor import BrandProcessor
from dataset.enricher.brand_storage import BrandStorage
from dataset.enricher.country_processor import CountryProcessor
from dataset.enricher.enricher_factory import EnricherFactory
from dataset.enricher.store_name import StoreName

configs = [
    {'path': 'C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\scrape\\ebay_jackets_data_raw.csv',
     'name': StoreName.EBAY},
    {'path': 'C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\scrape\\olx_jackets_data_raw.csv',
     'name': StoreName.OLX},
    {'path': 'C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\scrape\\vinted_jackets_data_raw.csv',
     'name': StoreName.VINTED}
]

class DataUnionPipeline:
    FILE_PATH = 'C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\analysis\\masters_jackets_data.csv'

    def __init__(self):
        self.brand_storage = BrandStorage()
        self.brand_processor = BrandProcessor(brands=self.brand_storage.get_brands())

    def transform_file(self, input_path, source_name : StoreName):
        df = pd.read_csv(input_path)
        enricher = EnricherFactory.get_enricher(source_name)

        df['price($)'] = df['price'].apply(enricher.extract_price)
        df['location'] = df['location'].apply(enricher.extract_country)
        df['country_code'] = df['location'].apply(CountryProcessor.get_iso_code)
        df['store_name'] = source_name.value
        df['store_type'] = enricher.get_store_type().value
        df['simple_condition'] = df['condition'].apply(enricher.extract_condition)
        df['brand'] = df['title'].apply(self.brand_processor.extract_brand)
        df['has_brand'] = df['brand'] != 'Other'
        df['title_length'] = df['title'].apply(lambda x: len(x))

        return df

    def run(self, file_configs: List[dict], output_path: str):
        all_dfs = []

        for config in file_configs:
            print(f"Обробка {config['name']}...")
            df = self.transform_file(config['path'], config['name'])
            all_dfs.append(df)

        master_df = pd.concat(all_dfs, ignore_index=True)
        master_df.to_csv(output_path, index=False)
        print(f"Master data saved to file: {output_path}")

pipe = DataUnionPipeline()
pipe.run(configs, pipe.FILE_PATH)
