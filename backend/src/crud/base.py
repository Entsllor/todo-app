from typing import Mapping

from src.core.database import db


class BaseCrud:
    model: db.Model

    def get_many(self, filters: Mapping):
        return self.model.query.filter_by(**filters).all()

    def get_one(self, filters: Mapping):
        return self.model.query.filter_by(**filters).first()

    def get_by_id(self, id_):
        return self.get_one({"id": id_})

    def delete(self, filters: Mapping):
        return self.model.query.filter_by(**filters).delete()

    def update(self, values: Mapping, filters: Mapping):
        return self.model.query.filter_by(**filters).update(values)
