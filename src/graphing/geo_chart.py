import HeatMap
from enum import Enum

class GeoSpecifier(Enum):
    COUNTY = 1

    @classmethod
    def value_of(cls, value):
        """Compare the value of a string to enum values."""
        # The class of enum to compare the string to.
        # cls = "your-enum-name"
        # The string value to compare.
        # value = "your-string=value"
        for k, v in cls.__members__.items():
            if k == value:
                return v
        else:
            raise ValueError(f"'{cls.__name__}' enum not found for '{value}'")

class GeoHeatMap(HeatMap):
    geo_region: str
    geo_specifier: GeoSpecifier
