from fastapi import APIRouter, File, UploadFile
from app.services.ocr_service import OCRService
from app.schemas.ocr import OCRResponse

router = APIRouter()
ocr_service = OCRService()

@router.post("/ocr", response_model=OCRResponse)
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    result = await ocr_service.process_image(contents)
    return result