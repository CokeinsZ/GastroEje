"""
Script to drop and recreate all database tables.
WARNING: This will delete all existing data!
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
from app.database import Base

# Import all models to ensure they're registered with Base
from app.models.users import User
from app.models.establishments import Establishment
from app.models.dishes import Dish
from app.models.categories import Category
from app.models.allergens import Allergens
from app.models.menus import Menu
from app.models.reservations import Reservation
from app.models.reviews import Review
from app.models.accessibility_features import AccessibilityFeature
from app.models.dish_allergen import DishAllergen
from app.models.dish_category import DishCategory
from app.models.establishment_category import EstablishmentCategory
from app.models.user_allergen import UserAllergen

async def recreate_database():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        print("Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)
        
        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
        
    await engine.dispose()
    print("Database recreated successfully!")

if __name__ == "__main__":
    print("WARNING: This will delete all existing data!")
    response = input("Do you want to continue? (yes/no): ")
    
    if response.lower() == 'yes':
        asyncio.run(recreate_database())
    else:
        print("Operation cancelled.")
