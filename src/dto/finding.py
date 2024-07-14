from data.Solution import Solution
from data.apischema import GetRecommendationResponseItem
from db.models import Finding as DBFinding


def db_finding_to_response_item(
        find: DBFinding,
) -> GetRecommendationResponseItem:
    return GetRecommendationResponseItem(
        category=(
            find.category
        ),
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
