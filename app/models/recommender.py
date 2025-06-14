import pymysql
from typing import Tuple
from app.core.config import DB_CONFIG

def get_db_conn():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

def get_menu_average_score(conn, menu_id: int) -> float:
    query = """
    SELECT AVG(fr.food_score) AS avg_score
    FROM menu_food mf
    JOIN food_review fr ON mf.food_id = fr.food_id
    WHERE mf.menu_id = %s
    """
    with conn.cursor() as cur:
        cur.execute(query, (menu_id,))
        result = cur.fetchone()
        return result["avg_score"] or 0.0

def recommend_menu_by_score(menu_a: int, menu_b: int) -> Tuple[int, float, float]:
    conn = get_db_conn()
    score_a = get_menu_average_score(conn, menu_a)
    score_b = get_menu_average_score(conn, menu_b)
    conn.close()
    recommended = menu_a if score_a >= score_b else menu_b
    return recommended, score_a, score_b
