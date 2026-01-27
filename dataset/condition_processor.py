from abc import ABC, abstractmethod

class ConditionProcessor(ABC):
    @abstractmethod
    def extract_condition(self, condition: str) -> str:
        """Method for extracting condition"""
        pass

class EbayConditionProcessor(ConditionProcessor):
    def extract_condition(self, condition: str) -> str:
        cleaned_condition = condition.strip().lower()
        if "new" in cleaned_condition:
            return "new"
        return "pre-owned"

class OLXConditionProcessor(ConditionProcessor):
    def extract_condition(self, condition: str) -> str:
        cleaned_condition = condition.strip().lower()
        if "нове" in cleaned_condition:
            return "new"
        return "pre-owned"

class VintedConditionProcessor(ConditionProcessor):
    def extract_condition(self, condition: str) -> str:
        cleaned_condition = condition.strip().lower()
        if "nuovo" in cleaned_condition:
            return "new"
        return "pre-owned"
