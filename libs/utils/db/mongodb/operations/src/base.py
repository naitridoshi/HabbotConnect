from abc import ABC
from typing import Any, Dict, Generic, List, Optional, TypeVar

from bson import ObjectId

from libs.utils.db.mongodb.src.base_repository import BaseRepository

T = TypeVar("T")


class BaseOperations(ABC, Generic[T]):
    """Abstract base class for all database operations.Provides common CRUD operations and query patterns."""

    def __init__(self, repository: BaseRepository):
        """Initialize with a repository instance."""
        self._repository = repository

    @property
    def repository(self) -> BaseRepository:
        """Get the underlying repository."""
        return self._repository

    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Find a single document by its ID."""
        return self._repository.find_one({"_id": ObjectId(entity_id)})

    def find_all(
        self,
        query: Optional[Dict[str, Any]] = None,
        limit: int = 0,
        sort_key: Optional[str] = None,
        sort_type: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Find all documents matching the query."""
        cursor = self._repository.find(
            query=query or {}, limit=limit, sort_key=sort_key, sort_type=sort_type
        )
        return list(cursor)

    def create(self, data: Dict[str, Any]) -> str:
        """Create a new document."""
        result = self._repository.insert_one(data)
        return str(result.inserted_id)

    def update_by_id(self, entity_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a document by its ID."""
        result = self._repository.update_one(
            {"_id": ObjectId(entity_id)}, {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, entity_id: str) -> bool:
        """Delete a document by its ID."""
        result = self._repository.delete_one({"_id": ObjectId(entity_id)})
        return result.deleted_count > 0

    def count(self, query: Optional[Dict[str, Any]] = None) -> int:
        """Count documents matching the query."""
        return self._repository.count_documents(query or {})

    def exists(self, query: Dict[str, Any]) -> bool:
        """Check if any document matches the query."""
        return self._repository.find_one(query) is not None
