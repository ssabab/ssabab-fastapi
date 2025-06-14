from loguru import logger
import sys
from pathlib import Path
from datetime import datetime

# 로그 디렉토리 생성
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 현재 날짜로 로그 파일명 생성
current_date = datetime.now().strftime("%Y-%m-%d")
log_file = log_dir / f"{current_date}.log"
error_log_file = log_dir / "error.log"

# 기본 로거 설정 제거
logger.remove()

# 콘솔 출력 설정
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# 일반 로그 파일 설정
logger.add(
    log_file,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="00:00",  # 매일 자정에 새로운 파일 생성
    retention="30 days"  # 30일간 보관
)

# 에러 로그 파일 설정
logger.add(
    error_log_file,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="100 MB",  # 100MB마다 새로운 파일 생성
    retention="30 days"  # 30일간 보관
)
