from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.accessibility_features import router as accessibility_router
from app.routes.allergens import router as allergen_router
from app.routes.categories import router as category_router
from app.routes.dishes import router as dish_router
from app.routes.establishments import router as establishment_router
from app.routes.menu import router as menu_router
from app.routes.reservations import router as reservation_router
from app.routes.reviews import router as review_router
from app.routes.users import router as user_router

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(accessibility_router)
app.include_router(allergen_router)
app.include_router(category_router)
app.include_router(dish_router)
app.include_router(establishment_router)
app.include_router(menu_router)
app.include_router(reservation_router)
app.include_router(review_router)
app.include_router(user_router) 