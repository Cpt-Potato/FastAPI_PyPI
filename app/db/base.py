import databases
import sqlalchemy

from app.core.config import DATABASE_URL

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)


# def create_tables():
#     from sqlalchemy import create_engine
#     engine = create_engine(DATABASE_URL)
#     metadata.drop_all(engine)
#     metadata.create_all(engine)
