import json
import uvicorn

from utils.models_write import save_model
from src.config import logger, public_or_local
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form, HTTPException


if public_or_local == 'LOCAL':
    url = 'http://localhost'
else:
    url = 'http://11.11.11.11'

origins = [
    url
]

app = FastAPI(docs_url="/models_base/docs", openapi_url='/models_base/openapi.json')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

example = {
    "description": "test"
}


@app.post("/models_base/save")
async def save_model_endpoint(
        pipeline: str = Form(...),
        metrics: str = Form(...),
        name: str = Form(...),
        lag: int = Form(...),
        point_per_call: int = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
):
    try:
        try:
            pipeline_dict = json.loads(pipeline)
            metrics_dict = json.loads(metrics)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON in pipeline or metrics: {e}"
            )

        model_data = await file.read()

        model_id = await save_model(
            model_data=model_data,
            pipeline=pipeline_dict,
            metrics=metrics_dict,
            name=name,
            lag=lag,
            point_per_call=point_per_call,
            description=description
        )

        return {"model_id": model_id}

    except HTTPException as e:
        raise e

    except Exception as ApplicationError:
        logger.error(f"Unexpected error: {ApplicationError}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
            headers={"X-Error": str(ApplicationError)},
        )


@app.get("/")
def read_root():
    return {"message": "Welcome to the indicators System API"}


if __name__ == "__main__":
    port = 7070
    uvicorn.run(app, host="0.0.0.0", port=port)
