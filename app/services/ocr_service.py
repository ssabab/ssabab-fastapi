import requests
import uuid
import time
import json
import pandas as pd
import os
from app.core.config import settings

class OCRService:
    def __init__(self):
        self.api_url = settings.API_URL
        self.secret_key = settings.SECRET_KEY
        self.ocr_version = settings.OCR_VERSION
        self.enable_table_detection = settings.ENABLE_TABLE_DETECTION

    def extract_cell_text(self, cell):
        if 'cellTextLines' in cell and cell['cellTextLines']:
            lines = []
            for line in cell['cellTextLines']:
                words = [w['inferText'] for w in line.get('cellWords', []) if 'inferText' in w]
                if words:
                    lines.append(''.join(words))
            return '\n'.join(lines)
        return cell.get('inferText', '')

    def process_table(self, table):
        max_row = max(cell['rowIndex'] + cell.get('rowSpan', 1) - 1 for cell in table['cells'])
        max_col = max(cell['columnIndex'] + cell.get('columnSpan', 1) - 1 for cell in table['cells'])
        df = pd.DataFrame('', index=range(max_row + 1), columns=range(max_col + 1))
        
        for cell in table['cells']:
            text = self.extract_cell_text(cell)
            row = cell['rowIndex']
            col = cell['columnIndex']
            row_span = cell.get('rowSpan', 1)
            col_span = cell.get('columnSpan', 1)
            for r in range(row, row + row_span):
                for c in range(col, col + col_span):
                    if df.iloc[r, c]:
                        df.iloc[r, c] += '\n' + text
                    else:
                        df.iloc[r, c] = text
        return df

    def format_menu_block_json(self, menu_block):
        result = []
        for c in menu_block.columns[1:6]:
            items = [item.strip() for item in menu_block[c].dropna().astype(str).tolist() if item.strip()]
            result.append(items)
        return result

    async def process_image(self, file_content: bytes) -> dict:
        # 파일 크기 체크
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            raise ValueError(f"파일 크기가 너무 큽니다. 최대 {settings.MAX_UPLOAD_SIZE} bytes까지 허용됩니다.")

        # 임시 파일 저장
        temp_file = settings.UPLOAD_DIR / "temp_image.jpg"
        temp_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_file, "wb") as f:
            f.write(file_content)

        try:
            # OCR API 요청
            request_json = {
                'images': [{'format': 'jpg', 'name': 'demo'}],
                'requestId': str(uuid.uuid4()),
                'version': self.ocr_version,
                'timestamp': int(round(time.time() * 1000)),
                'enableTableDetection': self.enable_table_detection
            }

            payload = {'message': json.dumps(request_json).encode('UTF-8')}
            files = [('file', open(temp_file, 'rb'))]
            headers = {'X-OCR-SECRET': self.secret_key}

            response = requests.request("POST", self.api_url, headers=headers, data=payload, files=files)
            result = response.json()

            if 'tables' not in result['images'][0]:
                return {"error": "표를 찾을 수 없습니다."}

            # 표 처리
            tables = result['images'][0]['tables']
            processed_tables = []
            
            for table in tables:
                df = self.process_table(table)
                
                # 한식과 일품 행 추출
                hansik_rows = df[df[0] == '한식']
                ilpum_rows = df[df[0] == '일품']
                
                days = ['월', '화', '수', '목', '금']
                menu1 = self.format_menu_block_json(hansik_rows)
                menu2 = self.format_menu_block_json(ilpum_rows)
                
                menu_data = {
                    '요일': days,
                    '메뉴1_한식': menu1,
                    '메뉴2_일품': menu2
                }
                processed_tables.append(menu_data)

            return {"tables": processed_tables}

        finally:
            # 임시 파일 삭제
            if os.path.exists(temp_file):
                os.remove(temp_file)