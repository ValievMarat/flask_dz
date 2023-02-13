import atexit
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PG_DSN = 'postgresql://app:app@127.0.0.1:5431/advertisement'

engine = sq.create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class User(Base):

    __tablename__ = 'app_users'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    username = sq.Column(sq.String, nullable=False, unique=True, index=True)
    password = sq.Column(sq.String, nullable=False)
    mail = sq.Column(sq.String, nullable=False)
    created_at = sq.Column(sq.DateTime, server_default=sq.func.now())


class Advert(Base):

    __tablename__ = 'app_adverts'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    caption = sq.Column(sq.String(length=100), nullable=False)
    description = sq.Column(sq.Text, nullable=False)
    created_at = sq.Column(sq.DateTime, server_default=sq.func.now())
    owner_id = sq.Column(sq.Integer, sq.ForeignKey("app_users.id"), nullable=False)


# Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)
