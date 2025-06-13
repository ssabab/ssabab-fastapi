import requests
import uuid
import time
import json
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

api_url = os.getenv('API_URL')
secret_key = os.getenv('SECRET_KEY')
image_file = 'test.jpg'  # 이미지 파일명에 맞게 수정

request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000)),
    'enableTableDetection': True
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
result = response.json()

print(json.dumps(result, indent=2, ensure_ascii=False))  # 응답 전체 출력

if 'tables' in result['images'][0]:
    print("tables:", result['images'][0]['tables'])
else:
    print("tables 필드가 없습니다.")

def extract_cell_text(cell):
    # cellTextLines가 있으면 그 안의 cellWords의 inferText를 모두 합침
    if 'cellTextLines' in cell and cell['cellTextLines']:
        lines = []
        for line in cell['cellTextLines']:
            words = [w['inferText'] for w in line.get('cellWords', []) if 'inferText' in w]
            if words:
                lines.append(''.join(words))
        return '\n'.join(lines)
    # 없으면 inferText 사용
    return cell.get('inferText', '')

# 표 추출 결과 처리 (tables 사용)
if 'tables' in result['images'][0]:
    tables = result['images'][0]['tables']
    for table_idx, table in enumerate(tables):
        max_row = max(cell['rowIndex'] + cell.get('rowSpan', 1) - 1 for cell in table['cells'])
        max_col = max(cell['columnIndex'] + cell.get('columnSpan', 1) - 1 for cell in table['cells'])
        df = pd.DataFrame('', index=range(max_row + 1), columns=range(max_col + 1))
        for cell in table['cells']:
            text = extract_cell_text(cell)
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
        print(df)
        df.to_csv(f'table_{table_idx + 1}.csv', index=False)

# OCR로 추출된 표를 DataFrame으로 불러오기
df = pd.read_csv('table_1.csv', header=None)

print(df[0].tolist())

days = ['월', '화', '수', '목', '금']

# '한식'과 '일품' 행만 추출
hansik_rows = df[df[0] == '한식']
ilpum_rows = df[df[0] == '일품']

def format_menu_block_json(menu_block):
    result = []
    for c in menu_block.columns[1:6]:  # 1~5열(요일별)
        items = [item.strip() for item in menu_block[c].dropna().astype(str).tolist() if item.strip()]
        result.append(json.dumps(items, ensure_ascii=False))
    return result

menu1 = format_menu_block_json(hansik_rows)
menu2 = format_menu_block_json(ilpum_rows)

final_df = pd.DataFrame({
    '요일': days,
    '메뉴1(한식)': menu1,
    '메뉴2(일품)': menu2
})

print(final_df)
final_df.to_csv('final_menu_table.csv', index=False)