from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./applications.db"

engine = create_engine(DATABASE_URL)