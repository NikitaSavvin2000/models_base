import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, func


Base = declarative_base()


class ModelInfo(Base):
    __tablename__ = 'models_info'

    id = Column(Integer, primary_key=True, index=True)
    model_path = Column(String, nullable=False)
    date = Column(DateTime, default=func.now())
    pipline = Column(JSON, nullable=True)
    metrix = Column(JSON, nullable=True)
    name = Column(String, nullable=False)
    size = Column(Float, nullable=False)
    lag = Column(Integer, nullable=False)
    point_per_call = Column(Integer, nullable=False)
    description = Column(String, nullable=False)


DATABASE_URL = "sqlite:///./models_info.db"


def reset_database():
    db_file = "./models_info.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Deleted existing database: {db_file}")
    else:
        print(f"No existing database found at: {db_file}")

    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    print("New database created successfully.")


if __name__ == "__main__":
    reset_database()
