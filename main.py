from fastapi import FastAPI
from app.api import ocr
from app.api import predict

app = FastAPI(title="MLOps API")

# 라우터 등록
app.include_router(ocr.router, prefix="/api/v1", tags=["ocr"])
app.include_router(predict.router, prefix="/api/v1", tags=["predict"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)