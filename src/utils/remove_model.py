import os

from config import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_base_create import ModelInfo


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_BASE_PATH = os.path.join(BASE_DIR, 'models')
PIPELINE_BASE_PATH = os.path.join(BASE_DIR, 'models_pipline')
DATABASE_URL = "sqlite:///./models_info.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def delete_model_by_id(model_id: str):
    db: Session = SessionLocal()
    try:
        model_record = db.query(ModelInfo).filter(ModelInfo.id == model_id).first()

        if model_record:
            model_file_path = model_record.model_path

            if os.path.exists(model_file_path):
                os.remove(model_file_path)
                logger.info(f"Model file {model_id}.h5 deleted at path {model_file_path}.")

            db.delete(model_record)
            db.commit()
            return f"Model record with ID: {model_id} deleted from database."
        else:
            logger.warning(f"Model with ID: {model_id} not found in the database.")
            return {"message": f"Model with ID: {model_id} not found."}

    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting model with ID {model_id}: {e}")
        raise

    finally:
        db.close()
