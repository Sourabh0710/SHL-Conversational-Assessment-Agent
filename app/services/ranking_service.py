def generate_recommendation_reason(
    query,
    assessment_name
):

    query_lower = query.lower()

    if "java" in query_lower:

        return (
            "Recommended because it evaluates "
            "Java programming and backend "
            "development skills."
        )

    if "python" in query_lower:

        return (
            "Recommended because it measures "
            "Python programming and software "
            "development capabilities."
        )

    if "sales" in query_lower:

        return (
            "Recommended because it evaluates "
            "sales aptitude and customer-facing "
            "skills."
        )

    if "leadership" in query_lower:

        return (
            "Recommended because it measures "
            "leadership and managerial competencies."
        )

    return (
        "Recommended due to strong semantic "
        "relevance with the user query."
    )


def rerank_results(query, results):

    query_lower = query.lower()

    scored_results = []

    for result in results:

        score = 0

        name = result["name"].lower()

        # JAVA BOOST
        if "java" in query_lower and "java" in name:
            score += 10

        # PYTHON BOOST
        if "python" in query_lower:

            backend_terms = [
                "programming",
                "software",
                "linux",
                "database",
                "engineering",
                "development",
                "coding",
                "backend"
            ]

            if any(term in name for term in backend_terms):
                score += 8

        # SALES BOOST
        if "sales" in query_lower and "sales" in name:
            score += 10

        # LEADERSHIP BOOST
        if "leadership" in query_lower:
            leadership_terms = [
                "leadership",
                "manager",
                "managerial",
                "opq"
            ]

            if any(term in name for term in leadership_terms):
                score += 10

        scored_results.append((score, result))

    # SORT DESCENDING
    scored_results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    reranked = [item[1] for item in scored_results]

    return reranked