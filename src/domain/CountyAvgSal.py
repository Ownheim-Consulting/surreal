from sqlalchemy import Column, Integer, String
from sqlalchemy.types import REAL

from .db import Base, Session

class CountyAvgSal(Base):
    __tablename__ = 'county_avg_sal'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lat = Column(REAL)
    lng = Column(REAL)
    lr2017 = Column(REAL)
    lr2018 = Column(REAL)
    lr2019 = Column(REAL)
    lr2020 = Column(REAL)
    lr2021 = Column(REAL)
    lr2022 = Column(REAL)
    lr2023 = Column(REAL)

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lng": self.lng,
            "lr2017": self.lr2017,
            "lr2018": self.lr2018,
            "lr2019": self.lr2019,
            "lr2020": self.lr2020,
            "lr2021": self.lr2021,
            "lr2022": self.lr2022,
            "lr2023": self.lr2023
        }

def addCountyAvgSal(s: Session, c: CountyAvgSal) -> CountyAvgSal:
        s.add(c)
        s.commit()
        return c

def getCountyAvgSalByLatLng(s: Session, lat: str, lng: str) -> CountyAvgSal:
        c = s.query(CountyAvgSal).filter(CountyAvgSal.lat == lat).filter(CountyAvgSal.lng == lng).first()
        return c

def getCountyAvgSalByName(s: Session, name: str) -> CountyAvgSal:
        c = s.query(CountyAvgSal).filter(CountyAvgSal.name == name).first()
        return c
