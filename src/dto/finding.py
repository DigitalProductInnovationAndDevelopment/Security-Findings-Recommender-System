from models.models import Finding as DBFinding
from data.Finding import Finding

# def DBFindingToFindingWithSolution(db_finding: DBFinding,db_solution) -> Finding:
#     return Finding(
#         title=[t for t in db_finding.title_list],
#         source=db_finding.source,
#         description=db_finding.description,
#         cwe_ids=db_finding.cwe_ids,
#         cve_ids=db_finding.cve_ids,
#         severity=db_finding.severity,
#         priority=db_finding.priority,
#         location_list=db_finding.location_list,
#         category=db_finding.category,
#         solution=db_solution
#     )
