from pydantic import BaseModel, Field
from database.models import RentTypes
from typing import Optional
from database.models import TransportTypes
from datetime import datetime


class AdminRentCreate(BaseModel):
    transport_id: int = Field(alias="transportId", ge=1)
    renter_id: int = Field(alias="userId", ge=1)
    time_start: datetime = Field(alias="timeStart")
    time_end: datetime = Field(alias="timeEnd", default=None)
    price_of_unit: float = Field(alias="priceOfUnit", ge=0)
    rent_type: RentTypes = Field(alias="priceType")
    final_price: float = Field(alias="finalPrice", default=None, ge=0)


class AdminUpdateRent(BaseModel):
    transport_id: Optional[int] = Field(alias="transportId", ge=1, default=None)
    renter_id: Optional[int] = Field(alias="userId", ge=1, default=None)
    time_start: Optional[datetime] = Field(alias="timeStart", default=None)
    time_end: Optional[datetime] = Field(alias="timeEnd", default=None)
    price_of_unit: Optional[float] = Field(alias="priceOfUnit", ge=0, default=None)
    rent_type: Optional[RentTypes] = Field(alias="priceType", default=None)
    final_price: Optional[float] = Field(alias="finalPrice", default=None, ge=0)
