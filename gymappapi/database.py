import databases
import sqlalchemy

from gymappapi.config import config

metadata = sqlalchemy.MetaData()
membership_table = sqlalchemy.Table(
    "membership",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("valid_until", sqlalchemy.DateTime),
)

connect_args = {"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {}
engine = sqlalchemy.create_engine(config.DATABASE_URL, connect_args=connect_args)
metadata.create_all(engine)
database = databases.Database(config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK, min_size=1, max_size=3)
