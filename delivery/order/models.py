from datetime import datetime

from sqlalchemy.orm import relationship, mapped_column, Mapped

from delivery.order.schemas import Status
from sqlalchemy import ForeignKey

from sqlalchemy import String, Integer, TIMESTAMP

from delivery.database import Base


class Order(Base):
    __tablename__ = "order_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    district: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[Status] = mapped_column(nullable=False, default=Status.in_progress)
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, default=None)

    courier_id: Mapped[int] = mapped_column(Integer, ForeignKey("courier_table.id"), nullable=False)
    courier: Mapped["Courier"] = relationship(
        "Courier",
        back_populates="active_order")

