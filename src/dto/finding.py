from data.Solution import Solution
from data.apischema import GetRecommendationResponseItem
from db.models import Finding as DBFinding
from data.Finding import Category, AffectedComponent


def db_finding_to_response_item(
    find: DBFinding,
) -> GetRecommendationResponseItem:
    category = None
    try:
        recommendation = find.recommendations[0]
        category = Category.model_validate_json(recommendation.category)
    except Exception as e:
        category = Category()

    return GetRecommendationResponseItem(
        category=category,
        solution=Solution(
            short_description=(
                find.recommendations[0].description_short
                if find.recommendations
                else None
            ),
            long_description=(
                find.recommendations[0].description_long
                if find.recommendations
                else None
            ),
            search_terms=(
                find.recommendations[0].search_terms if find.recommendations else None
            ),
            metadata=(find.recommendations[0].meta if find.recommendations else {}),
        ),
    ).from_json(find.raw_data)
