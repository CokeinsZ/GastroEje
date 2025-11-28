"""
Migration script to update enum values in PostgreSQL database.
This updates the userstatus and userrole enums to use lowercase values.
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings

async def migrate_enums():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        # For UserStatus enum - rename old values to new ones
        print("Migrating UserStatus enum...")
        
        # First, check if we need to migrate by trying to add the new values
        try:
            # Add new enum values if they don't exist
            await conn.execute(text(
                "ALTER TYPE userstatus ADD VALUE IF NOT EXISTS 'active'"
            ))
            await conn.execute(text(
                "ALTER TYPE userstatus ADD VALUE IF NOT EXISTS 'inactive'"
            ))
            await conn.execute(text(
                "ALTER TYPE userstatus ADD VALUE IF NOT EXISTS 'not_verified'"
            ))
            await conn.execute(text(
                "ALTER TYPE userstatus ADD VALUE IF NOT EXISTS 'banned'"
            ))
            
            # Update existing data
            await conn.execute(text(
                "UPDATE users SET status = 'active' WHERE status = 'ACTIVE'"
            ))
            await conn.execute(text(
                "UPDATE users SET status = 'inactive' WHERE status = 'INACTIVE'"
            ))
            await conn.execute(text(
                "UPDATE users SET status = 'not_verified' WHERE status = 'NOT_VERIFIED'"
            ))
            await conn.execute(text(
                "UPDATE users SET status = 'banned' WHERE status = 'BANNED'"
            ))
            
            print("UserStatus enum migrated successfully!")
            
        except Exception as e:
            print(f"Error migrating enums: {e}")
            print("\nAlternative: Drop and recreate tables")
            print("Run: python recreate_tables.py")
    
    await engine.dispose()

if __name__ == "__main__":
    from sqlalchemy import text
    asyncio.run(migrate_enums())
