from fastapi import FastAPI
from app.api import ocr

app = FastAPI(title="OCR API")

# 라우터 등록
app.include_router(ocr.router, prefix="/api/v1", tags=["ocr"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)