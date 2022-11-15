from database import Base
from repos.base_repo import BaseRepo

from sqlalchemy.orm import Session

class SqliteRepo(BaseRepo):
    entity: Base = None
    db: Session = None

    def __init__(self, db: Session, entity: Base) -> None:
        super().__init__(db, entity)

    def get(self, id: any):
        return self.db.query(self.entity).filter(self.entity.id == id).first()

    def get_all(self) -> list:
        return self.db.query(self.entity).all()

    def persist(self, entity: entity) -> None:
        self.db.add(entity)
        self.db.commit()

    def update(self, entity: entity) -> None:
        self.db.update()
        self.db.commit()

    def delete(self, entity: entity) -> None:
        self.db.delete(entity)
        self.db.commit()

