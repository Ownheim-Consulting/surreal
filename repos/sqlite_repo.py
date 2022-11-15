from dataclasses import dataclass

from database import Base
from repos.base_repo import BaseRepo
from models.choropleth_map import ChoroplethMap

from sqlalchemy.orm import Session

T = Base

@dataclass
class SqliteRepo(BaseRepo[T]):
    db: Session
    model: T

    def get(self, id: any) -> T:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> list:
        return self.db.query(self.model).all()

    def persist(self, entity: T) -> None:
        self.db.add(entity)
        self.db.commit()

    def update(self, entity: T) -> None:
        self.db.update()
        self.db.commit()

    def delete(self, entity: T) -> None:
        self.db.delete(entity)
        self.db.commit()
