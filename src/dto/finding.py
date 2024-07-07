from data.Solution import Solution
from data.apischema import GetRecommendationResponseItem
from db.models import Finding as DBFinding
from data.Finding import Finding, FindingKind


def db_finding_to_response_item(
    find: DBFinding,
) -> GetRecommendationResponseItem:

    return GetRecommendationResponseItem(
        category=(
            FindingKind[find.recommendations[0].category]
            if find.recommendations
            else FindingKind.DEFAULT
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
