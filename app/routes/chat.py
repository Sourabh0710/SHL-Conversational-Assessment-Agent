from fastapi import APIRouter

from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse

from app.services.retrieval_service import (
    retrieve_assessments
)

from app.services.conversation_service import (
    save_conversation,
    get_conversation_context
)

from app.services.ranking_service import (
    generate_recommendation_reason,
    rerank_results
)

from app.utils.helpers import ATTRIBUTE_MAPPING

router = APIRouter()


# OFF-TOPIC DETECTION
OFF_TOPIC_KEYWORDS = [
    "weather",
    "ipl",
    "movie",
    "movies",
    "cricket",
    "football",
    "politics",
    "bitcoin",
    "crypto",
    "celebrity",
    "stock market",
    "news"
]


# VAGUE QUERIES
VAGUE_QUERIES = [
    "help hiring",
    "need assessment",
    "recommend something",
    "help me recruit",
    "need hiring help",
    "assessment recommendation"
]


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    query = request.query
    session_id = request.session_id

    query_lower = query.lower().strip()

    # ---------------------------------
    # OFF-TOPIC REFUSAL
    # ---------------------------------

    if any(
        keyword in query_lower
        for keyword in OFF_TOPIC_KEYWORDS
    ):

        return ChatResponse(
            response=(
                "I specialize in recommending "
                "SHL assessments and talent "
                "evaluation solutions."
            ),
            recommendations=[]
        )

    # ---------------------------------
    # VAGUE QUERY HANDLING
    # ---------------------------------

    if query_lower in VAGUE_QUERIES:

        return ChatResponse(
            response=(
                "Could you clarify the role, "
                "skills, seniority level, or "
                "job category you are hiring for?"
            ),
            recommendations=[]
        )

    # ---------------------------------
    # SAVE CONVERSATION
    # ---------------------------------

    save_conversation(session_id, query)

    # ---------------------------------
    # GET CONTEXT
    # ---------------------------------

    previous_queries = get_conversation_context(
        session_id
    )

    # BUILD CONTEXTUAL QUERY
    contextual_query = " ".join(previous_queries)

    # ---------------------------------
    # RETRIEVE RESULTS
    # ---------------------------------

    results = retrieve_assessments(
        contextual_query,
        top_k=15
    )

    # ---------------------------------
    # RERANK RESULTS
    # ---------------------------------

    results = rerank_results(
        contextual_query,
        results
    )

    # FINAL TOP 10
    results = results[:10]

    recommendations = []

    for result in results:

        recommendations.append({

            "name": result["name"],

            "url": result["url"],

            "attributes": [
                ATTRIBUTE_MAPPING.get(attr, attr)
                for attr in result["attributes"]
            ],

            "reason": generate_recommendation_reason(
                contextual_query,
                result["name"]
            )
        })

    # ---------------------------------
    # RESPONSE MESSAGE
    # ---------------------------------

    response_text = (
        f"For the ongoing conversation, "
        f"I identified {len(recommendations)} "
        f"relevant SHL assessments using "
        f"context-aware hybrid retrieval "
        f"and intelligent reranking."
    )

    return ChatResponse(
        response=response_text,
        recommendations=recommendations
    )