from pydantic import BaseModel, Field
from database.models import RentTypes
from typing import Optional
from database.models import TransportTypes
from datetime import datetime


class RentCreate(BaseModel):
    rent_type: RentTypes = Field(alias="rentType")


class RentRead(BaseModel):
    rent_id: int
    renter_id: int
    transport_id: int
    rent_type: RentTypes = Field(alias="priceType")
    is_end: Optional[bool] = None  # TODO delete None
    time_start: str = Field(alias="timeStart")
    time_end: Optional[str] = Field(alias="timeEnd", default=None)
    price_of_unit: float = Field(alias="priceOfUnit", ge=0)
    final_price: Optional[float] = Field(alias="finalPrice", default=None, ge=0)


class Coordinates(BaseModel):
    latitude: float = Field(alias="lat")
    longitude: float = Field(alias="long")


class RentTransportRead(BaseModel):
    latitude: float = Field(alias="lat")
    longitude: float = Field(alias="long")
    radius: float = 0
    transport_type: TransportTypes = Field(alias="type")
