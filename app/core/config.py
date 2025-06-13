from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, Set
from pathlib import Path

class Settings(BaseSettings):
    # API 설정
    API_URL: str
    SECRET_KEY: str
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # 파일 업로드 설정
    UPLOAD_DIR: Path = Path("uploads")
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: str = "jpg,jpeg,png"  # 문자열로 변경
    
    # OCR 설정
    OCR_VERSION: str = "V2"
    ENABLE_TABLE_DETECTION: bool = True
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @property
    def allowed_extensions_set(self) -> Set[str]:
        """허용된 확장자 집합을 반환"""
        return set(self.ALLOWED_EXTENSIONS.split(","))
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    설정을 싱글톤으로 관리하기 위한 함수
    """
    return Settings()

# 설정 인스턴스 생성
settings = get_settings()