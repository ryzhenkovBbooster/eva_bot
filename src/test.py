import asyncio
from urllib.parse import quote


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


# password = "!bG2$B5DipTV3%bd"
# encoded_password = quote(password)
# DATABASE_URL = f"postgresql+asyncpg://postgres:{encoded_password}@44.205.114.26:5432/postgres"
#
# engine = create_async_engine(DATABASE_URL, echo=True)
#
# # Создаем асинхронную сессию
# AsyncSessionLocal = sessionmaker(
#     bind=engine, class_=AsyncSession, expire_on_commit=False
# )
#
# async def test_connection():
#     # Создаем новую сессию
#     async with AsyncSessionLocal() as session:
#         # Простой запрос для проверки подключения
#         result = await session.execute(text('SELECT 1'))
#         value = result.scalar_one()
#         print(value)  # Должно вывести "1"
#
# asyncio.run(test_connection())



name = 'rjgrweigj rigjwoigj edd'
rudiment = name.split(' ')[-1]
name = name.replace(f" {rudiment}", '')

print(name)