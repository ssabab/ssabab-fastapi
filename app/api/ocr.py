from fastapi import APIRouter, File, UploadFile
from app.services.ocr_service import OCRService
from app.schemas.ocr import OCRResponse
from app.core.logger import logger
import time
from datetime import datetime

router = APIRouter()
ocr_service = OCRService()

@router.post("/ocr", response_model=OCRResponse)
async def process_image(file: UploadFile = File(...)):
    start_time = time.time()
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 요청 정보 로깅
    logger.info(f"OCR 요청 시작 - 시간: {request_time}, 파일명: {file.filename}, 크기: {file.size} bytes")
    
    try:
        contents = await file.read()
        result = await ocr_service.process_image(contents)
        
        # 응답 시간 계산
        response_time = time.time() - start_time
        
        # 성공 로깅
        logger.info(f"OCR 요청 성공 - 처리시간: {response_time:.2f}초")
        
        return result
        
    except Exception as e:
        # 에러 로깅
        logger.error(f"OCR 요청 실패 - 에러: {str(e)}")
        raise