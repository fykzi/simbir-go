from pydantic import BaseModel, Field
import enum
from typing import Optional
from database.models import TransportTypes


class AdmintransportTypes(str, enum.Enum):
    Car = "Car"
    Bike = "Bike"
    Scooter = "Scooter"
    All = "All"


class AdminTransportCreate(BaseModel):
    owner: int = Field(alias="ownerId", ge=1)
    canBeRented: Optional[bool] = None
    transportType: TransportTypes
    model: str
    color: str
    identifier: str
    description: str = None
    latitude: float
    longitude: float
    minutePrice: float = None
    dayPrice: float = None


class AdminTransportUpdate(BaseModel):
    owner: int = Field(alias="ownerId", ge=1, default=None)
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
