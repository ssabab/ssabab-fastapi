from pydantic import BaseModel

class MenuComparisonRequest(BaseModel):
    menu_id_a: int
    menu_id_b: int

class MenuRecommendationResponse(BaseModel):
    recommended_menu_id: int
    menu_a_score: float
    menu_b_score: float