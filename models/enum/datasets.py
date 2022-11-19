from enum import EnumMeta, Enum

class MetaEnum(EnumMeta):
    def __contains__(cls, item) -> bool:
        try:
            cls(item)
        except ValueError:
            return False
        return True

class BaseEnum(Enum, metaclass=MetaEnum):
    pass

class WeatherDatasets(str, BaseEnum):
    T_AVG = 'T_AVG'
    PCP_AVG = 'PCP_AVG'
    SEVERE_WEATHER_ALERTS = 'SEVERE_WEATHER_ALERTS'

class EconomicDatasets(str, BaseEnum):
    UNEMP = 'UNEMP'
    AVG_SAL = 'AVG_SAL'

class ViewingAreas(str, BaseEnum):
    USA = 'USA'

class DatasetLevels(str, BaseEnum):
    COUNTY = 'COUNTY'

class GeoDataFormat(str, BaseEnum):
    JSON = 'JSON'
    CSV = 'CSV'

class ZDataFormat(str, BaseEnum):
    JSON = 'JSON'
    CSV = 'CSV'
