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
