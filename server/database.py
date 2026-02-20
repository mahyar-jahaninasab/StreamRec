import os
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine, URL
import asyncio
import asyncpg
import datetime


from dotenv import load_dotenv  


load_dotenv()

DATABASE_URL = URL.create(
    drivername=os.getenv("DB_DRIVER"),
    username=os.getenv("DB_USER"),      
    password=os.getenv("DB_PASSWORD"),  
    host=os.getenv("DB_HOST"),         
    port=int(os.getenv("DB_PORT", 5432)), 
    database=os.getenv("DB_NAME"),    
)


engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

SessionMaker = async_sessionmaker(engine, c) 

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
async def main():
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect('postgresql://postgres@localhost/test')
    # Execute a statement to create a new table.
    await conn.execute('''
        CREATE TABLE users(
            id serial PRIMARY KEY,
            name text,
            dob date
        )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO users(name, dob) VALUES($1, $2)
    ''', 'Bob', datetime.date(1984, 3, 1))

    # Select a row from the table.
    row = await conn.fetchrow(
        'SELECT * FROM users WHERE name = $1', 'Bob')
    # *row* now contains
    # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))

    # Close the connection.
    await conn.close()

asyncio.run(main())