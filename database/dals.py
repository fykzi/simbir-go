from sqlalchemy import select, update, and_, delete, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Literal, Optional
from database.models import User, Transport, Rent
from fastapi import HTTPException, status
from api.v1.rent.shemas import Coordinates
from datetime import datetime


class BaseDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class UserDAL(BaseDAL):
    async def sign_up(self, data: dict) -> User:
        new_user = User(**data)
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def get_user_by_username(self, username: str) -> User:
        query = select(User).where(User.username == username)
        res = await self.session.execute(query)
        user = res.first()
        if user:
            return user[0]

    async def get_user_by_user_id(self, user_id: int):
        query = select(User).where(User.user_id == user_id)
        user = await self.session.execute(query)
        return user.first()[0]

    async def user_update(self, user_id: int, data: dict) -> User:
        query = update(User).where(User.user_id == user_id).values(**data)
        await self.session.execute(query)
        user = await self.get_user_by_user_id(user_id)
        return user

    async def is_superuser(self, user_id: int) -> bool:
        query = select(User).where(
            and_(User.user_id == user_id, User.is_superuser == True)
        )
        result = await self.session.execute(query)
        if result.first():
            return True
        return False

    async def replenish_balance(self, account_id) -> User:
        query = (
            update(User)
            .where(User.user_id == account_id)
            .values(balance=User.balance + 250_000)
        )
        await self.session.execute(query)
        return await self.get_user_by_user_id(account_id)


class TransportDAL(BaseDAL):
    async def add_transport(self, data: dict) -> Transport:
        new_transport = Transport(**data)
        self.session.add(new_transport)
        await self.session.flush()
        return new_transport

    async def get_transport_by_id(self, transport_id: int) -> Transport:
        query = select(Transport).where(Transport.transport_id == transport_id)
        res = await self.session.execute(query)
        transport = res.first()
        if transport:
            return transport[0]

    async def is_owner(self, transport_id: int, user_id: int) -> bool:
        query = select(Transport).where(
            and_(Transport.transport_id == transport_id, Transport.owner == user_id)
        )
        result = await self.session.execute(query)
        if result.first():
            return True
        return False

    async def update_(self, transport_id: int, data: dict) -> Transport:
        query = (
            update(Transport)
            .where(Transport.transport_id == transport_id)
            .values(**data)
        )
        await self.session.execute(query)
        transport = await self.get_transport_by_id(transport_id)
        return transport

    async def delete_(self, transport_id: int) -> None:
        query = delete(Transport).where(Transport.transport_id == transport_id)
        await self.session.execute(query)

    async def can_be_rented(self, transport_id: int) -> bool:
        query = select(Transport).where(
            and_(Transport.transport_id == transport_id, Transport.canBeRented == True)
        )
        result = await self.session.execute(query)
        if result.first():
            return True
        return False

    async def change_located(
        self,
        transport_id,
        coordinates: dict[Literal["longitude"] | Literal["latitude"], float],
    ) -> None:
        query = (
            update(Transport)
            .where(Transport.transport_id == transport_id)
            .values(**coordinates)
        )
        await self.session.execute(query)

    async def switch_status(self, transport_id: int, status: bool):
        query = (
            update(Transport)
            .where(Transport.transport_id == transport_id)
            .values(canBeRented=status)
            .returning(Transport.canBeRented)
        )
        await self.session.execute(query)

    async def get_transports(self) -> List[Transport]:
        query = select(Transport).where(Transport.canBeRented == True)
        result = await self.session.execute(query)
        return result.all()


class RentDAL(BaseDAL):
    def get_transport_dal(self) -> TransportDAL:
        return TransportDAL(self.session)

    async def create_(self, data: dict) -> Rent:
        new_rent = Rent(**data)
        self.session.add(new_rent)
        await self.session.flush()
        await self.get_transport_dal().switch_status(data.get("transport_id"), False)
        return new_rent

    async def get_user_rents(self, user_id: int) -> List[Rent]:
        query = select(Rent).where(Rent.renter_id == user_id)
        result = await self.session.execute(query)
        rents = result.all()
        if not rents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You do not have rental agreements",
            )
        return rents

    async def is_renter(self, rent_id, user_id: int) -> bool:
        query = select(Rent).where(
            and_(Rent.rent_id == rent_id, Rent.renter_id == user_id)
        )
        result = await self.session.execute(query)
        if result.first():
            return True
        return False

    async def end_rent(self, rent_id: int, coordinates: Coordinates) -> None:
        query = (
            update(Rent)
            .where(Rent.rent_id == rent_id)
            .values(is_end=True, time_end=datetime.now())
            .returning(Rent.transport_id)
        )
        result = await self.session.execute(query)
        transport_id = result.first()[0]
        await self.get_transport_dal().switch_status(transport_id, True)
        await self.get_transport_dal().change_located(transport_id, coordinates)

    async def get_transport_rents(self, transport_id: int) -> List[Rent]:
        query = select(Rent).where(Rent.transport_id == transport_id)
        result = await self.session.execute(query)
        return result.all()

    async def is_renter_or_owner(self, rent_id: int, user_id: int) -> Optional[Rent]:
        query = select(Rent, Transport).where(
            and_(
                Rent.rent_id == rent_id,
                or_(Rent.renter_id == user_id, Transport.owner == user_id),
            )
        )
        result = await self.session.execute(query)
        rent = result.first()
        if rent:
            return rent[0]


class AdminAccountDAL(UserDAL):
    async def get_accounts(self, start: int, count: int) -> Optional[List[User]]:
        query = select(User).where(User.user_id >= start)
        res = await self.session.execute(query)
        res = res.fetchmany(abs(count))
        return res

    async def delete_(self, account_id: int) -> None:
        query = delete(User).where(User.user_id == account_id)
        await self.session.execute(query)


class AdminTransportDal(TransportDAL):
    async def get_transports(
        self,
        start: int,
        count: int,
        transport_type: str = None,
    ) -> Optional[List[Transport]]:
        if transport_type:
            query = select(Transport).where(
                and_(
                    Transport.transport_id >= start,
                    Transport.transportType == transport_type,
                )
            )
        else:
            query = select(Transport).where(
                Transport.transport_id >= start,
            )

        res = await self.session.execute(query)
        transports = res.fetchmany(abs(count))
        return transports

    async def delete_(self, transport_id: int) -> None:
        query = delete(Transport).where(Transport.transport_id == transport_id)
        await self.session.execute(query)


class AdminRentDAL(RentDAL):
    async def get_rent_by_id(self, rent_id: int) -> Rent:
        query = select(Rent).where(Rent.rent_id == rent_id)
        res = await self.session.execute(query)
        if rent := res.first():
            return rent[0]

    async def update_(self, rent_id: int, data: dict) -> Rent:
        query = (
            update(Rent).where(Rent.rent_id == rent_id).values(**data).returning(Rent)
        )
        res = await self.session.execute(query)
        rent = res.first()
        if rent:
            return rent[0]

    async def delete_(self, rent_id: int) -> None:
        query = delete(Rent).where(Rent.rent_id == rent_id)
        await self.session.execute(query)
