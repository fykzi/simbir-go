from pydantic import BaseModel
from typing import Optional
import enum


class TransportTypes(str, enum.Enum):
    Car = "Car"
    Bike = "Bike"
    Scooter = "Scooter"


class TransportRead(BaseModel):
    transport_id: int
    canBeRented: bool
    transportType: TransportTypes
    model: str
    color: str
    identifier: str
    description: Optional[str]
    latitude: float
    longitude: float
    minutePrice: Optional[float]
    dayPrice: Optional[float]


class TransportCreate(BaseModel):
    canBeRented: bool
    transportType: TransportTypes
    model: str
    color: str
    identifier: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    minutePrice: Optional[float] = None
    dayPrice: Optional[float] = None


class TransportUpdate(BaseModel):
    canBeRented: Optional[bool] = None
    transportType: TransportTypes = None
    model: Optional[str] = None
    color: Optional[str] = None
    identifier: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    minutePrice: Optional[float] = None
    dayPrice: Optional[float] = None
