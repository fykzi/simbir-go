import uuid
import enum
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ENUM, DOUBLE_PRECISION, TIME
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    balance: Mapped[float] = mapped_column(DOUBLE_PRECISION(asdecimal=True), default=0)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    # transport = relationship("Transport", cascade="delete-orphan")

    def __str__(self) -> str:
        return f"{self.user_id} {self.username}"

    def __repr__(self) -> str:
        return f"{self.user_id} {self.username}"

    def get_user_info(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "balance": self.balance,
            "is_superuser": self.is_superuser,
        }


class TransportTypes(str, enum.Enum):
    Car = "Car"
    Bike = "Bike"
    Scooter = "Scooter"


class Transport(Base):
    __tablename__ = "transports"

    transport_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    canBeRented: Mapped[bool] = mapped_column(Boolean, default=True)
    transportType: Mapped[str] = mapped_column(ENUM(TransportTypes))
    model: Mapped[str]
    color: Mapped[str]
    identifier: Mapped[str]
    description: Mapped[str] = mapped_column(String, nullable=True)
    latitude: Mapped[DOUBLE_PRECISION(asdecimal=True)] = mapped_column(DOUBLE_PRECISION)
    longitude: Mapped[DOUBLE_PRECISION(asdecimal=True)] = mapped_column(
        DOUBLE_PRECISION
    )
    minutePrice: Mapped[DOUBLE_PRECISION(asdecimal=True)] = mapped_column(
        DOUBLE_PRECISION, nullable=True
    )
    dayPrice: Mapped[DOUBLE_PRECISION(asdecimal=True)] = mapped_column(
        DOUBLE_PRECISION, nullable=True
    )
    owner: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"))

    def __str__(self) -> str:
        return f"ID: {self.transport_id}"

    def __repr__(self) -> str:
        return f"ID: {self.transport_id}"

    def get_transport_info(self) -> dict:
        return {
            "transport_id": self.transport_id,
            "canBeRented": self.canBeRented,
            "transportType": self.transportType.value,
            "model": self.model,
            "color": self.color,
            "identifier": self.identifier,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "minutePrice": self.minutePrice,
            "dayPrice": self.dayPrice,
            # "owner": self.owner.username,
        }

    def get_transport_info_for_rent_search(self) -> dict:
        return {
            "lat": self.latitude,
            "long": self.longitude,
            "type": self.transportType.value,
        }


class RentTypes(str, enum.Enum):
    Minutes = "Minutes"
    Days = "Days"


class Rent(Base):
    __tablename__ = "rents"

    rent_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    renter_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="SET NULL")
    )
    transport_id: Mapped[int] = mapped_column(
        ForeignKey("transports.transport_id", ondelete="SET NULL")
    )
    rent_type: Mapped[str] = mapped_column(ENUM(RentTypes))
    is_end: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=True
    )  # TODO delete nullable
    time_start: Mapped[TIME] = mapped_column(TIME)
    time_end: Mapped[TIME] = mapped_column(TIME, nullable=True)
    price_of_unit: Mapped[DOUBLE_PRECISION(asdecimal=True)] = mapped_column(
        DOUBLE_PRECISION, default=1
    )
    final_price: Mapped[DOUBLE_PRECISION(asdecimal=True)] = mapped_column(
        DOUBLE_PRECISION, nullable=True
    )

    def __str__(self):
        return f"rent_id: {self.rent_id}"

    def get_rent_info(self) -> dict:
        return {
            "rent_id": self.rent_id,
            "renter_id": self.renter_id,
            "transport_id": self.transport_id,
            "priceType": self.rent_type.value,
            "is_end": self.is_end,
            "timeStart": str(self.time_start),
            "timeEnd": str(self.time_end),
            "priceOfUnit": self.price_of_unit,
            "finalPrice": self.final_price,
        }
