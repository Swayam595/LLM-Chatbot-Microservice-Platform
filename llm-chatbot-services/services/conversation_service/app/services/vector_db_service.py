"""This service is used to store and retrieve documents from the vector database."""

from chromadb import HttpClient
from shared import get_logger
from app.utils.embedding_utils import mock_embedding
from config import AppConfig


class VectorDBService:
    """Service for the vector database."""

    def __init__(self):
        """Initialize the vector database service."""
        self.app_config = AppConfig()
        self.client = HttpClient(host=self.app_config.CHROMA_DB_URL)
        self.collection = self.client.get_or_create_collection(name="conversations")
        self._logger = get_logger(service_name="conversation_service")

    def add_document(self, user_id: int, message_id: int, message: str):
        """Add a document to the vector database."""
        self._logger.info(
            f"Adding document to vector database for user {user_id} and message {message_id}"
        )
        vector = mock_embedding(message)
        self.collection.add(
            ids=[f"{user_id}-{message_id}"],
            documents=[message],
            metadatas=[{"user_id": user_id, "message_id": message_id}],
            embeddings=[vector],
        )
        self._logger.info(
            f"Document added to vector database for user {user_id} and message {message_id}"
        )

    def search_similar(self, user_id: int, query: str, top_k: int = 5) -> list[str]:
        """Search for similar documents in the vector database."""
        self._logger.info(
            f"Searching for similar documents in the vector database for user {user_id} and query {query}"
        )
        query_vector = mock_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_vector], n_results=top_k, where={"user_id": user_id}
        )
        return results["documents"][0] if results["documents"] else []
