import pycountry


class CountryProcessor:
    @staticmethod
    def get_iso_code(country_name: str) -> str:
        if not country_name:
            return "Unknown"

        clean_name = country_name.strip().title()

        try:
            country = pycountry.countries.lookup(clean_name)
            return country.alpha_2
        except (LookupError, AttributeError):
            return "Unknown"
