from app.services.retrieval_service import (
    retrieve_assessments
)

query = "Java backend developer assessment"

results = retrieve_assessments(query)

for result in results:

    print("\n-------------------")
    print("NAME:", result["name"])
    print("URL:", result["url"])
    print("ATTRIBUTES:", result["attributes"])