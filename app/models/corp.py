from typing import Optional

from sqlalchemy.orm import relationship

from app.models import db, TimestampMixin, BaseModelMixin
from app.models.stockprice import Stockprice


class CorpSimple:
    def __init__(self, corpname: str, corpcode: str) -> None:
        super().__init__()
        self.corpcode = corpcode
        self.corpname = corpname

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, CorpSimple):
            return False

        return self.corpcode == o.corpcode \
            and self.corpname == o.corpname

    def __repr__(self) -> str:
        return f"<corpcode=[{self.corpcode}] "\
               f"corpname=[{self.corpname}]>"


class Corp(db.Model, BaseModelMixin, TimestampMixin):
    __tablename__ = 'corps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    corpcode = db.Column(db.String(20), nullable=True)
    corpname = db.Column(db.String(200), nullable=True)


Corp.stockprices = relationship(
    "Stockprice",
    order_by=Stockprice.id,
    back_populates="corp",
)


def get_corp_or_assert(corpcode: str) -> Corp:
    corp = Corp.query \
        .filter_by(corpcode=corpcode) \
        .one()
    return corp


def get_corp_or_none(corpcode: str) -> Optional[Corp]:
    corp = Corp.query \
        .filter_by(corpcode=corpcode) \
        .one_or_none()
    return corp
