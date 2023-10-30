from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.payment.handlers import payment_router
from api.v1.rent.handlers import rent_router
from api.v1.transport.handlers import transport_router
from api.v1.user.handlers import account_router
from api.v1.admin_accounts.handlers import admin_account_router
from api.v1.admin_transports.handlers import admin_transport_router
from api.v1.admin_rents.handlers import admin_rent_router
from app import settings


app = FastAPI(title="Simbir.GO", docs_url="/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

api_router = APIRouter()

api_router.include_router(account_router, prefix="/Account", tags=["AccountController"])
api_router.include_router(
    admin_account_router, prefix="/Admin/Account", tags=["AdminAccountController"]
)
api_router.include_router(payment_router, prefix="/Payment", tags=["PaymentController"])
api_router.include_router(
    transport_router, prefix="/Transport", tags=["TransportController"]
)
api_router.include_router(
    admin_transport_router, prefix="/Admin/Transport", tags=["AdminTranstorController"]
)
api_router.include_router(rent_router, prefix="/Rent", tags=["RentController"])
api_router.include_router(
    admin_rent_router, prefix="/Admin", tags=["AdminRentController"]
)

app.include_router(api_router, prefix="/api")
