import os
import io
import uuid
import h5py

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


async def get_model_size_in_mb(model_file_path):
    file_size_bytes = os.path.getsize(model_file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    file_size_mb = round(file_size_mb, 3)
    return file_size_mb


async def save_model(model_data, pipeline, metrics, name, lag, point_per_call, description):
    model_id = str(uuid.uuid4())
    os.makedirs(MODEL_BASE_PATH, exist_ok=True)

    model_file_path = os.path.join(MODEL_BASE_PATH, f"{model_id}.h5")
    model_file_like = io.BytesIO(model_data)
    model_data_cleaned = model_file_like.read().replace(b'\x00', b'')

    with h5py.File(model_file_path, 'w') as h5_file:
        h5_file.create_dataset('model_data', data=model_data_cleaned)

    size_in_mb = await get_model_size_in_mb(model_file_path)

    db: Session = SessionLocal()
    try:
        model_record = ModelInfo(
            model_path=model_file_path,
            pipline=pipeline,
            metrix=metrics,
            name=name,
            size=size_in_mb,
            lag=lag,
            point_per_call=point_per_call,
            description=description
        )
        db.add(model_record)
        db.commit()
        db.refresh(model_record)

        logger.info(f"Model saved with ID: {model_record.id}")
        return model_id

    except Exception as e:
        db.rollback()
        logger.error(f"Error saving model to database: {e}")
        raise

    finally:
        db.close()
