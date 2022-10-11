from enum import EnumMeta, Enum

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

class BaseEnum(Enum, metaclass=MetaEnum):
    pass

class WeatherDatasets(BaseEnum):
    T_AVG = 1
    PCP_AVG = 2
    SEVERE_WEATHER_ALERTS = 3

class EconomicDatasets(BaseEnum):
    AVG_SAL = 1
