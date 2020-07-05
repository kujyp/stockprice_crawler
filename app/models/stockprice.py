from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.models import db, TimestampMixin, BaseModelMixin


class StockpriceSimple:
    def __init__(self, corpcode: str, target_date: date, price: Optional[int]) -> None:
        super().__init__()
        self.corpcode = corpcode
        self.target_date = target_date
        self.is_holiday = price is None
        self.price = price

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, StockpriceSimple):
            return False

        return self.corpcode == o.corpcode \
            and self.target_date == o.target_date \
            and self.is_holiday == o.is_holiday \
            and self.price == o.price

    def __repr__(self) -> str:
        return f"<corpcode=[{self.corpcode}] "\
               f"target_date=[{self.target_date}] "\
               f"is_holiday=[{self.is_holiday}] "\
               f"price=[{self.price}]>"


class Stockprice(db.Model, BaseModelMixin, TimestampMixin):
    __tablename__ = 'stockprices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    target_date = db.Column(db.DateTime, nullable=True)
    corp = relationship("Corp", back_populates="stockprices")
    corp_id = db.Column(db.Integer, ForeignKey('corps.id'))
    is_holiday = db.Column(db.Boolean, default=False)
    price = db.Column(db.Integer, nullable=True)


def get_stockprice_or_none(stock, target_date: date) -> Optional[Stockprice]:
    stockprice = Stockprice.query \
        .filter_by(stock_id=stock.id) \
        .filter_by(target_date=target_date) \
        .one_or_none()
    return stockprice
