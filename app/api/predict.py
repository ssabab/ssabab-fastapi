from fastapi import APIRouter
from app.schemas.predict import MenuComparisonRequest, MenuRecommendationResponse
from app.models.recommender import recommend_menu_by_score

router = APIRouter()

@router.post("/predict", response_model=MenuRecommendationResponse)
def recommend_menu(request: MenuComparisonRequest):
    recommended_id, score_a, score_b = recommend_menu_by_score(request.menu_id_a, request.menu_id_b)
    return MenuRecommendationResponse(
        recommended_menu_id=recommended_id,
        menu_a_score=round(score_a, 2),
        menu_b_score=round(score_b, 2)
    )
