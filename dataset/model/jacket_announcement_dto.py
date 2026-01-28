from dataclasses import dataclass

@dataclass
class JacketAnnouncementDto:
    title: str
    condition: str
    price: str
    location: str
