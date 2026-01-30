from typing import Dict, Type

from dataset.enricher.ebay_enricher import EbayEnricher
from dataset.enricher.enricher import Enricher
from dataset.enricher.olx_enricher import OlxEnricher
from dataset.enricher.store_name import StoreName
from dataset.enricher.vinted_enricher import VintedEnricher


class EnricherFactory:
    ENRICHERS: Dict[StoreName, Type[Enricher]] = {
        StoreName.VINTED: VintedEnricher,
        StoreName.EBAY: EbayEnricher,
        StoreName.OLX: OlxEnricher,
    }

    @staticmethod
    def get_enricher(store_name: StoreName) -> Enricher:
        enricher_class = EnricherFactory.ENRICHERS.get(store_name)

        if not enricher_class:
            raise ValueError(f"Enricher for store '{store_name}' is not implemented.")

        return enricher_class()
