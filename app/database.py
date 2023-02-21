from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
PASSWORD = "sql123"
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{PASSWORD}@127.0.0.1/blog"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    #  connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
