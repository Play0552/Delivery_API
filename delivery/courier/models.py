from sqlalchemy.orm import relationship, mapped_column, Mapped

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList

from delivery.database import Base


class Courier(Base):
    __tablename__ = "courier_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    districts = mapped_column(MutableList.as_mutable(ARRAY(String)), index=True, nullable=False)

    active_order: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="courier",
        primaryjoin="and_(Courier.id == Order.courier_id, Order.status == 'in_progress')"
        )


