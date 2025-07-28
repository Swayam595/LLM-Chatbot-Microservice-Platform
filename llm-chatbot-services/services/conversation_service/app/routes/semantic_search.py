from fastapi import APIRouter, Query, Depends
from shared import get_logger
from app.dependencies.dependency_factory import get_vector_db_service
from app.services.vector_db_service import VectorDBService

logger = get_logger(service_name="conversation_service")

router = APIRouter(prefix="/semantic-search", tags=["Semantic Search"])

@router.get("/")
async def search_messages(query: str = Query(...), user_id: int = Query(...), vector_db: VectorDBService = Depends(get_vector_db_service)):
    """Return semantically similar messages"""
    logger.info(f"Searching for similar messages for user {user_id} with query {query}")
    return {"matches": vector_db.search_similar(user_id=user_id, query=query)}
